"""Google Sheets data access layer — replaces a traditional database."""

import gspread
from google.oauth2.service_account import Credentials
import os
import json
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

# ── connection ────────────────────────────────────────────────────────────────

_spreadsheet = None


def get_spreadsheet():
    global _spreadsheet
    if _spreadsheet is not None:
        return _spreadsheet

    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if creds_json:
        info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        path = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
        creds = Credentials.from_service_account_file(path, scopes=SCOPES)

    gc = gspread.authorize(creds)
    _spreadsheet = gc.open_by_key(os.environ["GOOGLE_SHEET_ID"])
    return _spreadsheet


def ws(name: str):
    return get_spreadsheet().worksheet(name)


# ── simple cache (avoids hammering Sheets API) ────────────────────────────────

_cache: dict[str, tuple[Any, float]] = {}


def _cached(key: str, ttl: int = 60) -> Any:
    if key in _cache:
        data, ts = _cache[key]
        if time.time() - ts < ttl:
            return data
    return None


def _set(key: str, data: Any):
    _cache[key] = (data, time.time())


def _bust(key: str):
    _cache.pop(key, None)


# ── sheet initialisation ──────────────────────────────────────────────────────

SHEET_HEADERS = {
    "users":         ["id", "username", "email", "password_hash", "is_admin", "is_active", "created_at"],
    "invite_tokens": ["token", "email", "used", "created_at", "expires_at"],
    "matches":       ["match_code", "stage", "home_team", "away_team", "venue",
                      "match_time_utc", "home_score", "away_score", "is_completed", "notes"],
    "predictions":   ["key", "user_id", "match_code", "home_score", "away_score",
                      "points_earned", "created_at", "updated_at"],
}


def init_sheets():
    ss = get_spreadsheet()
    existing = {ws.title for ws in ss.worksheets()}
    for name, headers in SHEET_HEADERS.items():
        if name not in existing:
            sheet = ss.add_worksheet(title=name, rows=2000, cols=len(headers))
            sheet.append_row(headers, value_input_option="RAW")
    # remove default blank sheet if present alongside real sheets
    if "Sheet1" in existing and len(existing) >= len(SHEET_HEADERS):
        try:
            ss.del_worksheet(ss.worksheet("Sheet1"))
        except Exception:
            pass


# ── users ─────────────────────────────────────────────────────────────────────

def _parse_user(row: dict) -> dict:
    return {
        "id":            int(row["id"]),
        "username":      row["username"],
        "email":         row["email"],
        "password_hash": row["password_hash"],
        "is_admin":      row["is_admin"] == "True",
        "is_active":     row["is_active"] == "True",
        "created_at":    row["created_at"],
    }


def get_all_users() -> list[dict]:
    cached = _cached("users")
    if cached is not None:
        return cached
    rows = ws("users").get_all_records()
    users = [_parse_user(r) for r in rows if r.get("id")]
    _set("users", users)
    return users


def get_user_by_email(email: str) -> Optional[dict]:
    return next((u for u in get_all_users() if u["email"].lower() == email.lower()), None)


def get_user_by_id(uid: int) -> Optional[dict]:
    return next((u for u in get_all_users() if u["id"] == uid), None)


def get_user_by_username(username: str) -> Optional[dict]:
    return next((u for u in get_all_users() if u["username"].lower() == username.lower()), None)


def create_user(username: str, email: str, password_hash: str, is_admin: bool = False) -> dict:
    users = get_all_users()
    new_id = max((u["id"] for u in users), default=0) + 1
    row = [new_id, username, email, password_hash, str(is_admin), "True",
           datetime.now(timezone.utc).isoformat()]
    ws("users").append_row(row, value_input_option="RAW")
    _bust("users")
    return get_user_by_email(email)  # re-fetch to confirm


def user_count() -> int:
    return len(get_all_users())


# ── invite tokens ─────────────────────────────────────────────────────────────

def _parse_token(row: dict) -> dict:
    return {
        "token":      row["token"],
        "email":      row["email"],
        "used":       row["used"] == "True",
        "created_at": row["created_at"],
        "expires_at": row["expires_at"],
    }


def get_invite_token(token: str) -> Optional[dict]:
    rows = ws("invite_tokens").get_all_records()
    for r in rows:
        if r.get("token") == token:
            return _parse_token(r)
    return None


def create_invite_token(email: str, expires_at: datetime) -> str:
    token = str(uuid.uuid4())
    row = [token, email, "False",
           datetime.now(timezone.utc).isoformat(), expires_at.isoformat()]
    ws("invite_tokens").append_row(row, value_input_option="RAW")
    return token


def mark_token_used(token: str):
    sheet = ws("invite_tokens")
    cell = sheet.find(token, in_column=1)
    if cell:
        # column 3 is "used"
        sheet.update_cell(cell.row, 3, "True")


# ── matches ───────────────────────────────────────────────────────────────────

def _parse_match(row: dict) -> dict:
    return {
        "match_code":    row["match_code"],
        "stage":         row["stage"],
        "home_team":     row["home_team"],
        "away_team":     row["away_team"],
        "venue":         row.get("venue", ""),
        "match_time_utc": datetime.fromisoformat(row["match_time_utc"]).replace(tzinfo=timezone.utc)
                          if row.get("match_time_utc") else None,
        "home_score":    int(row["home_score"]) if str(row.get("home_score", "")).strip() != "" else None,
        "away_score":    int(row["away_score"]) if str(row.get("away_score", "")).strip() != "" else None,
        "is_completed":  row.get("is_completed", "") == "True",
        "notes":         row.get("notes", ""),
    }


def get_all_matches() -> list[dict]:
    cached = _cached("matches", ttl=120)
    if cached is not None:
        return cached
    rows = ws("matches").get_all_records()
    matches = [_parse_match(r) for r in rows if r.get("match_code")]
    _set("matches", matches)
    return matches


def get_match(match_code: str) -> Optional[dict]:
    return next((m for m in get_all_matches() if m["match_code"] == match_code), None)


def matches_count() -> int:
    rows = ws("matches").get_all_records()
    return len([r for r in rows if r.get("match_code")])


def clear_matches():
    """Wipe all match rows (keeps header) for a clean reload."""
    sheet = ws("matches")
    sheet.clear()
    sheet.append_row(SHEET_HEADERS["matches"], value_input_option="RAW")
    _bust("matches")


def bulk_insert_matches(matches: list[dict]):
    sheet = ws("matches")
    rows = []
    for m in matches:
        rows.append([
            m["match_code"], m["stage"], m["home_team"], m["away_team"],
            m.get("venue", ""), m["match_time_utc"], "", "", "False", m.get("notes", "")
        ])
    sheet.append_rows(rows, value_input_option="RAW")
    _bust("matches")


def update_match_score(match_code: str, home_score: int, away_score: int):
    sheet = ws("matches")
    rows = sheet.get_all_records()
    for i, row in enumerate(rows, start=2):  # row 1 is header
        if row.get("match_code") == match_code:
            sheet.update(f"G{i}:I{i}", [[home_score, away_score, "True"]])
            break
    _bust("matches")
    _bust("predictions")  # so points get recalculated on next fetch


def update_match_teams(match_code: str, home_team: str, away_team: str):
    sheet = ws("matches")
    rows = sheet.get_all_records()
    for i, row in enumerate(rows, start=2):
        if row.get("match_code") == match_code:
            sheet.update(f"C{i}:D{i}", [[home_team, away_team]])
            break
    _bust("matches")


# ── predictions ───────────────────────────────────────────────────────────────

def _parse_prediction(row: dict) -> dict:
    return {
        "key":          row["key"],
        "user_id":      int(row["user_id"]),
        "match_code":   row["match_code"],
        "home_score":   int(row["home_score"]),
        "away_score":   int(row["away_score"]),
        "points_earned": int(row["points_earned"]) if str(row.get("points_earned", "")).strip() != "" else None,
        "created_at":   row["created_at"],
        "updated_at":   row["updated_at"],
    }


def get_all_predictions() -> list[dict]:
    cached = _cached("predictions", ttl=30)
    if cached is not None:
        return cached
    rows = ws("predictions").get_all_records()
    preds = [_parse_prediction(r) for r in rows if r.get("key")]
    _set("predictions", preds)
    return preds


def get_prediction(user_id: int, match_code: str) -> Optional[dict]:
    key = f"{user_id}|{match_code}"
    return next((p for p in get_all_predictions() if p["key"] == key), None)


def upsert_prediction(user_id: int, match_code: str, home_score: int, away_score: int):
    key = f"{user_id}|{match_code}"
    now = datetime.now(timezone.utc).isoformat()
    sheet = ws("predictions")
    rows = sheet.get_all_records()
    for i, row in enumerate(rows, start=2):
        if row.get("key") == key:
            sheet.update(f"D{i}:H{i}", [[home_score, away_score, "", now, now]])
            _bust("predictions")
            return
    # not found → insert
    sheet.append_row([key, user_id, match_code, home_score, away_score, "", now, now],
                     value_input_option="RAW")
    _bust("predictions")


def award_points(match_code: str, actual_home: int, actual_away: int):
    """Calculate and write points for all predictions on a completed match."""
    sheet = ws("predictions")
    rows = sheet.get_all_records()
    for i, row in enumerate(rows, start=2):
        if row.get("match_code") != match_code:
            continue
        ph, pa = int(row["home_score"]), int(row["away_score"])
        if ph == actual_home and pa == actual_away:
            pts = 3
        elif (ph - pa > 0) == (actual_home - actual_away > 0) == True:
            pts = 1
        elif (ph - pa < 0) == (actual_home - actual_away < 0) == True:
            pts = 1
        elif ph == pa and actual_home == actual_away:
            pts = 1
        else:
            pts = 0
        sheet.update_cell(i, 6, pts)
    _bust("predictions")


def get_leaderboard() -> list[dict]:
    """Return users sorted by total points."""
    preds = get_all_predictions()
    users = get_all_users()
    totals: dict[int, int] = {}
    predicted: dict[int, int] = {}
    for p in preds:
        uid = p["user_id"]
        pts = p["points_earned"] or 0
        totals[uid] = totals.get(uid, 0) + pts
        predicted[uid] = predicted.get(uid, 0) + 1

    board = []
    for u in users:
        if not u["is_active"]:
            continue
        uid = u["id"]
        board.append({
            "user_id":   uid,
            "username":  u["username"],
            "points":    totals.get(uid, 0),
            "predicted": predicted.get(uid, 0),
        })
    board.sort(key=lambda x: (-x["points"], x["username"]))
    for i, row in enumerate(board, start=1):
        row["rank"] = i
    return board

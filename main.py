from fastapi import FastAPI, Request, Form, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

import sheets
import auth as authlib
import email_service
from fixtures_data import get_all_fixtures

app = FastAPI(title="FWC 2026 Predictor")
templates = Jinja2Templates(directory="templates")

NPT = timezone(timedelta(hours=5, minutes=45))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")

_FIFA_BASE   = "https://api.fifa.com/api/v3"
_FIFA_PARAMS = "idCompetition=17&idSeason=285023&language=en"
_GROUP_ORDER_ALPHA = [f"Group {c}" for c in "ABCDEFGHIJKL"]


def _str(val) -> str:
    """FIFA API returns either plain strings or [{Locale, Description}] arrays."""
    if isinstance(val, str):
        return val
    if isinstance(val, list) and val:
        d = val[0]
        return d.get("Description", "") if isinstance(d, dict) else str(d)
    return ""


def _compute_standings_from_matches(matches: list) -> list:
    groups: dict = {}
    for m in matches:
        gname = _str(m.get("GroupName", ""))
        if not gname or "Group" not in gname:
            continue
        home_obj = m.get("Home", {})
        away_obj = m.get("Away", {})
        ht = _str(home_obj.get("TeamName", ""))
        at = _str(away_obj.get("TeamName", ""))
        if not ht or not at:
            continue
        if gname not in groups:
            groups[gname] = {}
        for team in (ht, at):
            if team not in groups[gname]:
                groups[gname][team] = {"team": team, "P": 0, "W": 0, "D": 0, "L": 0,
                                       "GF": 0, "GA": 0, "GD": 0, "Pts": 0}
        # Score is in Home.Score or top-level HomeTeamScore
        hs = home_obj.get("Score") if home_obj.get("Score") is not None else m.get("HomeTeamScore")
        as_ = away_obj.get("Score") if away_obj.get("Score") is not None else m.get("AwayTeamScore")
        if hs is None or as_ is None:
            continue
        hs, as_ = int(hs), int(as_)
        for team, gf, ga in ((ht, hs, as_), (at, as_, hs)):
            groups[gname][team]["P"]  += 1
            groups[gname][team]["GF"] += gf
            groups[gname][team]["GA"] += ga
            groups[gname][team]["GD"]  = groups[gname][team]["GF"] - groups[gname][team]["GA"]
        if hs > as_:
            groups[gname][ht]["W"] += 1; groups[gname][ht]["Pts"] += 3; groups[gname][at]["L"] += 1
        elif hs < as_:
            groups[gname][at]["W"] += 1; groups[gname][at]["Pts"] += 3; groups[gname][ht]["L"] += 1
        else:
            groups[gname][ht]["D"] += 1; groups[gname][ht]["Pts"] += 1
            groups[gname][at]["D"] += 1; groups[gname][at]["Pts"] += 1

    result = []
    for g in _GROUP_ORDER_ALPHA:
        if g in groups:
            teams = sorted(groups[g].values(),
                           key=lambda x: (-x["Pts"], -x["GD"], -x["GF"], x["team"]))
            result.append({"name": g, "teams": teams})
    return result


# ── template helpers ──────────────────────────────────────────────────────────

def to_npt(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(NPT)


def prediction_status(match_time_utc: datetime) -> str:
    now = datetime.now(timezone.utc)
    if match_time_utc.tzinfo is None:
        match_time_utc = match_time_utc.replace(tzinfo=timezone.utc)
    opens  = match_time_utc - timedelta(hours=24)
    closes = match_time_utc - timedelta(hours=1)
    if now < opens:
        return "upcoming"
    if opens <= now < closes:
        return "open"
    if closes <= now < match_time_utc:
        return "closed"
    return "live"   # past kickoff, not yet marked complete by admin


def enrich_matches(matches: list[dict], user_id: Optional[int] = None) -> list[dict]:
    preds = {}
    if user_id:
        all_preds = sheets.get_all_predictions()
        preds = {p["match_code"]: p for p in all_preds if p["user_id"] == user_id}
    enriched = []
    for m in matches:
        m = dict(m)
        m["npt_time"] = to_npt(m["match_time_utc"])
        m["status"] = prediction_status(m["match_time_utc"])
        m["user_prediction"] = preds.get(m["match_code"])
        enriched.append(m)
    return enriched


def current_user(request: Request) -> Optional[dict]:
    token = request.cookies.get("session")
    if not token:
        return None
    payload = authlib.decode_token(token)
    if not payload:
        return None
    return sheets.get_user_by_id(int(payload["sub"]))


_TEAM_ISO: dict[str, str] = {
    "Algeria": "dz", "Argentina": "ar", "Australia": "au", "Austria": "at",
    "Belgium": "be", "Bosnia and Herzegovina": "ba", "Brazil": "br", "Canada": "ca",
    "Cape Verde": "cv", "Colombia": "co", "Croatia": "hr", "Curaçao": "cw",
    "Czech Republic": "cz", "DR Congo": "cd", "Ecuador": "ec", "Egypt": "eg",
    "England": "gb-eng", "France": "fr", "Germany": "de", "Ghana": "gh",
    "Haiti": "ht", "Iran": "ir", "Iraq": "iq", "Ivory Coast": "ci",
    "Japan": "jp", "Jordan": "jo", "Mexico": "mx", "Morocco": "ma",
    "Netherlands": "nl", "New Zealand": "nz", "Norway": "no", "Panama": "pa",
    "Paraguay": "py", "Portugal": "pt", "Qatar": "qa", "Saudi Arabia": "sa",
    "Scotland": "gb-sct", "Senegal": "sn", "South Africa": "za", "South Korea": "kr",
    "Spain": "es", "Sweden": "se", "Switzerland": "ch", "Tunisia": "tn",
    "Turkey": "tr", "United States": "us", "Uruguay": "uy", "Uzbekistan": "uz",
}

def _flag_url(name: str) -> str:
    code = _TEAM_ISO.get(name)
    if not code:
        return ""
    return f"https://flagcdn.com/w40/{code}.png"

templates.env.filters["npt"] = lambda dt: to_npt(dt).strftime("%d %b %Y, %I:%M %p NPT")
templates.env.globals["prediction_status"] = prediction_status
templates.env.globals["flag_url"] = _flag_url


# ── startup ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup():
    print(f"[startup] BASE_URL = {BASE_URL}")
    try:
        sheets.init_sheets()
    except Exception as e:
        print(f"[startup] Google Sheets init warning: {e}")
        print("[startup] App will still start — Sheets will connect on first request.")


# ── health check ─────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


# ── FIFA official standings proxy ─────────────────────────────────────────────

@app.get("/api/fifa-standings")
async def fifa_standings_api():
    import httpx as _httpx
    payload: dict = {"live": [], "groups": [], "source": ""}

    async with _httpx.AsyncClient(timeout=10) as client:
        # Live matches
        try:
            r = await client.get(f"{_FIFA_BASE}/live/football?{_FIFA_PARAMS}")
            if r.status_code == 200:
                live_raw = r.json().get("Results", [])
                payload["live"] = [
                    {
                        "home": _str(m.get("Home", {}).get("TeamName", "")),
                        "away": _str(m.get("Away", {}).get("TeamName", "")),
                        "home_score": m.get("Home", {}).get("Score"),
                        "away_score": m.get("Away", {}).get("Score"),
                        "minute": m.get("MatchTime", ""),
                        "group": _str(m.get("GroupName", "")),
                        "venue": _str((m.get("Stadium") or {}).get("Name", "")),
                    }
                    for m in live_raw
                ]
        except Exception:
            pass

        # Official standings endpoint (activates once matches start)
        try:
            r = await client.get(f"{_FIFA_BASE}/standings?{_FIFA_PARAMS}")
            if r.status_code == 200:
                data = r.json().get("Results", [])
                groups = []
                for grp in data:
                    gname = _str(grp.get("Name") or grp.get("GroupName", ""))
                    if not gname or "Group" not in gname:
                        continue
                    teams = []
                    for entry in grp.get("Teams", []):
                        t = entry.get("Team", {})
                        teams.append({
                            "team": _str(t.get("Name", "")),
                            "P":    entry.get("Played", 0),
                            "W":    entry.get("Won", 0),
                            "D":    entry.get("Drawn", 0),
                            "L":    entry.get("Lost", 0),
                            "GF":   entry.get("GoalsFor", 0),
                            "GA":   entry.get("GoalsAgainst", 0),
                            "GD":   entry.get("GoalDifference", 0),
                            "Pts":  entry.get("Points", 0),
                        })
                    if teams:
                        groups.append({"name": gname, "teams": teams})
                if groups:
                    payload["source"] = "standings"
                    payload["groups"] = groups
                    return JSONResponse(payload)
        except Exception:
            pass

        # Fallback: compute from match results
        try:
            r = await client.get(f"{_FIFA_BASE}/calendar/matches?{_FIFA_PARAMS}&count=500")
            if r.status_code == 200:
                payload["source"] = "matches"
                payload["groups"] = _compute_standings_from_matches(r.json().get("Results", []))
                return JSONResponse(payload)
        except Exception:
            pass

    payload["source"] = "error"
    return JSONResponse(payload, status_code=503)


# ── public routes ─────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user = current_user(request)
    if user:
        return RedirectResponse("/dashboard", status_code=302)
    return RedirectResponse("/login", status_code=302)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str = ""):
    user = current_user(request)
    if user:
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": error,
    })


@app.post("/login")
async def login_post(request: Request,
                     email: str = Form(...),
                     password: str = Form(...)):
    user = sheets.get_user_by_email(email.strip().lower())
    if not user or not authlib.verify_password(password, user["password_hash"]):
        return templates.TemplateResponse("login.html", {
            "request": request, "error": "Invalid email or password."
        }, status_code=400)
    if not user["is_active"]:
        return templates.TemplateResponse("login.html", {
            "request": request, "error": "Account is disabled."
        }, status_code=400)
    token = authlib.create_token(user["id"], user["is_admin"])
    resp = RedirectResponse("/dashboard", status_code=302)
    resp.set_cookie("session", token, httponly=True, max_age=60 * 60 * 24 * 14, samesite="lax")
    return resp


@app.get("/logout")
def logout():
    resp = RedirectResponse("/login", status_code=302)
    resp.delete_cookie("session")
    return resp


@app.get("/register/{token}", response_class=HTMLResponse)
def register_page(request: Request, token: str):
    inv = sheets.get_invite_token(token)
    if not inv:
        return templates.TemplateResponse("error.html", {
            "request": request, "message": "Invalid or expired invitation link."
        })
    if inv["used"]:
        return templates.TemplateResponse("error.html", {
            "request": request, "message": "This invitation link has already been used."
        })
    exp = datetime.fromisoformat(inv["expires_at"])
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > exp:
        return templates.TemplateResponse("error.html", {
            "request": request, "message": "This invitation link has expired."
        })
    return templates.TemplateResponse("register.html", {
        "request": request, "token": token, "email": inv["email"], "error": ""
    })


@app.post("/register/{token}")
async def register_post(request: Request, token: str,
                        username: str = Form(...),
                        password: str = Form(...),
                        password2: str = Form(...)):
    inv = sheets.get_invite_token(token)
    if not inv or inv["used"]:
        return RedirectResponse("/login", status_code=302)

    error = ""
    if len(username) < 3:
        error = "Username must be at least 3 characters."
    elif len(password) < 6:
        error = "Password must be at least 6 characters."
    elif password != password2:
        error = "Passwords do not match."
    elif sheets.get_user_by_username(username):
        error = "Username already taken."
    elif sheets.get_user_by_email(inv["email"]):
        error = "An account with this email already exists."

    if error:
        return templates.TemplateResponse("register.html", {
            "request": request, "token": token, "email": inv["email"], "error": error
        }, status_code=400)

    is_first = sheets.user_count() == 0
    pw_hash = authlib.hash_password(password)
    user = sheets.create_user(username.strip(), inv["email"].lower(), pw_hash, is_admin=is_first)
    sheets.mark_token_used(token)

    token_jwt = authlib.create_token(user["id"], user["is_admin"])
    resp = RedirectResponse("/dashboard", status_code=302)
    resp.set_cookie("session", token_jwt, httponly=True, max_age=60 * 60 * 24 * 14, samesite="lax")
    return resp


# ── setup route (first-time only) ────────────────────────────────────────────

@app.get("/setup", response_class=HTMLResponse)
def setup_page(request: Request):
    if sheets.user_count() > 0:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("setup.html", {"request": request, "error": ""})


@app.post("/setup")
async def setup_post(request: Request,
                     username: str = Form(...),
                     email: str = Form(...),
                     password: str = Form(...)):
    if sheets.user_count() > 0:
        return RedirectResponse("/login", status_code=302)

    # Init matches if sheet is empty
    if sheets.matches_count() == 0:
        fixtures = get_all_fixtures()
        sheets.bulk_insert_matches(fixtures)

    pw_hash = authlib.hash_password(password)
    user = sheets.create_user(username.strip(), email.strip().lower(), pw_hash, is_admin=True)
    token = authlib.create_token(user["id"], True)
    resp = RedirectResponse("/admin", status_code=302)
    resp.set_cookie("session", token, httponly=True, max_age=60 * 60 * 24 * 14, samesite="lax")
    return resp


# ── authenticated routes ──────────────────────────────────────────────────────

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    now = datetime.now(timezone.utc)
    all_matches = sheets.get_all_matches()

    live = [m for m in all_matches
            if not m["is_completed"] and m["match_time_utc"] and m["match_time_utc"] <= now]
    live.sort(key=lambda m: m["match_time_utc"])
    live = enrich_matches(live, user["id"])

    upcoming = [m for m in all_matches
                if not m["is_completed"] and m["match_time_utc"] and m["match_time_utc"] > now]
    upcoming.sort(key=lambda m: m["match_time_utc"])
    upcoming = enrich_matches(upcoming[:10], user["id"])

    recent = [m for m in all_matches if m["is_completed"]]
    recent.sort(key=lambda m: m["match_time_utc"], reverse=True)
    recent = enrich_matches(recent[:5], user["id"])

    all_preds = [p for p in sheets.get_all_predictions() if p["user_id"] == user["id"]]
    total_pts = sum(p["points_earned"] or 0 for p in all_preds)
    predicted_count = len(all_preds)

    lb = sheets.get_leaderboard()
    my_rank = next((r["rank"] for r in lb if r["user_id"] == user["id"]), "-")

    open_matches = [m for m in upcoming if m["status"] == "open"]

    return templates.TemplateResponse("dashboard.html", {
        "request": request, "user": user,
        "live": live, "upcoming": upcoming, "recent": recent,
        "total_pts": total_pts, "predicted_count": predicted_count,
        "my_rank": my_rank, "total_users": len(lb),
        "open_count": len(open_matches),
    })


@app.get("/fixtures", response_class=HTMLResponse)
def fixtures_page(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    all_matches = sheets.get_all_matches()
    all_matches.sort(key=lambda m: m["match_time_utc"] or datetime.min.replace(tzinfo=timezone.utc))
    enriched = enrich_matches(all_matches, user["id"])

    stage_order = [
        "Group A","Group B","Group C","Group D","Group E","Group F",
        "Group G","Group H","Group I","Group J","Group K","Group L",
        "Round of 32","Round of 16","Quarter-Final","Semi-Final","Third Place","Final"
    ]
    grouped: dict[str, list] = {}
    for m in enriched:
        grouped.setdefault(m["stage"], []).append(m)

    stages = [(s, grouped[s]) for s in stage_order if s in grouped]
    live_now = [m for m in enriched if not m["is_completed"] and m["status"] == "live"]

    return templates.TemplateResponse("fixtures.html", {
        "request": request, "user": user, "stages": stages, "live_now": live_now,
    })


@app.get("/predict/{match_code}", response_class=HTMLResponse)
def predict_page(request: Request, match_code: str):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    match = sheets.get_match(match_code)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    status = prediction_status(match["match_time_utc"])
    existing = sheets.get_prediction(user["id"], match_code)

    return templates.TemplateResponse("predict.html", {
        "request": request, "user": user, "match": match,
        "npt_time": to_npt(match["match_time_utc"]),
        "status": status, "existing": existing,
    })


@app.post("/predict/{match_code}")
async def predict_post(request: Request, match_code: str,
                       home_score: int = Form(...),
                       away_score: int = Form(...)):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    match = sheets.get_match(match_code)
    if not match:
        raise HTTPException(status_code=404)

    status = prediction_status(match["match_time_utc"])
    if status != "open":
        raise HTTPException(status_code=400, detail="Predictions are not open for this match.")

    if home_score < 0 or away_score < 0:
        raise HTTPException(status_code=400, detail="Scores cannot be negative.")

    sheets.upsert_prediction(user["id"], match_code, home_score, away_score)
    return RedirectResponse("/fixtures", status_code=302)


@app.get("/predictions/{match_code}", response_class=HTMLResponse)
def predictions_page(request: Request, match_code: str):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    match = sheets.get_match(match_code)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    status = prediction_status(match["match_time_utc"])
    if status in ("open", "upcoming"):
        raise HTTPException(status_code=403, detail="Predictions not yet revealed.")

    all_users = {u["id"]: u for u in sheets.get_all_users()}
    preds = [p for p in sheets.get_all_predictions() if p["match_code"] == match_code]
    preds.sort(key=lambda p: (-(p["points_earned"] or 0), (p.get("username") or "").lower()))

    return templates.TemplateResponse("predictions.html", {
        "request": request, "user": user,
        "match": match,
        "npt_time": to_npt(match["match_time_utc"]),
        "status": status,
        "preds": preds,
        "all_users": all_users,
    })


@app.get("/leaderboard", response_class=HTMLResponse)
def leaderboard(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)

    board = sheets.get_leaderboard()
    return templates.TemplateResponse("leaderboard.html", {
        "request": request, "user": user, "board": board,
    })


# ── admin routes ──────────────────────────────────────────────────────────────

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    user = current_user(request)
    if not user or not user["is_admin"]:
        return RedirectResponse("/dashboard", status_code=302)

    users = sheets.get_all_users()
    matches = sheets.get_all_matches()
    matches.sort(key=lambda m: m["match_time_utc"] or datetime.min.replace(tzinfo=timezone.utc))
    enriched = enrich_matches(matches)

    return templates.TemplateResponse("admin.html", {
        "request": request, "user": user,
        "users": users, "matches": enriched,
    })


@app.post("/admin/invite")
async def admin_invite(request: Request,
                       email: str = Form(...)):
    user = current_user(request)
    if not user or not user["is_admin"]:
        return RedirectResponse("/dashboard", status_code=302)

    # Check not already registered
    if sheets.get_user_by_email(email.strip().lower()):
        return RedirectResponse("/admin?msg=already_registered", status_code=302)

    expires = datetime.now(timezone.utc) + timedelta(hours=48)
    token = sheets.create_invite_token(email.strip().lower(), expires)
    invite_link = f"{BASE_URL}/register/{token}"

    try:
        await email_service.send_invite_email(email.strip(), invite_link)
        return RedirectResponse("/admin?msg=invite_sent", status_code=302)
    except Exception as e:
        import urllib.parse
        err = urllib.parse.quote(str(e)[:200])
        print(f"[email error] {e}")
        return RedirectResponse(f"/admin?msg=email_error&detail={err}", status_code=302)


@app.post("/admin/update-score/{match_code}")
async def update_score(request: Request, match_code: str,
                       home_score: int = Form(...),
                       away_score: int = Form(...)):
    user = current_user(request)
    if not user or not user["is_admin"]:
        raise HTTPException(status_code=403)

    sheets.update_match_score(match_code, home_score, away_score)
    sheets.award_points(match_code, home_score, away_score)
    return RedirectResponse("/admin?msg=score_updated", status_code=302)


@app.post("/admin/update-teams/{match_code}")
async def update_teams(request: Request, match_code: str,
                       home_team: str = Form(...),
                       away_team: str = Form(...)):
    user = current_user(request)
    if not user or not user["is_admin"]:
        raise HTTPException(status_code=403)

    sheets.update_match_teams(match_code, home_team.strip(), away_team.strip())
    return RedirectResponse("/admin?msg=teams_updated", status_code=302)


@app.post("/admin/load-fixtures")
async def load_fixtures(request: Request):
    user = current_user(request)
    if not user or not user["is_admin"]:
        raise HTTPException(status_code=403)

    if sheets.matches_count() == 0:
        fixtures = get_all_fixtures()
        sheets.bulk_insert_matches(fixtures)
    return RedirectResponse("/admin?msg=fixtures_loaded", status_code=302)


@app.post("/admin/reload-fixtures")
async def reload_fixtures(request: Request):
    """Clear all matches and reload from the official fixture list."""
    user = current_user(request)
    if not user or not user["is_admin"]:
        raise HTTPException(status_code=403)

    sheets.clear_matches()
    fixtures = get_all_fixtures()
    sheets.bulk_insert_matches(fixtures)
    return RedirectResponse("/admin?msg=fixtures_reloaded", status_code=302)

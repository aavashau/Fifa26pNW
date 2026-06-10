import httpx
import os

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
SENDER_EMAIL  = os.getenv("SMTP_USER", "fifaworldcuppredictor@gmail.com").strip()

_BREVO_URL = "https://api.brevo.com/v3/smtp/email"


async def send_invite_email(to_email: str, invite_link: str, inviter_name: str = "The Admin"):
    html = f"""
<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background:#0f1117;color:#fff;margin:0;padding:20px;">
  <div style="max-width:540px;margin:0 auto;background:#1a1f2e;border-radius:12px;padding:40px;border:1px solid #2d3748;">
    <div style="text-align:center;margin-bottom:30px;">
      <img src="https://m.media-amazon.com/images/M/MV5BNzk0NGIyMTctNmRkZi00ODQ0LWFhYjMtZDlmOTI3Y2JjMTRhXkEyXkFqcGc@.jpg"
           alt="FIFA World Cup 2026" width="80" height="80"
           style="border-radius:12px;object-fit:contain;display:block;margin:0 auto 12px;"/>
      <h1 style="color:#FFD700;margin:10px 0;font-size:24px;">FIFA World Cup 2026</h1>
      <h2 style="color:#00c853;margin:0;font-size:18px;">Score Predictor</h2>
    </div>
    <p style="color:#a0aec0;line-height:1.6;">You've been invited to join our private FWC 2026 prediction game!</p>
    <p style="color:#a0aec0;line-height:1.6;">Predict scores for every match from the Group Stage to the Final and climb the leaderboard.</p>
    <div style="text-align:center;margin:30px 0;">
      <a href="{invite_link}"
         style="background:#00c853;color:#000;padding:14px 32px;border-radius:8px;
                text-decoration:none;font-weight:bold;font-size:16px;display:inline-block;">
        Accept Invitation &amp; Register
      </a>
    </div>
    <p style="color:#718096;font-size:13px;">This link expires in 48 hours. If you didn't request this, ignore this email.</p>
    <p style="color:#718096;font-size:12px;border-top:1px solid #2d3748;padding-top:16px;margin-top:24px;">
      FWC 2026 Score Predictor &middot; Private Game
    </p>
  </div>
</body>
</html>
"""

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            _BREVO_URL,
            headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"},
            json={
                "sender": {"name": "FIFA WC 2026 Predictor", "email": SENDER_EMAIL},
                "to":     [{"email": to_email}],
                "subject": "You're invited to FWC 2026 Score Predictor!",
                "htmlContent": html,
            },
        )

    if resp.status_code not in (200, 201):
        raise Exception(f"Brevo error {resp.status_code}: {resp.text[:200]}")

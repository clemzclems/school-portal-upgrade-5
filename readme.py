# readme_gen.py
# Writes README.md safely without using triple-quoted strings.

import os
from datetime import datetime

def backup_and_write(path: str, content: str):
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{path}.bak-{ts}"
        with open(path, "rb") as rf, open(bak, "wb") as wf:
            wf.write(rf.read())
        print(f"• Backed up {path} -> {bak}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Wrote {path}")

lines = [
"# School Portal Upgrade 5",
"",
"Node.js + Express + SQLite school portal with Admin / Teacher / Student / Parent portals,",
"CSV import, attendance, employment/jobs, library/blog, printable report cards,",
"email/SMS notifications.",
"",
"## 🚀 Quick Start",
"",
"```bash",
"# 1) install deps",
"npm install",
"",
"# 2) create .env (see .env.example) then seed admin",
"npm run seed",
"",
"# 3) run",
"npm start   # http://localhost:3000",
"```",
"",
"## Scripts",
"- `npm start` — start Express server (server.js)",
"- `npm run seed` — create initial admin user from `.env` values",
"",
"## Required Env (see .env.example)",
"- `SITE_NAME`, `PORT`, `SESSION_SECRET`",
"- `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURE`, `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL`",
"- Optional: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`",
"- `BASE_URL` (for links in emails), `NODE_ENV`",
"",
"## Default Routes",
"- `/` — Home / login",
"- `/admin` — Admin dashboard",
"- `/teacher` — Teacher dashboard",
"- `/student` — Student dashboard",
"- `/parent` — Parent dashboard",
"- `/jobs` — Jobs portal",
"- `/health` — health JSON",
"",
"## Notes",
"- SQLite DB file is created automatically.",
"- If email/SMS env vars are missing, messages are logged to the console.",
"- Print-friendly report card at `/report/:studentId`.",
"",
]

if __name__ == "__main__":
    backup_and_write("README.md", "\n".join(lines) + "\n")
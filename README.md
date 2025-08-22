# School Portal Upgrade 5

Node.js + Express + SQLite school portal with Admin / Teacher / Student / Parent portals,
CSV import, attendance, employment/jobs, library/blog, printable report cards,
email/SMS notifications.

## 🚀 Quick Start

```bash
# 1) install deps
npm install

# 2) create .env (see .env.example) then seed admin
npm run seed

# 3) run
npm start   # http://localhost:3000
```

## Scripts
- `npm start` — start Express server (server.js)
- `npm run seed` — create initial admin user from `.env` values

## Required Env (see .env.example)
- `SITE_NAME`, `PORT`, `SESSION_SECRET`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURE`, `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL`
- Optional: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`
- `BASE_URL` (for links in emails), `NODE_ENV`

## Default Routes
- `/` — Home / login
- `/admin` — Admin dashboard
- `/teacher` — Teacher dashboard
- `/student` — Student dashboard
- `/parent` — Parent dashboard
- `/jobs` — Jobs portal
- `/health` — health JSON

## Notes
- SQLite DB file is created automatically.
- If email/SMS env vars are missing, messages are logged to the console.
- Print-friendly report card at `/report/:studentId`.


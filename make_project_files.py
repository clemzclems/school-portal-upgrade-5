# make_project_files.py
# Creates/updates .gitignore, README.md, .env, and .env.example with backups.

import os
from datetime import datetime

def backup_and_write(path: str, content: str):
    """If file exists, make a timestamped backup, then write fresh content."""
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{path}.bak-{ts}"
        with open(path, "rb") as rf, open(bak, "wb") as wf:
            wf.write(rf.read())
        print(f"• Backed up {path} -> {bak}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")
    print(f"✓ Wrote {path}")

GITIGNORE = r'''# ---- Node / package managers ----
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-lock.yaml
.pnpm-store/

# ---- Environment & secrets ----
.env
.env.local
.env.*.local

# ---- OS / Editor cruft ----
.DS_Store
Thumbs.db
*.swp
*.swo

# ---- Build outputs (if any) ----
dist/
build/

# ---- Backups & temp ----
*.bak
*.tmp
*.log
'''

README = '''# School Portal Upgrade 5

A Node.js + Express + SQLite school portal with **Admin / Teacher / Student / Parent** portals, **attendance**, **employment/jobs**, **CSV import**, **PIN result view**, **printable report cards**, and **email/SMS notifications** (email via Gmail SMTP App Password; SMS via Twilio if configured).

---

## 🔧 Requirements

- Node.js 18+ (Termux/Android or Windows/Mac/Linux)
- npm (comes with Node)
- SQLite (bundled via `sqlite3` package; no external install needed)

---

## 📦 Install

```bash
# 1) go to the project folder
cd school-portal-upgrade-5

# 2) install dependencies
npm install
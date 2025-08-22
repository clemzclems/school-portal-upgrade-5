# gitignore.py
# Creates/updates a .gitignore file with Node.js/Express defaults.
# Usage: python gitignore.py

import os
from datetime import datetime

def backup_and_write(path: str, content: str):
    """Backup old file if exists, then write fresh content."""
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{path}.bak-{ts}"
        with open(path, "rb") as rf, open(bak, "wb") as wf:
            wf.write(rf.read())
        print(f"• Backed up {path} -> {bak}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")
    print(f"✓ Wrote {path}")

GITIGNORE = """# ---- Node / package managers ----
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
"""

if __name__ == "__main__":
    backup_and_write(".gitignore", GITIGNORE)
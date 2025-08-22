#!/usr/bin/env python3
"""
termux_setup.py
- Switches project to better-sqlite3 (no compiler issues on Termux)
- Installs server dependencies
- Writes server.js and db.js with safe backups

Usage:
  python termux_setup.py
"""

import os
import shutil
import subprocess
from datetime import datetime
from shutil import which

# ---------- helpers ----------
def sh(cmd, cwd=None):
    print(f"\n$ {cmd}")
    try:
        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"!! Command failed (ignored so you can continue): {e}")

def backup_and_write(path: str, content: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{path}.bak-{ts}"
        shutil.copy2(path, bak)
        print(f"• Backed up {os.path.basename(path)} → {os.path.basename(bak)}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")
    print(f"✓ Wrote {os.path.basename(path)}")

def ensure_not_in_storage():
    here = os.getcwd()
    if here.startswith("/storage/"):
        print("⚠️  You are running in /storage/... . On Android this can cause npm symlink problems.")
        print("   Tip: move your project into $HOME (Termux) e.g.:")
        print("     mkdir -p ~/workspace")
        print("     mv /storage/emulated/0/Download/school-portal-upgrade-5 ~/workspace/")
        print("     cd ~/workspace/school-portal-upgrade-5")
        print("   Then run this script again.\n")

# ---------- file contents ----------
SERVER_JS = r"""// server.js
require('dotenv').config();

const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const session = require('express-session');

const app = express();

/* ------------ Basics ------------ */
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// NOTE: in-memory session store is fine for Termux/dev.
// For production, use a persistent store (connect-sqlite3/redis, etc).
app.use(
  session({
    secret: process.env.SESSION_SECRET || 'dev-session-secret',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 1000 * 60 * 60 }, // 1 hour
  })
);

/* ------------ Static & Views ------------ */
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Optional global available in all EJS templates
app.locals.siteName = process.env.SITE_NAME || 'School Portal';

/* ------------ Routes ------------ */
// Your route files should `module.exports = router`
try {
  const authRoutes       = require('./src/routes/auth');
  const adminRoutes      = require('./src/routes/admin');
  const teacherRoutes    = require('./src/routes/teacher');
  const studentRoutes    = require('./src/routes/student');
  const parentRoutes     = require('./src/routes/parent');
  const employmentRoutes = require('./src/routes/employment');

  app.use('/', authRoutes);
  app.use('/admin', adminRoutes);
  app.use('/teacher', teacherRoutes);
  app.use('/student', studentRoutes);
  app.use('/parent', parentRoutes);
  app.use('/jobs', employmentRoutes);
} catch (e) {
  // If some route files aren’t present yet, don’t crash during setup
  console.warn('⚠️  Some route modules were not loaded:', e.message);
}

/* ------------ Home & Health ------------ */
app.get('/', (req, res) => {
  try {
    res.render('index', { user: req.session.user || null });
  } catch (e) {
    console.error(e);
    res.status(500).send('Template error');
  }
});

app.get('/health', (_req, res) => res.json({ ok: true }));

/* ------------ 404 & Errors ------------ */
app.use((req, res, next) => {
  if (res.headersSent) return next();
  res.status(404);
  try {
    return res.render('404', { url: req.originalUrl });
  } catch {
    return res.send('404 Not Found');
  }
});

// Final error handler
app.use((err, _req, res, _next) => {
  console.error('Unhandled error:', err);
  if (!res.headersSent) res.status(500).send('Internal Server Error');
});

/* ------------ Start ------------ */
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
"""

DB_JS = r"""// db.js  (better-sqlite3)
const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.join(__dirname, 'data.sqlite'); // change if you like
const db = new Database(dbPath);

// Example schema bootstrap (idempotent)
db.exec(`
  PRAGMA journal_mode = WAL;

  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    role TEXT NOT NULL,
    password_hash TEXT,
    pin_hash TEXT
  );

  CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES users(id)
  );

  CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT (datetime('now'))
  );

  CREATE TABLE IF NOT EXISTS job_apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    resume TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
  );

  CREATE TABLE IF NOT EXISTS parent_student (
    parent_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    PRIMARY KEY (parent_id, student_id),
    FOREIGN KEY (parent_id) REFERENCES users(id),
    FOREIGN KEY (student_id) REFERENCES users(id)
  );
`);

module.exports = db;
"""

# ---------- main ----------
def main():
    ensure_not_in_storage()

    # 0) quick checks
    if which("node") is None or which("npm") is None:
        print("❌ node or npm not found in PATH. Install them in Termux first:\n"
              "   pkg update && pkg upgrade\n"
              "   pkg install nodejs\n")
        return

    print("✅ node and npm detected.")
    print("📂 Working in:", os.getcwd())

    # 1) remove sqlite3 (ignore errors)
    sh("npm uninstall sqlite3")

    # 2) install better-sqlite3 + other deps
    deps = "better-sqlite3 express ejs body-parser cors express-session dotenv nodemailer"
    sh(f"npm i {deps}")

    # 3) write server.js and db.js (with backups)
    backup_and_write("server.js", SERVER_JS)
    backup_and_write("db.js", DB_JS)

    print("\n🎉 Done!")
    print("Next steps:")
    print("  1) Ensure your routes use the db helper, e.g.:")
    print("       const db = require('../db'); // adjust path")
    print("       const row = db.prepare('SELECT 1 as x').get();")
    print("  2) Start the server:")
    print("       node server.js")
    print("     Then open: http://localhost:3000\n")

if __name__ == "__main__":
    main()
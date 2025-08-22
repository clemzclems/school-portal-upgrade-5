# fix_server.py
# Safely overwrite server.js with a clean, working version (backs up existing file).

import os
from datetime import datetime

SERVER_JS = r"""
// server.js
require('dotenv').config();

const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const session = require('express-session');

// LowDB instance (your ./db.js should export the db object)
let db;
try {
  db = require('./db');
} catch (e) {
  console.warn('⚠️ Could not require ./db. Make sure db.js exists and exports the LowDB instance.');
  db = null;
}

const app = express();

/* ---------- Basics ---------- */
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Simple in-memory session store (fine for dev/testing)
app.use(
  session({
    secret: process.env.SESSION_SECRET || 'dev-session-secret',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 1000 * 60 * 60 } // 1 hour
  })
);

// Static files and views
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Optional globals for EJS
app.locals.siteName = process.env.SITE_NAME || 'School Portal';

/* ---------- Safe route loader ---------- */
function safeRoute(modulePath) {
  try {
    return require(modulePath);
  } catch (err) {
    console.warn(`⚠️ Route "${modulePath}" not found. Mounting a placeholder.`);
    const r = express.Router();
    r.get('/', (_req, res) => {
      res.status(501).send(`Route "${modulePath}" is not implemented yet.`);
    });
    return r;
  }
}

/* ---------- Routes ---------- */
// Each route file should: module.exports = router
const authRoutes       = safeRoute('./src/routes/auth');
const adminRoutes      = safeRoute('./src/routes/admin');
const teacherRoutes    = safeRoute('./src/routes/teacher');
const studentRoutes    = safeRoute('./src/routes/student');
const parentRoutes     = safeRoute('./src/routes/parent');
const employmentRoutes = safeRoute('./src/routes/employment');

// Mount
app.use('/', authRoutes);            // login, logout, reset, etc.
app.use('/admin', adminRoutes);
app.use('/teacher', teacherRoutes);
app.use('/student', studentRoutes);
app.use('/parent', parentRoutes);
app.use('/jobs', employmentRoutes);

// Home page (feel free to change)
app.get('/', async (req, res) => {
  try {
    // Example: ensure db is loaded, show counts (works if LowDB available)
    let stats = null;
    if (db) {
      try {
        await db.read?.();
        const users = db.data?.users || [];
        stats = { userCount: users.length };
      } catch {}
    }
    res.render('index', { user: req.session.user || null, stats });
  } catch (e) {
    console.error('Home render error:', e);
    res.status(500).send('Template error');
  }
});

// Health check
app.get('/health', (_req, res) => res.json({ ok: true }));

/* ---------- 404 & Errors ---------- */
app.use((req, res, next) => {
  if (res.headersSent) return next();
  res.status(404);
  try {
    return res.render('404', { url: req.originalUrl });
  } catch {
    return res.send('404 Not Found');
  }
});

app.use((err, _req, res, _next) => {
  console.error('Unhandled error:', err);
  if (res.headersSent) return;
  res.status(500).send('Internal Server Error');
});

/* ---------- Start ---------- */
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
""".strip() + "\n"

def backup_and_write(path: str, content: str):
    # Make backup if file exists
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{path}.bak-{ts}"
        with open(path, "rb") as rf, open(bak, "wb") as wf:
            wf.write(rf.read())
        print(f"• Backed up existing {os.path.basename(path)} -> {os.path.basename(bak)}")
    # Write new file
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Wrote {path}")

if __name__ == "__main__":
    backup_and_write("server.js", SERVER_JS)
    print("\nNext:")
    print("  1) Ensure ./db.js exists and exports your LowDB instance (you already created it).")
    print("  2) Run: node server.js  (or: npm start)")
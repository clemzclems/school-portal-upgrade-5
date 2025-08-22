# make_server_js.py
# Usage:
#   python make_server_js.py              # writes into current directory
#   python make_server_js.py /path/to/app # writes into given directory
#
# By default, also creates minimal placeholders (routes/views/public)
# so the server can boot. Toggle CREATE_PLACEHOLDERS as needed.

import os
import sys
from datetime import datetime

CREATE_PLACEHOLDERS = False 

SERVER_JS = r"""// server.js
require('dotenv').config();

const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const session = require('express-session');

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

/* ---------- Routes ---------- */
// Each of these files should `module.exports = router`
const authRoutes       = require('./src/routes/auth');
const adminRoutes      = require('./src/routes/admin');
const teacherRoutes    = require('./src/routes/teacher');
const studentRoutes    = require('./src/routes/student');
const parentRoutes     = require('./src/routes/parent');
const employmentRoutes = require('./src/routes/employment');

// Mount
app.use('/', authRoutes);            // login, logout, reset, etc.
app.use('/admin', adminRoutes);
app.use('/teacher', teacherRoutes);
app.use('/student', studentRoutes);
app.use('/parent', parentRoutes);
app.use('/jobs', employmentRoutes);

// Home page (feel free to change)
app.get('/', (req, res) => {
  try {
    res.render('index', { user: req.session.user || null });
  } catch (e) {
    res.status(500).send('Template error');
  }
});

// Health check
app.get('/health', (_req, res) => res.json({ ok: true }));

/* ---------- 404 & Errors ---------- */
app.use((req, res, next) => {
  if (res.headersSent) return next();
  res.status(404);
  // Try to render a 404 page if you have one; fallback to text
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
"""

ROUTE_STUB = """const express = require('express');
const router = express.Router();

// TODO: replace with real handlers
router.get('/', (req, res) => res.send('{name} route OK'));
module.exports = router;
"""

INDEX_EJS = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title><%= siteName || 'School Portal' %></title>
    <link rel="stylesheet" href="/style.css" />
  </head>
  <body>
    <header>
      <h1><%= siteName || 'School Portal' %></h1>
    </header>
    <main>
      <p>Welcome <%= user ? user.name : 'Guest' %>!</p>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/admin">Admin</a></li>
        <li><a href="/teacher">Teacher</a></li>
        <li><a href="/student">Student</a></li>
        <li><a href="/parent">Parent</a></li>
        <li><a href="/jobs">Jobs</a></li>
      </ul>
    </main>
  </body>
</html>
"""

NOT_FOUND_EJS = """<!doctype html>
<html>
  <head><meta charset="utf-8" /><title>404</title></head>
  <body>
    <h1>404 Not Found</h1>
    <p>No page for <code><%= url %></code></p>
    <p><a href="/">Back to Home</a></p>
  </body>
</html>
"""

STYLE_CSS = """body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial,sans-serif;margin:2rem}
h1{margin-bottom:1rem} ul{line-height:1.8}
"""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = f"{path}.bak-{ts}"
        try:
            with open(path, "rb") as rf, open(backup, "wb") as wf:
                wf.write(rf.read())
            print(f"• Backed up existing file to {backup}")
        except Exception as e:
            print(f"! Could not backup {path}: {e}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Wrote {path}")

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    target = os.path.abspath(target)
    print(f"Target directory: {target}")

    # server.js
    write_file(os.path.join(target, "server.js"), SERVER_JS)

    if CREATE_PLACEHOLDERS:
        # routes
        routes_dir = os.path.join(target, "src", "routes")
        for name in ["auth", "admin", "teacher", "student", "parent", "employment"]:
            write_file(os.path.join(routes_dir, f"{name}.js"), ROUTE_STUB.replace("{name}", name))

        # views
        views_dir = os.path.join(target, "views")
        write_file(os.path.join(views_dir, "index.ejs"), INDEX_EJS)
        write_file(os.path.join(views_dir, "404.ejs"), NOT_FOUND_EJS)

        # public
        public_dir = os.path.join(target, "public")
        write_file(os.path.join(public_dir, "style.css"), STYLE_CSS)

    print("\nAll done.")
    print("Next steps:")
    print("  1) Ensure .env has PORT, SITE_NAME, SESSION_SECRET (and email creds if used).")
    print("  2) npm install express express-session body-parser cors ejs dotenv")
    print("  3) npm start")

if __name__ == "__main__":
    main()
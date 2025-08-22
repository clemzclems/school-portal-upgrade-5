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

// === ROUTERS ADDED BY PY SCRIPT ===
const adminRouter = require('./src/routes/admin');
const teacherRouter = require('./src/routes/teacher');
const studentRouter = require('./src/routes/student');
const parentRouter  = require('./src/routes/parent');
const jobsRouter    = require('./src/routes/jobs');
// === END ROUTERS ADDED BY PY SCRIPT ===



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
  console.log(`✅ Server running on http://0.0.0.0:${PORT}`);
});

// === ROUTER MOUNTS ADDED BY PY SCRIPT ===
app.use('/admin', adminRouter);
app.use('/teacher', teacherRouter);
app.use('/student', studentRouter);
app.use('/parent', parentRouter);
app.use('/jobs', jobsRouter);
// === END ROUTER MOUNTS ADDED BY PY SCRIPT ===


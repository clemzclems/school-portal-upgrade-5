# fix_routes.py
# Creates/overwrites src/routes/*.js and safely wires them in server.js

import os, textwrap

PROJECT_ROOT = os.getcwd()
ROUTES_DIR = os.path.join(PROJECT_ROOT, "src", "routes")
SERVER_JS = os.path.join(PROJECT_ROOT, "server.js")

os.makedirs(ROUTES_DIR, exist_ok=True)

routes = [
    ("admin",   "Admin Home",   "Admin"),
    ("teacher", "Teacher Home", "Teacher"),
    ("student", "Student Home", "Student"),
    ("parent",  "Parent Home",  "Parent"),
    ("jobs",    "Jobs",         "Jobs Board"),
]

TEMPLATE = """\
const express = require('express');
const router = express.Router();

router.get('/health', (req, res) => {{
  res.json({{ ok: true, service: '{service}' }});
}});

router.get('/', (req, res) => {{
  res.render('page', {{ title: '{title}', who: '{who}' }});
}});

module.exports = router;
"""

# 1) Write/overwrite each route file
written = []
for fname, title, who in routes:
    js_path = os.path.join(ROUTES_DIR, f"{fname}.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(service=fname, title=title, who=who))
    written.append(js_path)

# 2) Patch server.js to require + mount routers (idempotent)
require_block = """\
// === ROUTERS ADDED BY PY SCRIPT ===
const adminRouter = require('./src/routes/admin');
const teacherRouter = require('./src/routes/teacher');
const studentRouter = require('./src/routes/student');
const parentRouter  = require('./src/routes/parent');
const jobsRouter    = require('./src/routes/jobs');
// === END ROUTERS ADDED BY PY SCRIPT ===
"""

mount_block = """\
// === ROUTER MOUNTS ADDED BY PY SCRIPT ===
app.use('/admin', adminRouter);
app.use('/teacher', teacherRouter);
app.use('/student', studentRouter);
app.use('/parent', parentRouter);
app.use('/jobs', jobsRouter);
// === END ROUTER MOUNTS ADDED BY PY SCRIPT ===
"""

def patch_server_js():
    if not os.path.exists(SERVER_JS):
        print("WARNING: server.js not found; skipping auto-wiring.")
        return

    with open(SERVER_JS, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False

    # Insert require_block after "const app = express();" if not present
    if "ROUTERS ADDED BY PY SCRIPT" not in content:
        key = "const app = express();"
        if key in content:
            idx = content.index(key) + len(key)
            content = content[:idx] + "\n\n" + require_block + "\n" + content[idx:]
            changed = True

    # Insert mount_block before "// Fallback 404" (or append) if not present
    if "ROUTER MOUNTS ADDED BY PY SCRIPT" not in content:
        insert_marker = "// Fallback 404"
        if insert_marker in content:
            idx = content.index(insert_marker)
            content = content[:idx] + mount_block + "\n" + content[idx:]
        else:
            content = content.rstrip() + "\n\n" + mount_block + "\n"
        changed = True

    if changed:
        with open(SERVER_JS, "w", encoding="utf-8") as f:
            f.write(content)
        print("server.js patched: require + mount blocks added.")
    else:
        print("server.js already contains router requires/mounts; no changes made.")

patch_server_js()

print("\nRoutes written:")
for p in written:
    print(" -", os.path.relpath(p, PROJECT_ROOT))

print("\nDone. Now run:\n  npm run dev\n\nThen test:\n  curl http://127.0.0.1:3000/admin/health\n  curl http://127.0.0.1:3000/teacher/health\n  curl http://127.0.0.1:3000/student/health\n  curl http://127.0.0.1:3000/parent/health\n  curl http://127.0.0.1:3000/jobs/health\n")
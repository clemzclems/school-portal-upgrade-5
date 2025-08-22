# create_db_file.py

db_js_code = """\
const path = require('path');
const fs = require('fs');
const { Low, JSONFile } = require('lowdb');

const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

const file = path.join(dataDir, 'db.json');
const adapter = new JSONFile(file);

// Default data structure
const db = new Low(adapter, { users: [], sessions: [], posts: [] });

async function init() {
  await db.read();
  if (!db.data) {
    db.data = { users: [], sessions: [], posts: [] };
    await db.write();
  }
}
init();

module.exports = db;
"""

# Write to db.js (overwrite if exists)
with open("db.js", "w") as f:
    f.write(db_js_code)

print("✅ db.js file has been created/overwritten successfully!")
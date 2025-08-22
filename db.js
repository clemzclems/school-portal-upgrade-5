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

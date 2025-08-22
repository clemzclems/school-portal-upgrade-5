# fix_server.py
code = """\
const express = require('express');
const app = express();

// Health check route
app.get('/health', (req, res) => {
  res.json({
    ok: true,
    ts: new Date().toISOString()
  });
});

const PORT = process.env.PORT || 3000;
const HOST = '0.0.0.0'; // bind to all interfaces

app.listen(PORT, HOST, () => {
  console.log(`Test server up at http://${HOST}:${PORT}`);
});
"""

with open("test_server.js", "w") as f:
    f.write(code)

print("✅ test_server.js has been overwritten successfully.")
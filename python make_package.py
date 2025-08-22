import os
import json

# Package.json content
package_json = {
    "name": "school-portal-upgrade",
    "version": "1.0.0",
    "description": "School portal upgrade project",
    "main": "server.js",
    "scripts": {
        "start": "node server.js",
        "seed": "node seed.js"
    },
    "keywords": [],
    "author": "",
    "license": "ISC",
    "dependencies": {
        "express": "^4.18.2",
        "sqlite3": "^5.1.6",
        "dotenv": "^16.4.5",
        "nodemailer": "^6.9.13",
        "body-parser": "^1.20.2",
        "cors": "^2.8.5",
        "express-session": "^1.17.3"
    }
}

# Save to package.json in current folder
file_path = os.path.join(os.getcwd(), "package.json")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(package_json, f, indent=2)

print(f"✅ package.json generated at: {file_path}")
# env_gen.py
# Writes .env.example and .env safely

import os
from datetime import datetime

def backup_and_write(path: str, content: str):
    if os.path.exists(path):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{path}.bak-{ts}"
        with open(path, "rb") as rf, open(bak, "wb") as wf:
            wf.write(rf.read())
        print(f"• Backed up {path} -> {bak}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Wrote {path}")

# Example template (user edits values)
example_lines = [
"# Example environment variables",
"PORT=3000",
"SITE_NAME=School Portal",
"SESSION_SECRET=replace_with_a_long_random_string",
"",
"# Email (SMTP) settings",
"SMTP_HOST=smtp.gmail.com",
"SMTP_PORT=465",
"SMTP_SECURE=true",
"SMTP_USER=your_email@gmail.com",
"SMTP_PASS=your_app_password_here",
"FROM_EMAIL=School Portal <your_email@gmail.com>",
"",
"# SMS (Twilio optional)",
"TWILIO_ACCOUNT_SID=",
"TWILIO_AUTH_TOKEN=",
"TWILIO_FROM=",
"",
"# Other",
"BASE_URL=http://localhost:3000",
"NODE_ENV=development",
]

# A starter .env (you can change it later)
env_lines = [
"PORT=3000",
"SITE_NAME=School Portal",
"SESSION_SECRET=dev-session-secret",
"SMTP_HOST=smtp.gmail.com",
"SMTP_PORT=465",
"SMTP_SECURE=true",
"SMTP_USER=drclem8@gmail.com",
"SMTP_PASS=your_app_password_here",
"FROM_EMAIL=School Portal <drclem8@gmail.com>",
"BASE_URL=http://localhost:3000",
"NODE_ENV=development",
]

if __name__ == "__main__":
    backup_and_write(".env.example", "\n".join(example_lines) + "\n")
    backup_and_write(".env", "\n".join(env_lines) + "\n")
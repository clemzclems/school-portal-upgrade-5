# fix_host_binding.py

def fix_host_binding(file_path):
    try:
        with open(file_path, "r") as f:
            content = f.read()

        # Replace localhost and 127.0.0.1 with 0.0.0.0
        fixed_content = (
            content.replace("127.0.0.1", "0.0.0.0")
                   .replace("localhost", "0.0.0.0")
        )

        with open(file_path, "w") as f:
            f.write(fixed_content)

        print(f"[✔] Fixed host binding in {file_path}")
        print("Now your server will listen on 0.0.0.0 instead of 127.0.0.1")
    except Exception as e:
        print(f"[✘] Error: {e}")


# Change this path to your server.js file
fix_host_binding("server.js")
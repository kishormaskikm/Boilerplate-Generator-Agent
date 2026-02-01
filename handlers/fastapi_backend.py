import os
def create_fastapi_backend(tool_input: dict):
    project_name = tool_input.get("project_name")

    if not project_name:
        return "❌ project_name required"

    base = os.path.join(os.getcwd(), project_name)

    if os.path.exists(base):
        return "❌ Project already exists"

    folders = [
        "app",
        "app/api",
        "app/core",
        "app/models"
    ]

    for f in folders:
        os.makedirs(os.path.join(base, f), exist_ok=True)

    files = {
        "app/main.py": """\
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
""",
        "requirements.txt": "fastapi\nuvicorn\n",
        "README.md": f"# {project_name}\nFastAPI backend"
    }

    for path, content in files.items():
        with open(os.path.join(base, path), "w") as f:
            f.write(content)

    return f"✅ FastAPI backend '{project_name}' created"

import os
def _create_node_backend(project_name: str):
    if not project_name:
        return "❌ project_name is required"

    base_path = os.path.join(os.getcwd(), project_name)

    if os.path.exists(base_path):
        return f"❌ Project '{project_name}' already exists."

    # ---- folders ----
    folders = [
        "src",
        "src/controllers",
        "src/routes",
        "src/services",
        "src/middlewares",
        "src/utils"
    ]

    for folder in folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

    # ---- files ----
    files = {
        "src/index.js": """\
const express = require("express");
const app = express();

app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
""",

        "package.json": f"""\
{{
  "name": "{project_name}",
  "version": "1.0.0",
  "main": "src/index.js",
  "scripts": {{
    "start": "node src/index.js",
    "dev": "nodemon src/index.js"
  }},
  "dependencies": {{
    "express": "^4.18.2"
  }},
  "devDependencies": {{
    "nodemon": "^3.0.0"
  }}
}}
""",

        ".gitignore": "node_modules\n.env\n",
        ".env.example": "PORT=3000\n",
        "README.md": f"# {project_name}\n\nNode.js backend boilerplate\n"
    }

    for file_path, content in files.items():
        full_path = os.path.join(base_path, file_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    return f"✅ Node.js backend boilerplate '{project_name}' created successfully at {base_path}"


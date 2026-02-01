import os
def create_react_app(tool_input: dict):
    name = tool_input.get("project_name")

    if not name:
        return "❌ project_name required"

    # safe shell usage
    return os.system(f"npm create vite@latest {name} -- --template react")

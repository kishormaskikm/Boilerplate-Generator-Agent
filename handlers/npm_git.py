import os
def npm_install(tool_input: dict):
    path = tool_input.get("path", os.getcwd())
    return os.system(f"cd {path} && npm install")

def git_init(tool_input: dict):
    path = tool_input.get("path", os.getcwd())
    return os.system(f"cd {path} && git init")

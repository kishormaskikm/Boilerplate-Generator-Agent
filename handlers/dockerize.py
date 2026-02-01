
import os


def dockerize_project(tool_input: dict):
    path = tool_input.get("path", os.getcwd())

    dockerfile = """\
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]
"""

    with open(os.path.join(path, "Dockerfile"), "w") as f:
        f.write(dockerfile)

    return "✅ Dockerfile added"

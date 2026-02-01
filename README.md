# Boilerplate-Generator-Agent
The agent will create the boiler plate template code for any project in your system


Project Boilerplate-Generator-Agentt is a backend AI agent that generates project folder structures and boilerplate files based on natural language instructions.

It is designed to automate repetitive project setup tasks such as creating backend templates, initializing files, and preparing a project for development.

---

## What It Does

The agent understands user intent and can:

- Create Node.js backend project structures
- Generate default boilerplate files
- Safely create folders and files using Python
- Route multiple setup actions through a single tool (`run_command`)

Example input: Create a nodejs backend project structure with the name backend

## How It Works

The agent follows a structured loop:

1. **Plan** – Analyzes the user query
2. **Action** – Calls the appropriate command via `run_command`
3. **Observe** – Receives the tool execution result
4. **Output** – Responds with a final message

All filesystem operations are handled programmatically (no unsafe shell commands).

---

## Supported Commands

The agent uses a single tool (`run_command`) as a command router.

Currently supported commands include:

- `create_node_backend`
- `create_fastapi_backend`
- `create_react_app`
- `dockerize_project`
- `npm_install`
- `git_init`

---

## Design Goals

- Keep agent logic simple and deterministic
- Separate reasoning from execution
- Make it easy to add new project templates
- Keep everything backend-only and framework-agnostic

---

## Status

This project currently focuses on backend logic only.  
Frontend or extension integration may be added later.

---

## License
Kishor Maski

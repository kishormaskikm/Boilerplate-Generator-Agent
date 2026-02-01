import json
import requests
from dotenv import load_dotenv
# from langfuse.decorators import observe
from openai import OpenAI
import os

#importing custom handlers
from handlers.node_backend import _create_node_backend
from handlers.fastapi_backend import create_fastapi_backend
from handlers.react_app import create_react_app
from handlers.dockerize import dockerize_project
from handlers.npm_git import npm_install, git_init

load_dotenv()

client = OpenAI()

def run_command(tool_input: dict):
    """
    Unified tool handler.
    tool_input is always a dict from the agent.
    """

    # Case 1: high-level command (agent intent)
    if isinstance(tool_input, dict):
        command = tool_input.get("command")

        if command == "create_node_backend":
            project_name = tool_input.get("project_name")
            return _create_node_backend(tool_input)

        if command == "create_fastapi_backend":
            return create_fastapi_backend(tool_input)

        if command == "create_react_app":
            return create_react_app(tool_input)

        if command == "dockerize_project":
            return dockerize_project(tool_input)

        if command == "npm_install":
            return npm_install(tool_input)

        if command == "git_init":
            return git_init(tool_input)

        # Case 2: raw shell command (optional fallback)
        if "command" in tool_input and isinstance(tool_input["command"], str):
            return os.system(tool_input["command"])

    return "❌ Invalid input to run_command"


def get_weather(city: str):
    print("🔨 Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

avaiable_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    - Every tool must accept ONE argument: a dict

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - run_command: Takes a command as input to execute on system and returns ouput
    
    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

    Example 2:
    User Query: Create a nodejs backend project structure with the name backend-template
    Output: {{ "step": "plan", "content": "The user wants to create a nodejs backend project structure with the name backend-template" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call run_command" }}
    Output: {{ "step": "action", "function": "run_command", "input": {{ "command": "create_node_backend", "project_name": "backend-template" }} }}
    output: {{ "step": "observe", "output": "Project structure created successfully" }}
    Output: {{ "step": "output", "content": "The nodejs backend project structure with the name backend-template has been created successfully." }}

"""

messages = [{"role": "system", "content": system_prompt}]

while True:
    user_query = input("> ")
    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

        if parsed_output.get("step") == "plan":
            print(f"🧠 {parsed_output.get('content')}")
            continue

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if tool_name in avaiable_tools:
                output = avaiable_tools[tool_name]["fn"](tool_input)
                messages.append({
                    "role": "assistant",
                    "content": json.dumps({"step": "observe", "output": output})
                })
                continue

        if parsed_output.get("step") == "output":
            print(f"🤖 {parsed_output.get('content')}")
            break

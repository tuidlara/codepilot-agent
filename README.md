# CodePilot Agent

A lightweight AI agent for developers, built from scratch with Python and Ollama.

CodePilot runs locally and can understand questions about a software project, decide when a tool is needed, execute it, and use the result to answer the user.

## Features

- Local LLM using Qwen3 4B
- Tool calling and agent loop
- Mathematical calculations
- File reading
- Project structure exploration
- Code search
- Multiple tool calls in a single request
- Basic project-wide code analysis

## Tools

**Calculator**  
Evaluates mathematical expressions safely using Python's `ast` module.

**File Reader**  
Reads project files while preventing access outside the project directory.

**Project Explorer**  
Lists project files while ignoring directories such as `.venv`, `.git` and `__pycache__`.

**Code Searcher**  
Searches the project for a term and returns the matching files and lines.

## How It Works

```text
User → Agent → Qwen3 → Tool → Result → Qwen3 → Response
```

The LLM decides which tool is required, while the Agent handles the execution and returns the result to the model.

The agent can also use multiple tools when a request requires more than one step.

## Technology

- Python 3.14
- Ollama
- Qwen3 4B
- Python Ollama client
- Standard Python libraries

No agent framework is used. The tool-calling loop and orchestration were implemented manually.

## Running Locally

Install the dependency:

```bash
pip install ollama
```

Download the model:

```bash
ollama pull qwen3:4b
```

Run the agent:

```bash
python src/main.py
```

## Limitations

CodePilot uses the local `Qwen3 4B` model.

The small model keeps the project lightweight and fully local, but it also limits the quality of its reasoning.

It can sometimes misunderstand requests, choose an unnecessary tool, fail to use a tool when needed, or produce inaccurate results when analyzing larger or more complex codebases.

Because of this, CodePilot is a learning and portfolio project rather than a production-ready coding assistant.

The tools themselves are deterministic Python code. The main limitations come from the LLM's reasoning and tool selection.

## Project Structure

```text
codepilot-agent/
├── src/
│   ├── agent/
│   │   └── agent.py
│   ├── tools/
│   │   ├── calculator.py
│   │   ├── file_reader.py
│   │   ├── project_explorer.py
│   │   └── code_searcher.py
│   └── main.py
├── .gitignore
└── README.md
```

## Purpose

This project was built to understand the fundamentals behind AI agents:

- Tool calling
- Agent orchestration
- Local LLM integration
- Tool execution
- Providing project context to the model

The goal was to build a small, understandable agent from scratch without relying on an agent framework.

## Author

**Arthur de Lara**

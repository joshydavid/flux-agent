# Flux Agent 🌀

`flux-agent` is a sophisticated multi-agent system built using the [Strands Agents SDK](https://strandsagents.com). It features a "write-review-improve" feedback loop and integrates external tools via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io).

## Key Features

- **Multi-Agent Orchestration**: Uses a `GraphBuilder` to coordinate a `writer`, `checker` (quality evaluator), and `finalizer`.
- **Feedback Loops**: Implements a cycle where content is written, checked, and sent back for revision if it doesn't meet quality standards.
- **MCP Integration**: The `writer` agent can use external tools like `mcp-server-fetch` to retrieve real-time information from the web.
- **Modular Tooling**: Tools are abstracted into a dedicated `app/tools` directory for easy extensibility.
- **Ollama Integration**: Runs locally using Ollama (defaulting to `llama3.1:latest`).

## Architecture

- **`app/workflow.py`**: Defines the graph structure, node transitions, and agent roles.
- **`app/quality_checker.py`**: A custom multi-agent node that determines if content is ready for finalization or needs another iteration.
- **`app/tools/`**:
  - `web_tools.py`: Manages the MCP connection to the fetch server.
  - `__init__.py`: Provides a central registry for all available tools.
- **`app/runner.py`**: A CLI interface for interacting with the workflow.

## Getting Started

### Prerequisites

1.  **Ollama**: Ensure Ollama is installed and running with `llama3.1` pulled:
    ```bash
    ollama pull llama3.1
    ```
2.  **uv**: This project uses `uv` for lightning-fast Python package management. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).

### Installation

Clone the repository and install dependencies:

```bash
uv sync
```

### Running the Demo

Launch the interactive CLI:

```bash
uv run main.py
```

### Demo Options

- **`demo`**: Generates a haiku about programming loops (standard workflow test).
- **`tool`**: Fetches content from a URL and summarizes it (MCP tool test).
- **`exit`**: Gracefully close the application.

## How it Works (MCP Tooling)

The `writer` agent is equipped with an `MCPClient`. When you ask for web content, the agent automatically:

1.  Connects to the `mcp-server-fetch` via `uvx`.
2.  Calls the `fetch` tool with the provided URL.
3.  Receives the content and incorporates it into the response.
4.  Sends the draft to the `checker` to start the review loop.

## License

MIT

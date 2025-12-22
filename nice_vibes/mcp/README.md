# NiceVibes MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that gives AI assistants direct access to NiceGUI documentation, source code, and visual debugging capabilities.

## Why Use This?

While the static prompts work great for most tasks, the MCP server provides **dynamic, on-demand access** to:

- **Project Setup** - Generate complete project structures (`single_page` or `spa`) with all files, editor rules, and best practices
- **Documentation Search** - Find relevant topics without loading everything into context
- **Source Code Inspection** - Read NiceGUI component source code directly from the installed package
- **Visual Debugging** - Capture screenshots (JPEG/PNG) of running applications
- **Sample Exploration** - Browse and copy working sample applications

## Capabilities

### 📚 Documentation Access

| Tool | Purpose |
|------|---------|
| `list_topics` | Browse all available documentation topics by category (mechanics, events, classes, samples) |
| `get_topic` | Retrieve detailed documentation for a specific topic |
| `search_topics` | Find topics matching a keyword across names, summaries, and tags |

### 🔍 Component Inspection

| Tool | Purpose |
|------|---------|
| `get_component_info` | Get comprehensive info: inheritance chain, documentation URLs, GitHub source links, and optionally full source code |
| `get_component_source` | Read component source directly from the installed NiceGUI package (fast, no network) |
| `get_component_docs` | Fetch official NiceGUI documentation with examples (downloaded and cached locally) |

### 🖼️ Visual Debugging

| Tool | Purpose |
|------|---------|
| `capture_url_screenshot` | Capture a screenshot of any URL (default: localhost:8080). Supports `format` (JPEG/PNG) and `quality` (1-100) options. |
| `kill_port_8080` | Kill any process on port 8080 - useful when restarting apps |
| `open_browser` | Open a URL in the user's default browser (default: http://localhost:8080) |

**Note:** Screenshots default to JPEG at 85% quality to reduce file size. Use `format: "PNG"` for lossless quality when needed.

### 📦 Sample Applications

| Tool | Purpose |
|------|---------|
| `list_samples` | List all available sample applications with descriptions and tags |
| `get_sample_source` | Get the source code of any file in a sample application |

### 🚀 Project Creation

| Tool | Purpose |
|------|---------|
| `project_setup` | Generate complete project structure with all files and folders. Returns JSON with paths and content - never overwrites existing files. Supports `single_page` and `spa` project types. |
| `get_project_creation_guide` | Get the guided questionnaire and rules for creating new NiceGUI projects |

**Project creation workflow:**
1. Use `project_setup` to get file/folder structure for new projects
2. Create files from the returned JSON (check for existing files first)
3. Run `poetry install` to install dependencies
4. Use `poetry run python -m {package}.main` to start the app
5. Use `capture_url_screenshot` to verify the UI renders correctly
6. Code changes are automatically hot-reloaded - no restart needed

## Setup

### 1. Get Your Configuration

Run this command to get the MCP configuration for your system:

```bash
nice-vibes mcp-config
```

This outputs something like:

```json
{
  "mcpServers": {
    "nice-vibes": {
      "command": "/path/to/python",
      "args": ["-m", "nice_vibes.mcp"]
    }
  }
}
```

### 2. Add to Your MCP Client

Copy the configuration to your MCP client's config file:

| Client | Config File Location |
|--------|---------------------|
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) |

#### Windsurf MCP Configuration

In Windsurf, you can access the MCP configuration via the Cascade panel:

![Windsurf MCP Server Configuration](media/windsurf_mcp_server.png)

#### Example with Multiple MCP Servers

Here's an example configuration combining nice-vibes with other popular MCP servers:

```json
{
  "mcpServers": {
    "github-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    },
    "mongodb-mcp-server": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server"],
      "env": {
        "MDB_MCP_CONNECTION_STRING": "mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority"
      }
    },
    "nice-vibes": {
      "command": "/Users/michael/Library/Caches/pypoetry/virtualenvs/nice-vibes-C_JF_RUt-py3.13/bin/python",
      "args": ["-m", "nice_vibes.mcp"]
    }
  }
}
```

### 3. Restart Your Client

Restart your AI assistant to load the new MCP server.

## Usage Examples

Once configured, your AI assistant can use these tools naturally:

### Finding Documentation

> "What documentation do you have about authentication?"

The AI will use `search_topics` to find relevant topics like `authentication`, `sub_pages`, etc.

### Understanding a Component

> "How does ui.table work internally?"

The AI will use `get_component_info` or `get_component_source` to read the actual implementation.

### Visual Debugging

> "My app at localhost:8080 looks wrong, can you see what's happening?"

The AI will use `capture_url_screenshot` to take a screenshot and analyze the visual output.

**Note:** Screenshots are automatically opened in your browser since some MCP clients (like Windsurf) cannot display images inline. The screenshot is saved to a temp directory and displayed in a styled HTML page.

### Learning from Samples

> "Show me how the dashboard sample handles charts"

The AI will use `get_sample_source` to read the relevant code from the dashboard sample.

### Creating a New Project

> "Help me create a new NiceGUI dashboard"

The AI will use `get_project_creation_guide` and guide you through questions about project type, complexity, page structure, and styling. After generating the code, it will use `capture_app_screenshot` to preview the design and ask for your feedback. Once approved, it starts the server and uses `open_browser` to open the app in your browser.

## Testing

You can test the MCP server interactively:

```bash
nice-vibes-mcp-test
```

This starts an interactive CLI where you can call tools manually:

```
> tools
Available tools (10):
  - list_topics
  - get_topic
  - search_topics
  ...

> call get_component_docs
  component: ui.button

# Documentation: button
...
```

## Architecture

```
nice_vibes/mcp/
├── __init__.py      # Package exports
├── __main__.py      # Entry point for python -m nice_vibes.mcp
├── server.py        # MCP server implementation
├── test_client.py   # Interactive test client
└── README.md        # This file
```

The server uses:
- **stdio transport** - Communicates via stdin/stdout JSON-RPC
- **Local caching** - Downloaded documentation is cached in `.cache/docs/`
- **Selenium** - For screenshot capture (requires Chrome/Chromium)

## Requirements

- Python 3.12+
- NiceGUI (installed)
- Chrome/Chromium (for screenshot features)
- `mcp` package (installed automatically with nice-vibes)

## Troubleshooting

### Server doesn't start

Make sure you're using the correct Python environment:

```bash
poetry run nice-vibes mcp-config
```

Use the exact path shown in the output.

### Screenshots fail

Ensure Chrome or Chromium is installed. The server uses headless Chrome via Selenium.

### Documentation fetch fails

Some components may not have dedicated documentation pages. The server will show an error with the attempted URL.

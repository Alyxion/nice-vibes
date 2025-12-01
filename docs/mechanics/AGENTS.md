# Project Rules for AI Agents

This project was created with [NiceGUI](https://nicegui.io/) using the [NiceVibes MCP server](https://github.com/Alyxion/nice-vibes).

## Framework & Tools

- **Framework:** NiceGUI - Python web UI framework
- **Package Manager:** Poetry
- **Default Port:** 8080

## Master Prompts

For comprehensive NiceGUI knowledge, load one of these master prompts:

| Variant | Tokens | Best For |
|---------|--------|----------|
| **Compact** | ~14K | Simple UIs, quick tasks |
| **Optimum** | ~23K | Most projects (recommended) |
| **Extended** | ~34K | Advanced: custom JS/Vue, 3D, deployment |

URLs:
- Compact: `https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_compact.md`
- Optimum: `https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes.md`
- Extended: `https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_extended.md`

## Running This Project

```bash
# Install dependencies
poetry install

# Run the application
poetry run python main.py
```

Always use `poetry run` - never plain `python main.py`.

## Development Rules

### Hot Reload
Once the server is running, code changes are **automatically hot-reloaded**. No need to restart the server.

### Port 8080
This project runs on port 8080. Never change the port. If the port is blocked, kill the existing process first.

### Browser
Never open a browser automatically without asking the user first.

### MCP Tools

If the nice-vibes MCP server is available, use the MCP tools provided by the NiceVibes MCP server to access documentation, source code, and visual debugging capabilities. It allows you to look up visual elements,
mechanics, events, classes, and samples.
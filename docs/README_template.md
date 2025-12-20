<p align="center">
  <img src="{{ASSETS_PREFIX}}assets/logo.png" alt="Nice Vibes Logo" width="300">
</p>

<p align="center">
  <strong>Nice Vibes - Teach AI agents to build beautiful NiceGUI applications</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python 3.12+"></a>
  <a href="https://nicegui.io/"><img src="https://img.shields.io/badge/NiceGUI-3.3+-green.svg" alt="NiceGUI"></a>
  <a href="{{GITHUB_PREFIX}}LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

<p align="center">
  <img src="{{ASSETS_PREFIX}}samples/showcase.gif" alt="Sample Applications"{{SHOWCASE_WIDTH}}>
</p>

A comprehensive toolkit of prompts, patterns, and examples that help AI coding assistants generate correct, idiomatic [NiceGUI](https://nicegui.io/) code.

## ✨ Features

- **📚 Complete Documentation** - Events, mechanics, styling, and class references
- **🔐 Authentication Patterns** - Signed cookie persistence, role-based permissions, login flows
- **🧭 SPA Navigation** - `ui.sub_pages`, header/drawer visibility, back button handling
- **🧪 Working Samples** - Full multi-dashboard app, stock analysis, custom components
- **🤖 AI-Optimized** - Single master prompt (~23K tokens) for context injection
- **✅ Validated** - All class references and URLs verified
- **🧩 Modular** - Pick what you need or use the full prompt

## 🚀 Quick Start

### Use Pre-Built Prompts (Recommended)

Just download and use the pre-built master prompt directly:

| Variant | Tokens | Use Case | Download |
|---------|--------|----------|----------|
| **Compact** | ~14K | Quick tasks, simple UI | [nice_vibes_compact.md](https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_compact.md) |
| **Optimum** | ~23K | Most use cases | [nice_vibes.md](https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes.md) |
| **Extended** | ~34K | Custom components, deployment | [nice_vibes_extended.md](https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_extended.md) |

When using tools such as [Windsurf](https://www.windsurf.com/) or [Claude Code](https://claude.ai/code), point it to the master prompt of your choice before providing the task description.

Choose of one the urls above depending on the complexity of the task.

Alternatively, you can add the global and local rules below to your tool of choice to let it fetch the corresponding master prompt automatically.

### Build From Source (Optional)

Only needed if you want to customize or extend the documentation:

```bash
git clone https://github.com/Alyxion/nice-vibes.git
cd nice-vibes
poetry install
poetry run python scripts/build_master_prompt.py
```

## 📋 Requirements

For building from source:
- Python 3.12+
- Poetry

## 📖 Documentation

| Folder | Description |
|--------|-------------|
| [docs/]({{DOCS_PREFIX}}docs{{DOCS_SUFFIX}}) | Main documentation |
| [docs/events/]({{DOCS_PREFIX}}docs/events{{DOCS_SUFFIX}}) | Event handling patterns |
| [docs/mechanics/]({{DOCS_PREFIX}}docs/mechanics{{DOCS_SUFFIX}}) | Core patterns (SPA, authentication, styling) |
| [docs/classes/]({{DOCS_PREFIX}}docs/classes{{DOCS_SUFFIX}}) | UI element reference by category |

## 📂 Other Folders

| Folder | Description |
|--------|-------------|
| [samples/]({{DOCS_PREFIX}}samples{{DOCS_SUFFIX}}) | Working example applications |
| [output/]({{DOCS_PREFIX}}output{{DOCS_SUFFIX}}) | Generated master prompts |
| [scripts/]({{DOCS_PREFIX}}scripts{{DOCS_SUFFIX}}) | Build and validation tools |
| [tests/]({{DOCS_PREFIX}}tests{{DOCS_SUFFIX}}) | Example NiceGUI tests |

## 🧪 Testing

```bash
poetry run pytest -v
```

## 🤖 Prompt Variants

Each variant is available in **online** (GitHub URLs) and **offline** (local paths) versions:

| Content | Compact | Optimum | Extended |
|---------|:-------:|:-------:|:--------:|
| Main guide | ✓ | ✓ | ✓ |
| Core mechanics | ✓ | ✓ | ✓ |
| Events | ref | ✓ | ✓ |
| Class reference | ref | ✓ | ✓ |
| Custom components | ref | ref | ✓ |
| Configuration & deployment | ref | ref | ✓ |
| Testing | ✓ | ✓ | ✓ |
| Sample references | ✓ | ✓ | ✓ |

**ref** = Not included but referenced with summary (AI knows where to look)

Configure file order and summaries in `docs/prompt_config.yaml`.

## 🖥️ Command Line Interface

Nice Vibes includes a CLI to explore and run sample applications:

```bash
# Install the package
pip install nice-vibes

# Interactive sample selector
nice-vibes

# List available samples
nice-vibes list

# Run a sample
nice-vibes run dashboard

# Copy sample source code to current directory
nice-vibes copy dashboard
nice-vibes copy video_custom_component -o my_video_app
```

<p align="center">
  <img src="{{ASSETS_PREFIX}}assets/cli_preview.png" alt="CLI Preview" width="600">
</p>

## 🔌 MCP Server (Optional)

NiceVibes includes an optional [Model Context Protocol](https://modelcontextprotocol.io/) server that gives AI assistants dynamic access to:

- **Guided project creation** - Step-by-step questionnaire with best practices
- **Documentation search** - Find topics without loading everything into context
- **Source code inspection** - Read NiceGUI component source directly
- **Visual debugging** - Capture screenshots of running or newly created applications
- **Sample exploration** - Browse and copy working examples

Get your configuration with `nice-vibes mcp-config`:

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

Add this to your MCP client config ([Windsurf](https://www.windsurf.com/), [Claude Desktop](https://claude.ai/desktop), etc.).

This is how it works:

<p align="center">
  <img src="{{ASSETS_PREFIX}}assets/mcp_sample.png" alt="MCP Sample" width="600">
</p>

See [nice_vibes/mcp/README.md]({{DOCS_PREFIX}}nice_vibes/mcp/README.md{{DOCS_SUFFIX}}) for detailed setup instructions.

## 🧠 Recommended Editor Rules (Windsurf / Claude Code)

Use the snippets below as **Global Rules / Global Instructions** and **Local Rules / Local Instructions**.

### Version A (recommended): MCP-enabled

#### Global (copy/paste)

```text
When I ask you to build a new Python dashboard or web UI, default to NiceGUI and Poetry (Python 3.12+).
Assume the app runs on http://localhost:8080. If the nice-vibes MCP server is available, you can refer
to it for sample apps and initial project setup.
```

#### Local (copy/paste)

```text
This repository uses NiceGUI and Poetry.

Rules:
- Always use `poetry run ...`.
- Keep NiceGUI on port 8080. If the port is blocked you can kill the process using nice-vibes MCP tools.
- NiceGUI hot-reloads on file-changes, you do usually not need to restart the server.
- Do not open a browser automatically.
- Prefer the nice-vibes MCP tools for docs, samples, and NiceGUI component details.
- If you want to verify visual impact of your changes you can use the nice-vibes MCP tools to capture screenshots using `capture_url_screenshot` (defaults to http://localhost:8080).
```

### Version B: No MCP (GitHub markdown only)

#### Global (copy/paste)

```text
When I ask you to build a new Python dashboard or web UI, default to NiceGUI and Poetry (Python 3.12+).
For documentation, samples, and NiceGUI component details use the Nice Vibes GitHub markdown prompts.
They are available in the following variants:
- https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_compact.md
- https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes.md
- https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_extended.md
```

#### Local (copy/paste)

```text
This repository uses NiceGUI and Poetry.

Rules:
- Always use `poetry run ...`.
- Keep NiceGUI on port 8080. Do not open a browser automatically.
- Use the Nice Vibes GitHub markdown prompts as your primary reference for NiceGUI component details.
- NiceGUI hot-reloads on file-changes, you do usually not need to restart the server.
```

## 🙏 Credits

Created by **Michael Ikemann**

[![GitHub](https://img.shields.io/badge/GitHub-Alyxion-181717?logo=github)](https://github.com/Alyxion)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Michael_Ikemann-0A66C2?logo=linkedin)](https://www.linkedin.com/in/michael-ikemann/)

Built for use with [NiceGUI](https://nicegui.io/) - a Python UI framework by [Zauberzeug](https://github.com/zauberzeug/nicegui).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE]({{GITHUB_PREFIX}}LICENSE) file for details.

Free to use, modify, and distribute.

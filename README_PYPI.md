<p align="center">
  <img src="https://raw.githubusercontent.com/Alyxion/nice-vibes/main/assets/logo.png" alt="Nice Vibes Logo" width="300">
</p>

<p align="center">
  <strong>Nice Vibes - Teach AI agents to build beautiful NiceGUI applications</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python 3.12+"></a>
  <a href="https://nicegui.io/"><img src="https://img.shields.io/badge/NiceGUI-3.3+-green.svg" alt="NiceGUI"></a>
  <a href="https://github.com/Alyxion/nice-vibes/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Alyxion/nice-vibes/main/samples/showcase.gif" alt="Sample Applications" width="600">
</p>

A comprehensive toolkit of prompts, patterns, and examples that help AI coding assistants generate correct, idiomatic [NiceGUI](https://nicegui.io/) code.

## ✨ Features

- **📚 Complete Documentation** - Events, mechanics, styling, and class references
- **🔐 Authentication Patterns** - Signed cookie persistence, role-based permissions, login flows
- **🧭 SPA Navigation** - `ui.sub_pages`, header/drawer visibility, back button handling
- **🧪 Working Samples** - Full multi-dashboard app, stock analysis, custom components
- **🤖 AI-Optimized** - Single master prompt (~22K tokens) for context injection
- **✅ Validated** - All class references and URLs verified
- **🧩 Modular** - Pick what you need or use the full prompt

## 🚀 Quick Start

### Use Pre-Built Prompts (Recommended)

Just download and use the pre-built master prompt directly:

| Variant | Tokens | Use Case | Download |
|---------|--------|----------|----------|
| **Compact** | ~14K | Quick tasks, simple UI | [nice_vibes_compact.md](https://github.com/Alyxion/nice-vibes/blob/main/output/nice_vibes_compact.md) |
| **Optimum** | ~23K | Most use cases | [nice_vibes.md](https://github.com/Alyxion/nice-vibes/blob/main/output/nice_vibes.md) |
| **Extended** | ~34K | Custom components, deployment | [nice_vibes_extended.md](https://github.com/Alyxion/nice-vibes/blob/main/output/nice_vibes_extended.md) |

Copy the content into your AI assistant's context or system prompt.

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
| [docs/](https://github.com/Alyxion/nice-vibes/tree/main/docs) | Main documentation |
| [docs/events/](https://github.com/Alyxion/nice-vibes/tree/main/docs/events) | Event handling patterns |
| [docs/mechanics/](https://github.com/Alyxion/nice-vibes/tree/main/docs/mechanics) | Core patterns (SPA, authentication, styling) |
| [docs/classes/](https://github.com/Alyxion/nice-vibes/tree/main/docs/classes) | UI element reference by category |

## 📂 Other Folders

| Folder | Description |
|--------|-------------|
| [samples/](https://github.com/Alyxion/nice-vibes/tree/main/samples) | Working example applications |
| [output/](https://github.com/Alyxion/nice-vibes/tree/main/output) | Generated master prompts |
| [scripts/](https://github.com/Alyxion/nice-vibes/tree/main/scripts) | Build and validation tools |
| [tests/](https://github.com/Alyxion/nice-vibes/tree/main/tests) | Example NiceGUI tests |

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
| Sample references | ✓ | ✓ | ✓ |

**ref** = Not included but referenced with summary (AI knows where to look)

Configure file order and summaries in `docs/prompt_config.yaml`.

## ✅ Validation

```bash
# Validate class references
poetry run python scripts/validate_classes.py

# Also check URLs
poetry run python scripts/validate_classes.py --check-urls
```

## 🙏 Credits

Created by **Michael Ikemann**

[![GitHub](https://img.shields.io/badge/GitHub-Alyxion-181717?logo=github)](https://github.com/Alyxion)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Michael_Ikemann-0A66C2?logo=linkedin)](https://www.linkedin.com/in/michael-ikemann/)

Built for use with [NiceGUI](https://nicegui.io/) - a Python UI framework by [Zauberzeug](https://github.com/zauberzeug/nicegui).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Alyxion/nice-vibes/blob/main/LICENSE) file for details.

Free to use, modify, and distribute.

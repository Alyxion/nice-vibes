# 🎯 Nice Prompt

> **Teach AI agents to build beautiful NiceGUI applications**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![NiceGUI](https://img.shields.io/badge/NiceGUI-3.3+-green.svg)](https://nicegui.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive toolkit of prompts, patterns, and examples that help AI coding assistants generate correct, idiomatic [NiceGUI](https://nicegui.io/) code.

## ✨ Features

- **📚 Complete Documentation** - Events, mechanics, styling, and class references
- **🧪 Working Samples** - Ready-to-run example applications
- **🤖 AI-Optimized** - Single master prompt (~18K tokens) for context injection
- **✅ Validated** - All class references and URLs verified
- **🧩 Modular** - Pick what you need or use the full prompt

## 🚀 Quick Start

```bash
# Install dependencies
poetry install

# Build the master prompt for AI agents
poetry run python scripts/build_master_prompt.py
```

## 📋 Requirements

- Python 3.12+
- NiceGUI 3.3+

## 📁 Project Structure

```
nice-prompt/
├── README.md                 # This file
├── project_rules.md          # Rules & guidelines for AI agents
├── pyproject.toml            # Poetry configuration
├── docs/
│   ├── nicegui_prompt.md     # Main AI agent guide
│   ├── events/               # Event handling
│   │   ├── element_events.md
│   │   ├── value_events.md
│   │   ├── button_events.md
│   │   ├── keyboard_events.md
│   │   ├── lifecycle_events.md
│   │   └── upload_events.md
│   ├── mechanics/            # Core patterns
│   │   ├── application_structure.md
│   │   ├── pages.md
│   │   ├── container_updates.md
│   │   ├── event_binding.md
│   │   ├── binding_and_state.md
│   │   ├── data_modeling.md
│   │   └── styling.md
│   ├── classes/              # Class reference by category
│   │   ├── text_elements.md
│   │   ├── controls.md
│   │   ├── audiovisual.md
│   │   ├── data_elements.md
│   │   ├── layout.md
│   │   ├── app_and_config.md
│   │   ├── utilities.md
│   │   └── *_references.md   # Source & doc URLs for each category
│   └── prompt_config.yaml    # Master prompt build configuration
├── output/
│   └── nice_prompt.md        # Generated master prompt
├── tests/
│   ├── conftest.py           # Pytest configuration
│   ├── main.py               # Minimal app for testing
│   └── test_basic.py         # Example NiceGUI tests
├── samples/
│   ├── dashboard/            # Sales dashboard sample
│   │   ├── main.py
│   │   └── README.md
│   └── stock_peers/          # Stock peer analysis sample
│       ├── main.py
│       └── README.md
└── scripts/
    ├── validate_classes.py           # Validate class references & URLs
    ├── generate_class_references.py  # Generate reference files
    └── build_master_prompt.py        # Build single-file master prompt
```

## 📖 Documentation

- [NiceGUI Prompt Guide](docs/nicegui_prompt.md) - Main guide for AI agents
- [Project Rules](project_rules.md) - Rules & guardrails for code generation
- [Events](docs/events/) - Event handling:
  - [Element Events](docs/events/element_events.md)
  - [Value Events](docs/events/value_events.md)
  - [Button Events](docs/events/button_events.md)
  - [Keyboard Events](docs/events/keyboard_events.md)
  - [Lifecycle Events](docs/events/lifecycle_events.md)
  - [Upload Events](docs/events/upload_events.md)
- [Mechanics](docs/mechanics/) - Core patterns and concepts:
  - [Application Structure](docs/mechanics/application_structure.md)
  - [Pages & Routing](docs/mechanics/pages.md)
  - [Container Updates](docs/mechanics/container_updates.md)
  - [Event Binding](docs/mechanics/event_binding.md)
  - [Binding & State](docs/mechanics/binding_and_state.md)
  - [Data Modeling](docs/mechanics/data_modeling.md)
  - [Styling](docs/mechanics/styling.md)
- [Class Reference](docs/classes/) - Detailed documentation by category:
  - [Text Elements](docs/classes/text_elements.md)
  - [Controls](docs/classes/controls.md)
  - [Audiovisual](docs/classes/audiovisual.md)
  - [Data Elements](docs/classes/data_elements.md)
  - [Layout](docs/classes/layout.md)
  - [App & Config](docs/classes/app_and_config.md)
  - [Utilities](docs/classes/utilities.md)

## 🧪 Testing

```bash
poetry run pytest -v
```

## 🤖 Build Master Prompt

Generate master prompt files for AI context injection:

```bash
poetry run python scripts/build_master_prompt.py
```

### Prompt Variants

Each variant is generated in **online** and **offline** versions:
- **Online**: References GitHub URLs for excluded docs
- **Offline** (`*_offline.md`): References local file paths

| Variant | Tokens | Use Case | Online | Offline |
|---------|--------|----------|--------|---------|
| Compact | ~9K | Quick tasks, simple UI | [nice_prompt_compact.md](output/nice_prompt_compact.md) | [nice_prompt_compact_offline.md](output/nice_prompt_compact_offline.md) |
| Optimum | ~18K | Most use cases | [nice_prompt.md](output/nice_prompt.md) | [nice_prompt_offline.md](output/nice_prompt_offline.md) |
| Extended | ~23K | Custom components, deployment | [nice_prompt_extended.md](output/nice_prompt_extended.md) | [nice_prompt_extended_offline.md](output/nice_prompt_extended_offline.md) |

### What's Included

| Content | Compact | Optimum | Extended |
|---------|:-------:|:-------:|:--------:|
| Main guide | ✓ | ✓ | ✓ |
| Core mechanics | ✓ | ✓ | ✓ |
| Events | ref | ✓ | ✓ |
| Class reference | ref | ✓ | ✓ |
| Custom components | ref | ref | ✓ |
| Configuration & deployment | ref | ref | ✓ |

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

Created by [Michael Ikemann](https://github.com/Alyxion).

Built for use with [NiceGUI](https://nicegui.io/) - a Python UI framework by [Zauberzeug](https://github.com/zauberzeug/nicegui).

## 📄 License

MIT

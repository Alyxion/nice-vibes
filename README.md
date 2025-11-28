# Nice Prompt

A toolkit to help AI agents build working [NiceGUI](https://nicegui.io/) applications.

## Overview

NiceGUI is a Python-based UI framework that lets you build web applications with ease. This project provides prompts, examples, and guidance to help AI coding assistants generate correct, idiomatic NiceGUI code.

## Installation

```bash
poetry install
```

## Requirements

- Python 3.12+
- NiceGUI 3.3+

## Project Structure

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
│   │   └── binding_and_state.md
│   └── classes/              # Class reference by category
│       ├── text_elements.md
│       ├── controls.md
│       ├── audiovisual.md
│       ├── data_elements.md
│       ├── layout.md
│       ├── app_and_config.md
│       ├── utilities.md
│       └── *_references.md   # Source & doc URLs for each category
└── scripts/
    ├── validate_classes.py       # Validate class references & URLs
    └── generate_class_references.py  # Generate reference files
```

## Documentation

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
- [Class Reference](docs/classes/) - Detailed documentation by category:
  - [Text Elements](docs/classes/text_elements.md)
  - [Controls](docs/classes/controls.md)
  - [Audiovisual](docs/classes/audiovisual.md)
  - [Data Elements](docs/classes/data_elements.md)
  - [Layout](docs/classes/layout.md)
  - [App & Config](docs/classes/app_and_config.md)
  - [Utilities](docs/classes/utilities.md)

## Validation

```bash
# Validate class references (fast)
poetry run python scripts/validate_classes.py

# Also check URLs (slower)
poetry run python scripts/validate_classes.py --check-urls

# Retry failed URLs only
poetry run python scripts/validate_classes.py --retry-failed
```

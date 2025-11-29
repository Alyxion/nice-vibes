# Nice Prompt - Project Rules

Rules for AI agents (like Cascade) working on this repository.

This file is **not** part of the master prompt. It governs how to maintain and extend the documentation and samples in this project.

---

## Project Overview

This repository contains documentation and examples to help AI agents generate correct NiceGUI code. The main output is `output/nice_prompt.md` - a single file containing all documentation for context injection.

## File Organization

```
docs/
├── nicegui_prompt.md       # Main guide (always first in master prompt)
├── mechanics/              # Core patterns (application structure, pages, etc.)
├── events/                 # Event handling documentation
├── classes/                # UI element reference by category
│   ├── *.md                # Class docs (included in master prompt)
│   └── *_references.md     # Source URLs (excluded from master prompt)
└── prompt_config.yaml      # Controls master prompt build order

samples/                    # Working example applications
scripts/                    # Build and validation tools
output/                     # Generated master prompt
```

## Maintenance Rules

### When Adding Documentation

1. Add new files to the appropriate `docs/` subdirectory
2. Update `docs/prompt_config.yaml` to include the file in the correct order
3. Rebuild the master prompt: `poetry run python scripts/build_master_prompt.py`

### When Modifying Class References

1. Edit the class file in `docs/classes/`
2. Regenerate reference files: `poetry run python scripts/generate_class_references.py`
3. Validate: `poetry run python scripts/validate_classes.py`

### When Adding Samples

- Keep samples as **single files** for easy reference
- Each sample should demonstrate specific patterns
- Include comments explaining the patterns used
- Always use `ui.run(show=False, title='...')` in the main guard

### Keep README.md Current

Update `README.md` when:
- Adding new files or directories
- Changing project structure
- Adding new scripts or tools

### Keep nicegui_prompt.md Current

Update `docs/nicegui_prompt.md` when:
- Adding new documentation sections
- Documenting new patterns or mechanics
- Adding important rules or gotchas

## Master Prompt Build

The master prompt is built from all documentation files in the order specified by `docs/prompt_config.yaml`.

### Configuration

Edit `docs/prompt_config.yaml` to control:
- **File order** - Priority order for each section
- **Exclusions** - Files to skip (e.g., `*_references.md`)

### Building

```bash
poetry run python scripts/build_master_prompt.py
```

Options:
- `--github-url URL` - Set GitHub URL for source links (default: https://github.com/Alyxion/nice-prompt)

## Validation

Run before committing:

```bash
# Validate class references
poetry run python scripts/validate_classes.py

# Also check URLs
poetry run python scripts/validate_classes.py --check-urls
```

## Class Reference Structure

Each class category file has a corresponding `*_references.md` with:
- **Description** - What the class does
- **Inherits** - Base class chain (important for event handling)
- **Source** - Link to GitHub source code
- **Documentation** - Link to nicegui.io docs

### Important Base Classes

Track these in the Inherits column:
- `ui.element` - Base for all UI elements
- `ValueElement` - Elements with `.value` and `on_change`
- `DisableableElement` - Elements that can be disabled
- `ContentElement` - Elements with text/HTML content
- `SourceElement` - Elements with source (images, audio, video)
- `ChoiceElement` - Selection elements (radio, select, toggle)
- `ValidationElement` - Input elements with validation

## NiceGUI Code Conventions

When writing samples or examples, follow these patterns:

### Main Guard

```python
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False, title='My App')
```

### Per-User Data

Never use global variables. Use `app.storage.client`:

```python
@dataclass
class UserData:
    name: str = ''
    
    @classmethod
    def get_current(cls) -> 'UserData':
        if 'user_data' not in app.storage.client:
            app.storage.client['user_data'] = cls()
        return app.storage.client['user_data']
```

### Container Updates

```python
container.clear()
with container:
    ui.label('New content')
```

Or use `@ui.refreshable` for simpler cases.

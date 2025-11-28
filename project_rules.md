# NiceGUI Project Rules & Guidelines

Rules and guardrails for AI agents generating NiceGUI code.

## Application Structure

### Main Guard (Critical)

Always wrap `ui.run()` with the multiprocessing guard:

```python
if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```

**Why both checks?**
- `__main__` - Normal script execution
- `__mp_main__` - Multiprocessing spawn context (used on macOS/Windows)

Without this guard:
- Worker processes would start their own servers
- Importing the module would start the server
- Test frameworks would trigger `ui.run()`
- Hot reload would create duplicate servers

## Container Updates

To update the content of a NiceGUI container element:

1. Call the container's `.clear()` method
2. Enter its context via `with`
3. Create new elements inside the context

```python
container = ui.column()

def update_content():
    container.clear()
    with container:
        ui.label('New content!')
```

**Alternative**: Use `@ui.refreshable` for simpler cases:

```python
@ui.refreshable
def content():
    ui.label('Content')

content()
content.refresh()  # Rebuilds automatically
```

## Pages

- Use `@ui.page('/path')` decorator to define routes
- Each page function builds UI when visited
- Elements created outside `@ui.page` go to the auto-index page at `/`

```python
@ui.page('/')
def index():
    ui.label('Home')

@ui.page('/about')
def about():
    ui.label('About')
```

## Project Structure

Recommended layout for larger applications:

```
my_app/
├── main.py              # Entry point with ui.run()
├── pages/
│   ├── __init__.py
│   ├── home.py          # @ui.page('/') 
│   └── about.py         # @ui.page('/about')
├── components/
│   ├── __init__.py
│   └── header.py        # Reusable components
├── static/              # Static files
└── pyproject.toml
```

## Documentation References

- [NiceGUI Prompt Guide](docs/nicegui_prompt.md) - Main AI agent guide
- [Mechanics](docs/mechanics/) - Core patterns
- [Class Reference](docs/classes/) - All UI elements with examples
- [Class References](docs/classes/*_references.md) - Source code & doc URLs

## Validation

Run validation before committing:

```bash
# Validate class references (fast)
poetry run python scripts/validate_classes.py

# Also check URLs (slower)
poetry run python scripts/validate_classes.py --check-urls

# Retry failed URLs only
poetry run python scripts/validate_classes.py --retry-failed
```

## Maintenance Rules

### Keep README.md Up to Date

Always update `README.md` when:
- Adding new files or directories
- Changing project structure
- Adding new scripts or tools
- Modifying documentation organization

The README should accurately reflect the current project structure at all times.

### Keep nicegui_prompt.md Up to Date

Always update `docs/nicegui_prompt.md` when:
- Adding new documentation folders (events, mechanics, etc.)
- Documenting new patterns or mechanics
- Adding important rules or gotchas
- Changing key concepts

The prompt guide is the main entry point for AI agents and must reflect all major changes.

### Class Reference Files

Each class category file (e.g., `controls.md`) has a corresponding `*_references.md` file with:
- **Description** - What the class does (visible at first glance)
- **Inherits** - Base class chain (essential for event handling)
- **Source** - Link to GitHub source code
- **Documentation** - Link to nicegui.io docs

#### Important Base Classes

Track these base classes in the Inherits column:
- `ui.element` - Base for all UI elements
- `ValueElement` - Elements with `.value` property and `on_change` event
- `DisableableElement` - Elements that can be disabled
- `ContentElement` - Elements with text/HTML content
- `SourceElement` - Elements with source (images, audio, video)
- `ChoiceElement` - Selection elements (radio, select, toggle)
- `ValidationElement` - Input elements with validation

#### Regenerate References

After modifying class documentation:
```bash
poetry run python scripts/generate_class_references.py
```

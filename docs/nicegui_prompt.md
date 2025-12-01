# NiceGUI Development Guide for AI Agents

This document helps AI coding agents build NiceGUI applications correctly.

## Quick Start

### New Project Setup (Always Use Poetry)

When creating a new NiceGUI project, **always use Poetry** for dependency management:

```bash
poetry new my-app
cd my-app
poetry add nicegui
```

Or for an existing directory:

```bash
cd my-app
poetry init
poetry add nicegui
```

**Basic Poetry project structure:**

```
my-app/
├── my_app/              # Package folder (underscore, not hyphen)
│   └── __init__.py      # Required for Python package
├── main.py              # Entry point with ui.run()
├── pyproject.toml       # Poetry config (auto-generated)
├── README.md            # Project documentation
└── AGENTS.md            # AI agent rules (see below)
```

**AGENTS.md for new projects:**
When creating a new NiceGUI project, always add an `AGENTS.md` file if one doesn't exist yet. Copy it from:
`https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/docs/mechanics/AGENTS.md`

This file contains project rules for AI agents working on NiceGUI projects.

Run your app with:

```bash
poetry run python main.py
```

If the user does not have installed Poetry yet, you can guide him here: https://python-poetry.org/docs/

### Minimal Example

```python
from nicegui import ui

ui.label('Hello World')
ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='My App', show=False)
```

Remark: For professioal applications do not build the root context but use the ui.page() decorator instead, example:

```python
from nicegui import ui

@ui.page('/')
def index():
    ui.label('Hello World')
    ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False)
```

For an even more ambitious projects use object orientation and build a class for each page. As an initializer can not be async we usually define a build() method that is called after the object is initialized. Example:

```python
from nicegui import ui

class Page:
    def __init__(self):
        pass

    async def build(self):
        ui.label('Hello World')
        ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

@ui.page('/')
async def index():
    await Page().build()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='My App', show=False)
```

## Events

Event handling documentation in the events folder:

| Topic | File | Description |
|-------|------|-------------|
| **Element Events** | [element_events.md](events/element_events.md) | Base `.on()` handler, DOM events |
| **Value Events** | [value_events.md](events/value_events.md) | `on_change` for inputs, selects, etc. |
| **Button Events** | [button_events.md](events/button_events.md) | `on_click` for buttons |
| **Keyboard Events** | [keyboard_events.md](events/keyboard_events.md) | Global keyboard handling |
| **Lifecycle Events** | [lifecycle_events.md](events/lifecycle_events.md) | App/client lifecycle hooks |
| **Upload Events** | [upload_events.md](events/upload_events.md) | File upload handling |

## Core Mechanics

Essential patterns for building NiceGUI applications in the mechanics folder:

| Topic | File | Description |
|-------|------|-------------|
| **Application Structure** | [application_structure.md](mechanics/application_structure.md) | Project setup, `ui.run()`, main guard |
| **Pages & Routing** | [pages.md](mechanics/pages.md) | `@ui.page`, URL parameters, navigation |
| **Container Updates** | [container_updates.md](mechanics/container_updates.md) | Dynamic content with `clear()` + `with` |
| **Event Binding** | [event_binding.md](mechanics/event_binding.md) | Constructor vs method, `on_value_change` |
| **Binding & State** | [binding_and_state.md](mechanics/binding_and_state.md) | Data binding, refreshable UI |
| **Data Modeling** | [data_modeling.md](mechanics/data_modeling.md) | Dataclasses, per-user storage, dashboards |
| **Styling** | [styling.md](mechanics/styling.md) | `.classes()`, `.style()`, custom CSS |
| **Background Execution** | [background_execution.md](mechanics/background_execution.md) | `run.io_bound`, `background_tasks`, threading |
| **Custom Components** | [custom_components.md](mechanics/custom_components.md) | Building Python/JS components |
| **Three.js Integration** | [threejs_integration.md](mechanics/threejs_integration.md) | 3D rendering with Three.js |
| **Coding Style** | [coding_style.md](mechanics/coding_style.md) | NiceGUI conventions, formatting, type hints |

## Class Reference by Category

Find detailed documentation for each category in the classes folder:

| Category | File | Description |
|----------|------|-------------|
| **Text Elements** | [text_elements.md](classes/text_elements.md) | Labels, links, markdown, HTML |
| **Controls** | [controls.md](classes/controls.md) | Buttons, inputs, selects, sliders |
| **Audiovisual** | [audiovisual.md](classes/audiovisual.md) | Images, audio, video, icons |
| **Data Elements** | [data_elements.md](classes/data_elements.md) | Tables, charts, 3D scenes, maps |
| **Layout** | [layout.md](classes/layout.md) | Containers, navigation, dialogs |
| **App & Config** | [app_and_config.md](classes/app_and_config.md) | Storage, lifecycle, routing |
| **Utilities** | [utilities.md](classes/utilities.md) | Background tasks, testing, HTML |

## Common Patterns

### Page with Layout
```python
from nicegui import ui

@ui.page('/')
def index():
    with ui.header():
        ui.label('My App').classes('text-xl')
    
    with ui.left_drawer():
        ui.link('Home', '/')
        ui.link('About', '/about')
    
    with ui.column().classes('p-4'):
        ui.label('Welcome!')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False)
```

### Form with Validation
```python
from nicegui import ui

name = ui.input('Name', validation={'Required': lambda v: bool(v)})
email = ui.input('Email', validation={'Invalid': lambda v: '@' in v})
ui.button('Submit', on_click=lambda: ui.notify(f'Hello {name.value}'))
```

### Data Binding
```python
from nicegui import ui

class Model:
    text = ''

model = Model()
ui.input('Type here').bind_value(model, 'text')
ui.label().bind_text_from(model, 'text', lambda t: f'You typed: {t}')
```

### Refreshable Content
```python
from nicegui import ui

items = []

@ui.refreshable
def show_items():
    for item in items:
        ui.label(item)

show_items()
ui.input('New item', on_change=lambda e: (items.append(e.value), show_items.refresh()))
```

### Async Operations
```python
from nicegui import ui, run

async def fetch_data():
    data = await run.io_bound(slow_api_call)
    ui.notify(f'Got: {data}')

ui.button('Fetch', on_click=fetch_data)
```

## Styling

NiceGUI uses **Tailwind CSS** and **Quasar** for styling:

```python
# Tailwind classes
ui.label('Styled').classes('text-2xl font-bold text-blue-500 bg-gray-100 p-4 rounded')

# Quasar props
ui.button('Outlined').props('outlined')
ui.input('Dense').props('dense filled')

# Inline CSS
ui.label('Custom').style('color: red; font-size: 24px')
```

## Key Concepts

1. **Main Guard**: Always use `if __name__ in {'__main__', '__mp_main__'}:` before `ui.run()`
2. **Context Managers**: Use `with` to nest elements inside containers
3. **Container Updates**: Call `.clear()` then enter context with `with` to rebuild content
4. **Event Binding**: Constructor (`on_change=`) vs method (`.on_value_change()`) - names differ!
5. **Binding**: Connect UI to data with `.bind_value()`, `.bind_text_from()`
6. **Refreshable**: Use `@ui.refreshable` for dynamic content that rebuilds
7. **Pages**: Define routes with `@ui.page('/path')`
8. **Storage**: Persist data with `app.storage.user`, `app.storage.general`

## Important Notes

- Always use `ui.run(show=False)` with `if __name__ in {'__main__', '__mp_main__'}:`
- Use `async` handlers for I/O operations
- Wrap CPU-bound work with `run.cpu_bound()`
- Use `.classes()` for Tailwind, `.props()` for Quasar, `.style()` for CSS
- Event method names differ from constructor: `on_change` → `.on_value_change()`

## Inheritance Matters

Check the `*_references.md` files for base class info:
- **ValueElement**: Has `.value` property and `on_change`/`.on_value_change()`
- **DisableableElement**: Can be disabled with `.disable()`/`.enable()`
- **ValidationElement**: Supports `validation` parameter
- **ChoiceElement**: Selection elements (radio, select, toggle)

## Sample Applications

When implementing a feature, **search the Sample Applications section by tags** to find relevant reference implementations. Each sample includes tags like `#charts`, `#authentication`, `#threejs`, `#custom-component`, `#spa`, etc. that help identify which sample demonstrates the pattern you need.

---

*This prompt should be updated when major documentation changes are made (new folders, new mechanics, new patterns).*

# NiceGUI Development Guide for AI Agents

This document helps AI coding agents build NiceGUI applications correctly.

## Quick Start

```python
from nicegui import ui

ui.label('Hello World')
ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False)
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

---

*This prompt should be updated when major documentation changes are made (new folders, new mechanics, new patterns).*

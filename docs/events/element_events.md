# Element Events (ui.element)

Base events available on all NiceGUI elements.

## Generic Event Handler

Use `.on()` to attach any DOM event:

```python
from nicegui import ui

ui.label('Click me').on('click', lambda: ui.notify('Clicked!'))
ui.label('Hover me').on('mouseenter', lambda: ui.notify('Hovered!'))
```

## Common DOM Events

| Event | Description |
|-------|-------------|
| `click` | Element clicked |
| `dblclick` | Element double-clicked |
| `mouseenter` | Mouse enters element |
| `mouseleave` | Mouse leaves element |
| `mousemove` | Mouse moves over element |
| `mousedown` | Mouse button pressed |
| `mouseup` | Mouse button released |
| `keydown` | Key pressed (focusable elements) |
| `keyup` | Key released |
| `focus` | Element gains focus |
| `blur` | Element loses focus |

## Event Handler Options

```python
# Throttle events (max once per interval)
ui.label('Move').on('mousemove', handler, throttle=0.1)

# Debounce events (wait for pause)
ui.input().on('input', handler, debounce=0.3)

# Get event arguments
def handler(e):
    print(e.args)  # Event data from JavaScript

ui.label('Click').on('click', handler)
```

## Async Event Handlers

```python
async def async_handler():
    await some_async_operation()
    ui.notify('Done!')

# Constructor style
ui.button('Async', on_click=async_handler)

# Method style
button = ui.button('Async')
button.on_click(async_handler)
```

## Lambda vs Function

```python
# Lambda for simple actions
ui.button('Notify', on_click=lambda: ui.notify('Hello'))

# Function for complex logic
def handle_click():
    # Multiple statements
    data = process()
    ui.notify(f'Result: {data}')

# Constructor style
ui.button('Process', on_click=handle_click)

# Method style (post-constructor)
button = ui.button('Process')
button.on_click(handle_click)
```

## Documentation

- [Generic Events](https://nicegui.io/documentation/generic_events)

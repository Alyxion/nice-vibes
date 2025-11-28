# Button Events

Events for clickable elements.

## on_click Event

The primary event for buttons:

```python
from nicegui import ui

# Constructor style
ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

# Method style (post-constructor)
button = ui.button('Click me')
button.on_click(lambda: ui.notify('Clicked!'))
```

## Event Object

```python
def handler(e):
    e.sender   # The button element
    e.client   # The client connection

# Constructor style
ui.button('Click', on_click=handler)

# Method style
button = ui.button('Click')
button.on_click(handler)
```

## Async Click Handlers

```python
async def fetch_data():
    ui.notify('Loading...')
    data = await some_api_call()
    ui.notify(f'Got: {data}')

# Constructor style
ui.button('Fetch', on_click=fetch_data)

# Method style
button = ui.button('Fetch')
button.on_click(fetch_data)
```

## Disabling During Action

```python
async def long_action():
    button.disable()
    await do_something()
    button.enable()

button = ui.button('Run', on_click=long_action)
```

## Button Variants

### Dropdown Button
```python
with ui.dropdown_button('Menu', on_click=lambda: print('Main clicked')):
    ui.item('Option 1', on_click=lambda: print('Option 1'))
    ui.item('Option 2', on_click=lambda: print('Option 2'))
```

### FAB (Floating Action Button)
```python
with ui.fab('add', on_click=lambda: print('FAB clicked')):
    ui.fab_action('edit', on_click=lambda: print('Edit'))
    ui.fab_action('delete', on_click=lambda: print('Delete'))
```

### Toggle/Radio (Value-based)
```python
# These use on_change, not on_click
ui.toggle(['A', 'B', 'C'], on_change=lambda e: print(e.value))
ui.radio(['X', 'Y', 'Z'], on_change=lambda e: print(e.value))
```

## Link vs Button

```python
# Link navigates, no on_click needed
ui.link('Go to docs', 'https://nicegui.io')

# Button with navigation
ui.button('Go Home', on_click=lambda: ui.navigate.to('/'))
```

## Documentation

- [Button](https://nicegui.io/documentation/button)
- [Dropdown Button](https://nicegui.io/documentation/dropdown_button)
- [FAB](https://nicegui.io/documentation/fab)

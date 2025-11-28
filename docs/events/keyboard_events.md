# Keyboard Events

Global and element-specific keyboard handling.

## Global Keyboard Handler

Capture keyboard events anywhere on the page:

```python
from nicegui import ui

def handle_key(e):
    if e.key == 'Escape':
        ui.notify('Escape pressed')
    elif e.key == 'Enter':
        ui.notify('Enter pressed')

# Constructor style
ui.keyboard(on_key=handle_key)

# Method style (post-constructor)
keyboard = ui.keyboard()
keyboard.on_key(handle_key)
```

## Key Event Properties

```python
def handler(e):
    e.key       # Key name: 'a', 'Enter', 'Escape', 'ArrowUp', etc.
    e.action    # 'keydown', 'keyup', or 'keypress'
    e.modifiers # Set of modifiers: {'ctrl', 'shift', 'alt', 'meta'}

ui.keyboard(on_key=handler)
```

## Modifier Keys

```python
def handler(e):
    if e.key == 's' and 'ctrl' in e.modifiers:
        ui.notify('Ctrl+S: Save!')
        e.prevent_default()  # Prevent browser save dialog
    
    if e.key == 'Enter' and 'shift' in e.modifiers:
        ui.notify('Shift+Enter')

ui.keyboard(on_key=handler)
```

## Key Filtering

Only listen for specific keys:

```python
# Only arrow keys
ui.keyboard(on_key=handler, ignore=[]).props('focus')

# Ignore when typing in inputs
ui.keyboard(on_key=handler)  # Default: ignores input/textarea
```

## Element-Specific Key Events

```python
def on_enter(e):
    if e.args.get('key') == 'Enter':
        ui.notify(f'Submitted: {input_field.value}')

input_field = ui.input('Search').on('keydown', on_enter)
```

## Common Patterns

### Submit on Enter
```python
def submit():
    ui.notify(f'Searching: {search.value}')

search = ui.input('Search', on_change=lambda e: None)
search.on('keydown.enter', submit)
```

### Keyboard Shortcuts
```python
shortcuts = {
    'n': lambda: ui.notify('New'),
    's': lambda: ui.notify('Save'),
    'd': lambda: ui.notify('Delete'),
}

def handle_key(e):
    if 'ctrl' in e.modifiers and e.key in shortcuts:
        shortcuts[e.key]()

ui.keyboard(on_key=handle_key)
```

### Arrow Key Navigation
```python
items = ['Item 1', 'Item 2', 'Item 3']
selected = {'index': 0}

def navigate(e):
    if e.key == 'ArrowDown':
        selected['index'] = min(selected['index'] + 1, len(items) - 1)
    elif e.key == 'ArrowUp':
        selected['index'] = max(selected['index'] - 1, 0)
    update_selection()

ui.keyboard(on_key=navigate)
```

## Documentation

- [Keyboard](https://nicegui.io/documentation/keyboard)
- [Generic Events](https://nicegui.io/documentation/generic_events)

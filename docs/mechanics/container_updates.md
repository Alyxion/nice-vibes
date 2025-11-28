# Updating Container Content in NiceGUI

## The Problem

NiceGUI elements are created once and rendered to the client. To dynamically update the content of a container, you cannot simply reassign children—you must clear and rebuild.

## The Pattern

To update a container's content:

1. Call `.clear()` to remove all children
2. Enter the container's context with `with`
3. Create new elements inside the context

```python
from nicegui import ui

container = ui.column()

def update_content():
    container.clear()
    with container:
        ui.label('New content!')
        ui.button('Another button')

ui.button('Update', on_click=update_content)
```

## Why This Works

- `container.clear()` removes all child elements from the DOM
- `with container:` sets the container as the current parent context
- Any `ui.*` calls inside the `with` block create elements as children of that container

## Common Patterns

### Dynamic List
```python
from nicegui import ui

items = []
item_list = ui.column()

def refresh_list():
    item_list.clear()
    with item_list:
        for item in items:
            ui.label(item)

def add_item():
    items.append(f'Item {len(items) + 1}')
    refresh_list()

ui.button('Add Item', on_click=add_item)
refresh_list()
```

### Conditional Content
```python
from nicegui import ui

content = ui.column()
show_details = False

def toggle_details():
    global show_details
    show_details = not show_details
    content.clear()
    with content:
        ui.label('Title')
        if show_details:
            ui.label('Detailed information here...')

ui.button('Toggle Details', on_click=toggle_details)
toggle_details()
```

### Loading State
```python
from nicegui import ui

container = ui.column()

async def load_data():
    container.clear()
    with container:
        ui.spinner()
    
    # Simulate async loading
    data = await fetch_data()
    
    container.clear()
    with container:
        for item in data:
            ui.label(item)
```

## Alternative: @ui.refreshable

For simpler cases, use the `@ui.refreshable` decorator:

```python
from nicegui import ui

items = ['A', 'B', 'C']

@ui.refreshable
def item_list():
    for item in items:
        ui.label(item)

item_list()

def add_item():
    items.append('New')
    item_list.refresh()  # Automatically clears and rebuilds

ui.button('Add', on_click=add_item)
```

### When to Use Each

| Approach | Use When |
|----------|----------|
| `clear()` + `with` | Fine-grained control, partial updates |
| `@ui.refreshable` | Entire section needs rebuilding |

## Important Notes

1. **Always clear before rebuilding** - Otherwise elements accumulate
2. **Store container reference** - You need the reference to call `.clear()` and enter context
3. **Context is required** - Elements created outside `with` go to the default parent
4. **Refreshable is simpler** - Prefer `@ui.refreshable` when possible

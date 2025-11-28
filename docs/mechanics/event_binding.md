# Event Binding in NiceGUI

NiceGUI supports two ways to attach event handlers: constructor parameters and methods.

## Two Ways to Bind Events

### 1. Constructor Parameter

Pass the handler directly when creating the element:

```python
ui.button('Click', on_click=lambda: ui.notify('Clicked!'))
ui.input('Name', on_change=lambda e: print(e.value))
```

### 2. Method Call

Attach the handler after creation using a method:

```python
button = ui.button('Click')
button.on_click(lambda: ui.notify('Clicked!'))

input_field = ui.input('Name')
input_field.on_value_change(lambda e: print(e.value))
```

## Important: Method Names Differ from Constructor Parameters

**The method name is NOT always the same as the constructor parameter!**

| Element | Constructor Parameter | Method |
|---------|----------------------|--------|
| Button | `on_click` | `.on_click()` |
| ValueElement | `on_change` | `.on_value_change()` |
| Upload | `on_upload` | `.on_upload()` |

### ValueElement Example

```python
# Constructor: on_change
ui.input('Name', on_change=handler)

# Method: on_value_change (NOT on_change!)
input_field = ui.input('Name')
input_field.on_value_change(handler)
```

## When to Use Each

### Constructor (Preferred for Simple Cases)
```python
# Clean, concise for single handler
ui.button('Save', on_click=save_data)
ui.input('Search', on_change=do_search)
```

### Method (For Complex Cases)
```python
# Multiple handlers
button = ui.button('Click')
button.on_click(log_click)
button.on_click(update_ui)

# Conditional binding
input_field = ui.input('Name')
if validate_mode:
    input_field.on_value_change(validate)

# Chaining with other methods
ui.input('Name').classes('w-full').on_value_change(handler)
```

## Generic Event Binding

For DOM events, use `.on()`:

```python
# Constructor style not available for DOM events
label = ui.label('Hover me')
label.on('mouseenter', lambda: ui.notify('Hovered!'))
label.on('mouseleave', lambda: ui.notify('Left!'))
```

## Documentation

- [Generic Events](https://nicegui.io/documentation/generic_events)

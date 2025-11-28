# Value Events (ValueElement)

Events for elements with a `.value` property (inputs, selects, checkboxes, etc.).

## Elements with ValueElement

All these inherit from `ValueElement` and support `on_change`:
- `ui.input`, `ui.textarea`, `ui.number`
- `ui.checkbox`, `ui.switch`
- `ui.select`, `ui.radio`, `ui.toggle`
- `ui.slider`, `ui.range`, `ui.knob`
- `ui.date`, `ui.time`, `ui.color_picker`
- `ui.codemirror`, `ui.editor`

## on_change Event

Fires when the value changes:

```python
from nicegui import ui

def on_change(e):
    print(f'New value: {e.value}')

# Constructor style: on_change parameter
ui.input('Name', on_change=on_change)
ui.checkbox('Accept', on_change=on_change)
ui.slider(min=0, max=100, on_change=on_change)

# Method style: .on_value_change() (NOTE: different name!)
input_field = ui.input('Name')
input_field.on_value_change(on_change)

checkbox = ui.checkbox('Accept')
checkbox.on_value_change(on_change)
```

**Important**: The method is `.on_value_change()`, NOT `.on_change()`!

## Event Object Properties

```python
def handler(e):
    e.value    # The new value
    e.sender   # The element that triggered the event
```

## Accessing Value Directly

```python
input_field = ui.input('Name')

def show_value():
    ui.notify(f'Current value: {input_field.value}')

ui.button('Show', on_click=show_value)
```

## Setting Value Programmatically

```python
input_field = ui.input('Name')

def reset():
    input_field.value = ''  # Triggers on_change if set

ui.button('Reset', on_click=reset)
```

## set_value() Without Triggering on_change

```python
input_field = ui.input('Name', on_change=lambda: print('Changed!'))

def silent_reset():
    input_field.set_value('')  # Does NOT trigger on_change

ui.button('Silent Reset', on_click=silent_reset)
```

## Common Patterns

### Form Validation
```python
def validate(e):
    if len(e.value) < 3:
        ui.notify('Too short!', type='warning')

ui.input('Username', on_change=validate)
```

### Dependent Fields
```python
country = ui.select(['USA', 'Canada', 'UK'], on_change=update_cities)
cities = ui.select([])

def update_cities(e):
    city_map = {
        'USA': ['New York', 'LA'],
        'Canada': ['Toronto', 'Vancouver'],
        'UK': ['London', 'Manchester'],
    }
    cities.options = city_map.get(e.value, [])
    cities.value = None
```

### Live Preview
```python
@ui.refreshable
def preview():
    ui.markdown(text_area.value)

text_area = ui.textarea('Markdown', on_change=preview.refresh)
preview()
```

## Documentation

- [ValueElement](https://nicegui.io/documentation/input) (see on_change parameter)
- [Generic Events](https://nicegui.io/documentation/generic_events)

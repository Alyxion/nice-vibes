# NiceGUI Controls

Interactive elements for user input and actions.

## Classes

| Class | Description |
|-------|-------------|
| `ui.button` | Clickable button |
| `ui.button_group` | Group of buttons |
| `ui.dropdown_button` | Button with dropdown menu |
| `ui.fab` | Floating Action Button |
| `ui.fab_action` | Action inside FAB |
| `ui.badge` | Badge/tag element |
| `ui.chip` | Chip/tag element |
| `ui.toggle` | Toggle button group |
| `ui.radio` | Radio button selection |
| `ui.select` | Dropdown selection |
| `ui.input_chips` | Input with chip tags |
| `ui.checkbox` | Checkbox input |
| `ui.switch` | Toggle switch |
| `ui.slider` | Slider input |
| `ui.range` | Range slider (min/max) |
| `ui.rating` | Star rating input |
| `ui.joystick` | Virtual joystick |
| `ui.input` | Text input field |
| `ui.textarea` | Multi-line text input |
| `ui.codemirror` | Code editor (CodeMirror) |
| `ui.xterm` | Terminal emulator |
| `ui.number` | Number input |
| `ui.knob` | Rotary knob input |
| `ui.color_input` | Color input field |
| `ui.color_picker` | Color picker dialog |
| `ui.date_input` | Date input field |
| `ui.date` | Date picker |
| `ui.time_input` | Time input field |
| `ui.time` | Time picker |
| `ui.upload` | File upload |

## Examples

### Button
```python
ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))
ui.button('With Icon', icon='thumb_up', on_click=handler)
```

### Input Fields
```python
ui.input('Name', placeholder='Enter your name')
ui.input('Password', password=True)
ui.textarea('Description')
ui.number('Age', min=0, max=120)
```

### Selection
```python
ui.select(['Option A', 'Option B', 'Option C'], value='Option A')
ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1)
ui.radio(['Red', 'Green', 'Blue'], value='Red')
ui.toggle(['On', 'Off'], value='On')
```

### Checkboxes & Switches
```python
ui.checkbox('Accept terms', on_change=lambda e: print(e.value))
ui.switch('Dark mode')
```

### Sliders
```python
ui.slider(min=0, max=100, value=50)
ui.range(min=0, max=100, value={'min': 20, 'max': 80})
ui.knob(0.5, min=0, max=1, step=0.1)
```

### Date & Time
```python
ui.date(value='2024-01-01')
ui.time(value='12:00')
ui.date_input('Select date')
ui.time_input('Select time')
```

### Color
```python
ui.color_input('Pick color', value='#ff0000')
ui.color_picker(on_pick=lambda e: print(e.color))
```

### File Upload
```python
ui.upload(on_upload=lambda e: print(e.name))
ui.upload(multiple=True, auto_upload=True)
```

### Code Editor
```python
ui.codemirror('print("Hello")', language='python')
```

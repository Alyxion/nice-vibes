# NiceGUI Utilities

Background tasks, async execution, testing, and HTML elements.

## Background Tasks

| Function | Description |
|----------|-------------|
| `background_tasks.create(coro)` | Create background task |
| `background_tasks.create_lazy(name, coro)` | Prevent duplicate tasks |
| `@background_tasks.await_on_shutdown` | Await during shutdown |

### Example
```python
from nicegui import background_tasks
import asyncio

async def long_running_task():
    await asyncio.sleep(10)
    print('Done!')

background_tasks.create(long_running_task())

# Prevent duplicates
background_tasks.create_lazy('my_task', long_running_task())
```

---

## Run Module

Execute blocking functions without blocking the UI.

| Function | Description |
|----------|-------------|
| `run.cpu_bound(func, *args)` | Run in separate process |
| `run.io_bound(func, *args)` | Run in separate thread |

### Example
```python
from nicegui import run, ui
import time

def slow_computation(n):
    time.sleep(2)
    return n * n

async def compute():
    result = await run.cpu_bound(slow_computation, 42)
    ui.notify(f'Result: {result}')

ui.button('Compute', on_click=compute)
```

---

## Testing

| Fixture | Description |
|---------|-------------|
| `Screen` | Headless browser testing (Selenium) |
| `User` | Simulated user testing (fast) |

### User Fixture Example
```python
from nicegui import ui
from nicegui.testing import User

async def test_button_click(user: User):
    @ui.page('/')
    def page():
        ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))
    
    await user.open('/')
    user.find('Click me').click()
    await user.should_see('Clicked!')
```

### Screen Fixture Example
```python
from nicegui.testing import Screen

def test_with_browser(screen: Screen):
    ui.button('Test')
    screen.open('/')
    screen.click('Test')
```

---

## HTML Namespace

Pure HTML elements for low-level control. Import with:

```python
from nicegui import html
```

### Available Elements

`a`, `abbr`, `acronym`, `address`, `area`, `article`, `aside`, `audio`, `b`, `basefont`, `bdi`, `bdo`, `big`, `blockquote`, `br`, `button`, `canvas`, `caption`, `cite`, `code`, `col`, `colgroup`, `data`, `datalist`, `dd`, `del_`, `details`, `dfn`, `dialog`, `div`, `dl`, `dt`, `em`, `embed`, `fieldset`, `figcaption`, `figure`, `footer`, `form`, `h1`, `header`, `hgroup`, `hr`, `i`, `iframe`, `img`, `input_`, `ins`, `kbd`, `label`, `legend`, `li`, `main`, `map_`, `mark`, `menu`, `meter`, `nav`, `object_`, `ol`, `optgroup`, `option`, `output`, `p`, `param`, `picture`, `pre`, `progress`, `q`, `rp`, `rt`, `ruby`, `s`, `samp`, `search`, `section`, `select`, `small`, `source`, `span`, `strong`, `sub`, `summary`, `sup`, `svg`, `table`, `tbody`, `td`, `template`, `textarea`, `tfoot`, `th`, `thead`, `time`, `tr`, `track`, `u`, `ul`, `var`, `video`, `wbr`

### Example
```python
from nicegui import html

with html.div().classes('container'):
    html.h1('Title')
    html.p('Paragraph text')
    with html.ul():
        html.li('Item 1')
        html.li('Item 2')
```

---

## Element Base Class

All UI elements inherit from `ui.element` and share these methods:

### Styling
```python
element.classes('text-xl bg-blue-500')      # Add CSS classes
element.classes(remove='old-class')          # Remove class
element.style('color: red; font-size: 20px') # Add inline style
element.props('outlined rounded')            # Add Quasar props
```

### Hierarchy
```python
element.clear()                    # Remove all children
element.move(new_parent)           # Move to new parent
element.remove(child)              # Remove specific child
element.delete()                   # Delete element
```

### Events
```python
element.on('click', handler)       # Add event handler
element.on('click', handler, throttle=0.5)  # Throttled
```

### Context Manager
```python
with ui.card() as card:
    ui.label('Inside card')
    with ui.row():
        ui.button('A')
        ui.button('B')
```

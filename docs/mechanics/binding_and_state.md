# NiceGUI Binding & State Management

Reactive data binding and state management patterns.

## UI Patterns

| Function | Description |
|----------|-------------|
| `ui.refreshable` | Decorator for refreshable UI sections |
| `ui.refreshable_method` | Refreshable method decorator |
| `ui.state(initial)` | Reactive state for refreshable UI |
| `ui.context` | Get current UI context |

## Binding Module

| Class/Function | Description |
|----------------|-------------|
| `binding.BindableProperty` | Bindable property descriptor |
| `binding.bindable_dataclass()` | Create bindable dataclass |
| `binding.bind(source, target)` | Two-way binding |
| `binding.bind_from(source, target)` | One-way (source → target) |
| `binding.bind_to(source, target)` | One-way (target → source) |

## Element Binding Methods

Every UI element supports these binding methods:

| Method | Description |
|--------|-------------|
| `.bind_value(obj, 'attr')` | Two-way bind value |
| `.bind_value_from(obj, 'attr')` | One-way bind value from |
| `.bind_value_to(obj, 'attr')` | One-way bind value to |
| `.bind_text(obj, 'attr')` | Two-way bind text |
| `.bind_text_from(obj, 'attr')` | One-way bind text from |
| `.bind_visibility(obj, 'attr')` | Bind visibility |
| `.bind_visibility_from(obj, 'attr')` | One-way bind visibility |

## Examples

### Basic Binding
```python
from nicegui import ui

class Model:
    name = ''
    show_greeting = True

model = Model()

ui.input('Name').bind_value(model, 'name')
ui.label().bind_text_from(model, 'name', lambda n: f'Hello, {n}!')
ui.label('Greeting').bind_visibility_from(model, 'show_greeting')
ui.checkbox('Show greeting').bind_value(model, 'show_greeting')
```

### Binding to Dictionary
```python
data = {'count': 0}

ui.number('Count').bind_value(data, 'count')
ui.label().bind_text_from(data, 'count')
```

### Refreshable UI
```python
from nicegui import ui

@ui.refreshable
def user_list():
    for user in users:
        ui.label(user)

users = ['Alice', 'Bob']
user_list()

def add_user():
    users.append('Charlie')
    user_list.refresh()

ui.button('Add User', on_click=add_user)
```

### Refreshable with State
```python
from nicegui import ui

@ui.refreshable
def counter():
    count, set_count = ui.state(0)
    ui.label(f'Count: {count}')
    ui.button('+', on_click=lambda: set_count(count + 1))

counter()
```

### Bindable Property
```python
from nicegui import ui
from nicegui import binding

class Counter:
    value = binding.BindableProperty()
    
    def __init__(self):
        self.value = 0

counter = Counter()
ui.slider(min=0, max=100).bind_value(counter, 'value')
ui.label().bind_text_from(counter, 'value')
```

### Bindable Dataclass
```python
from nicegui import ui
from nicegui.binding import bindable_dataclass

@bindable_dataclass
class Settings:
    volume: int = 50
    muted: bool = False

settings = Settings()
ui.slider(min=0, max=100).bind_value(settings, 'volume')
ui.switch('Muted').bind_value(settings, 'muted')
```

### Transformation Functions
```python
# Transform value when binding
ui.label().bind_text_from(
    model, 'price',
    backward=lambda p: f'${p:.2f}'
)

# Two-way with transforms
ui.input().bind_value(
    model, 'value',
    forward=lambda v: v.upper(),  # UI → model
    backward=lambda v: v.lower()  # model → UI
)
```

---

## Observables Module

Observable collections that notify on changes.

| Class | Description |
|-------|-------------|
| `ObservableCollection` | Base class |
| `ObservableDict` | Observable dictionary |
| `ObservableList` | Observable list |
| `ObservableSet` | Observable set |

### Example
```python
from nicegui.observables import ObservableList

items = ObservableList(['a', 'b', 'c'])

@ui.refreshable
def show_items():
    for item in items:
        ui.label(item)

show_items()

# Changes trigger UI update when bound
items.append('d')
```

---

## Event Module

Custom events for component communication.

| Method | Description |
|--------|-------------|
| `Event()` | Create event |
| `event.subscribe(callback)` | Subscribe to event |
| `event.emit(*args)` | Fire event (async) |
| `event.call(*args)` | Fire and await callbacks |

### Example
```python
from nicegui import Event

data_changed = Event()

@data_changed.subscribe
async def on_change(value):
    ui.notify(f'Data changed: {value}')

# Emit event
data_changed.emit('new value')
```

# Pages and Routing in NiceGUI

## Basic Page Definition

Use the `@ui.page` decorator to define routes:

```python
from nicegui import ui

@ui.page('/')
def index():
    ui.label('Home Page')

@ui.page('/about')
def about():
    ui.label('About Page')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```

## How Pages Work

1. **Decorator registers route** - `@ui.page('/path')` registers the function as a route handler
2. **Function builds UI** - When a user visits the path, the function executes
3. **Fresh instance per visit** - Each page visit creates a new UI instance
4. **Elements auto-attach** - UI elements created in the function become page content

## URL Parameters

### Path Parameters
```python
@ui.page('/user/{user_id}')
def user_page(user_id: str):
    ui.label(f'User ID: {user_id}')

@ui.page('/item/{item_id}/detail/{detail_id}')
def item_detail(item_id: int, detail_id: int):
    ui.label(f'Item {item_id}, Detail {detail_id}')
```

### Query Parameters
```python
from fastapi import Request

@ui.page('/search')
def search(request: Request):
    query = request.query_params.get('q', '')
    ui.label(f'Searching for: {query}')
    # URL: /search?q=hello
```

## Page Options

```python
@ui.page(
    '/dashboard',
    title='Dashboard',           # Browser tab title
    dark=True,                   # Dark mode
    response_timeout=30.0,       # Timeout in seconds
)
def dashboard():
    ui.label('Dashboard')
```

## Shared vs Per-Client State

### Per-Client (Default)
Each visitor gets their own UI instance:

```python
@ui.page('/')
def index():
    counter = 0  # Each visitor has their own counter
    
    def increment():
        nonlocal counter
        counter += 1
        label.text = str(counter)
    
    label = ui.label('0')
    ui.button('+', on_click=increment)
```

### Shared State
Use module-level or `app.storage.general` for shared data:

```python
from nicegui import app, ui

# Module-level shared state
shared_counter = {'value': 0}

@ui.page('/')
def index():
    def increment():
        shared_counter['value'] += 1
        label.text = str(shared_counter['value'])
    
    label = ui.label(str(shared_counter['value']))
    ui.button('+', on_click=increment)
```

## Auto-Index Page

Elements created outside `@ui.page` go to the auto-index page at `/`:

```python
from nicegui import ui

# This creates content on the root page
ui.label('Hello')  # Visible at /

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```

This is equivalent to:

```python
@ui.page('/')
def index():
    ui.label('Hello')
```

## Navigation Between Pages

```python
from nicegui import ui

@ui.page('/')
def index():
    ui.link('Go to About', '/about')
    ui.button('Navigate', on_click=lambda: ui.navigate.to('/about'))

@ui.page('/about')
def about():
    ui.link('Back to Home', '/')
    ui.button('Go Back', on_click=ui.navigate.back)
```

## Page Layout Pattern

```python
from nicegui import ui

def create_layout():
    """Shared layout for all pages"""
    with ui.header():
        ui.label('My App').classes('text-xl')
        ui.link('Home', '/')
        ui.link('About', '/about')

@ui.page('/')
def index():
    create_layout()
    ui.label('Welcome to the home page')

@ui.page('/about')
def about():
    create_layout()
    ui.label('About us')
```

## Async Pages

Pages can be async for I/O operations:

```python
@ui.page('/data')
async def data_page():
    ui.spinner()
    data = await fetch_data_from_api()
    ui.label(f'Data: {data}')
```

## Important Notes

1. **One function per route** - Each path needs its own decorated function
2. **Function runs on each visit** - Don't put expensive setup in page functions
3. **Elements are scoped** - UI elements belong to the page/client that created them
4. **Use storage for persistence** - `app.storage.user` persists across page visits

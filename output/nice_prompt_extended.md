# NiceGUI Master Prompt

Complete reference for AI agents building NiceGUI applications.

Source: https://github.com/Alyxion/nice-prompt

---


<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/nicegui_prompt.md -->

# NiceGUI Development Guide for AI Agents

This document helps AI coding agents build NiceGUI applications correctly.

## Quick Start

```python
from nicegui import ui

ui.label('Hello World')
ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False)
```

## Events

Event handling documentation in the events folder:

| Topic | File | Description |
|-------|------|-------------|
| **Element Events** | [element_events.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/events/element_events.md) | Base `.on()` handler, DOM events |
| **Value Events** | [value_events.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/events/value_events.md) | `on_change` for inputs, selects, etc. |
| **Button Events** | [button_events.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/events/button_events.md) | `on_click` for buttons |
| **Keyboard Events** | [keyboard_events.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/events/keyboard_events.md) | Global keyboard handling |
| **Lifecycle Events** | [lifecycle_events.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/events/lifecycle_events.md) | App/client lifecycle hooks |
| **Upload Events** | [upload_events.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/events/upload_events.md) | File upload handling |

## Core Mechanics

Essential patterns for building NiceGUI applications in the mechanics folder:

| Topic | File | Description |
|-------|------|-------------|
| **Application Structure** | [application_structure.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/application_structure.md) | Project setup, `ui.run()`, main guard |
| **Pages & Routing** | [pages.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/pages.md) | `@ui.page`, URL parameters, navigation |
| **Container Updates** | [container_updates.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/container_updates.md) | Dynamic content with `clear()` + `with` |
| **Event Binding** | [event_binding.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/event_binding.md) | Constructor vs method, `on_value_change` |
| **Binding & State** | [binding_and_state.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/binding_and_state.md) | Data binding, refreshable UI |
| **Data Modeling** | [data_modeling.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/data_modeling.md) | Dataclasses, per-user storage, dashboards |
| **Styling** | [styling.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/styling.md) | `.classes()`, `.style()`, custom CSS |
| **Background Execution** | [background_execution.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/background_execution.md) | `run.io_bound`, `background_tasks`, threading |
| **Custom Components** | [custom_components.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/custom_components.md) | Building Python/JS components |
| **Three.js Integration** | [threejs_integration.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/threejs_integration.md) | 3D rendering with Three.js |
| **Coding Style** | [coding_style.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/coding_style.md) | NiceGUI conventions, formatting, type hints |

## Class Reference by Category

Find detailed documentation for each category in the classes folder:

| Category | File | Description |
|----------|------|-------------|
| **Text Elements** | [text_elements.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/text_elements.md) | Labels, links, markdown, HTML |
| **Controls** | [controls.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/controls.md) | Buttons, inputs, selects, sliders |
| **Audiovisual** | [audiovisual.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/audiovisual.md) | Images, audio, video, icons |
| **Data Elements** | [data_elements.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/data_elements.md) | Tables, charts, 3D scenes, maps |
| **Layout** | [layout.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/layout.md) | Containers, navigation, dialogs |
| **App & Config** | [app_and_config.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/app_and_config.md) | Storage, lifecycle, routing |
| **Utilities** | [utilities.md](https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/utilities.md) | Background tasks, testing, HTML |

## Common Patterns

### Page with Layout
```python
from nicegui import ui

@ui.page('/')
def index():
    with ui.header():
        ui.label('My App').classes('text-xl')
    
    with ui.left_drawer():
        ui.link('Home', '/')
        ui.link('About', '/about')
    
    with ui.column().classes('p-4'):
        ui.label('Welcome!')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False)
```

### Form with Validation
```python
from nicegui import ui

name = ui.input('Name', validation={'Required': lambda v: bool(v)})
email = ui.input('Email', validation={'Invalid': lambda v: '@' in v})
ui.button('Submit', on_click=lambda: ui.notify(f'Hello {name.value}'))
```

### Data Binding
```python
from nicegui import ui

class Model:
    text = ''

model = Model()
ui.input('Type here').bind_value(model, 'text')
ui.label().bind_text_from(model, 'text', lambda t: f'You typed: {t}')
```

### Refreshable Content
```python
from nicegui import ui

items = []

@ui.refreshable
def show_items():
    for item in items:
        ui.label(item)

show_items()
ui.input('New item', on_change=lambda e: (items.append(e.value), show_items.refresh()))
```

### Async Operations
```python
from nicegui import ui, run

async def fetch_data():
    data = await run.io_bound(slow_api_call)
    ui.notify(f'Got: {data}')

ui.button('Fetch', on_click=fetch_data)
```

## Styling

NiceGUI uses **Tailwind CSS** and **Quasar** for styling:

```python
# Tailwind classes
ui.label('Styled').classes('text-2xl font-bold text-blue-500 bg-gray-100 p-4 rounded')

# Quasar props
ui.button('Outlined').props('outlined')
ui.input('Dense').props('dense filled')

# Inline CSS
ui.label('Custom').style('color: red; font-size: 24px')
```

## Key Concepts

1. **Main Guard**: Always use `if __name__ in {'__main__', '__mp_main__'}:` before `ui.run()`
2. **Context Managers**: Use `with` to nest elements inside containers
3. **Container Updates**: Call `.clear()` then enter context with `with` to rebuild content
4. **Event Binding**: Constructor (`on_change=`) vs method (`.on_value_change()`) - names differ!
5. **Binding**: Connect UI to data with `.bind_value()`, `.bind_text_from()`
6. **Refreshable**: Use `@ui.refreshable` for dynamic content that rebuilds
7. **Pages**: Define routes with `@ui.page('/path')`
8. **Storage**: Persist data with `app.storage.user`, `app.storage.general`

## Important Notes

- Always use `ui.run(show=False)` with `if __name__ in {'__main__', '__mp_main__'}:`
- Use `async` handlers for I/O operations
- Wrap CPU-bound work with `run.cpu_bound()`
- Use `.classes()` for Tailwind, `.props()` for Quasar, `.style()` for CSS
- Event method names differ from constructor: `on_change` → `.on_value_change()`

## Inheritance Matters

Check the `*_references.md` files for base class info:
- **ValueElement**: Has `.value` property and `on_change`/`.on_value_change()`
- **DisableableElement**: Can be disabled with `.disable()`/`.enable()`
- **ValidationElement**: Supports `validation` parameter
- **ChoiceElement**: Selection elements (radio, select, toggle)

---

*This prompt should be updated when major documentation changes are made (new folders, new mechanics, new patterns).*



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/poetry_setup.md -->

# Poetry Setup

We recommend [Poetry](https://python-poetry.org/) for dependency management.

## Project Structure

A valid Poetry package requires:

```
my_app/
├── pyproject.toml    # Dependencies and project config
├── poetry.lock       # Locked versions (commit this)
├── README.md         # Required for valid package
├── my_app/           # Package folder (matches project name)
│   ├── __init__.py
│   └── main.py
└── tests/            # Optional test folder
    └── test_app.py
```

## pyproject.toml

```toml
[tool.poetry]
name = "my-app"
version = "0.1.0"
description = "My NiceGUI application"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "my_app"}]

[tool.poetry.dependencies]
python = "^3.12"
nicegui = "^3.3"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Commands

```bash
# Install dependencies
poetry install

# Run application
poetry run python my_app/main.py

# Add a dependency
poetry add httpx

# Add dev dependency
poetry add --group dev pytest

# Update dependencies
poetry update

# Show installed packages
poetry show

# Lock and install in one command (useful after pyproject.toml changes)
poetry lock && poetry install
```

## Running Scripts

Always use `poetry run` to ensure the virtual environment is active:

```bash
# Run main application
poetry run python my_app/main.py

# Run tests
poetry run pytest

# Run any script
poetry run python scripts/my_script.py
```

## Storage Secret

For `app.storage.client` to work, set a storage secret:

```python
ui.run(storage_secret='your-secret-key')
```

Generate a secure secret:

```bash
poetry run python -c "import secrets; print(secrets.token_hex(32))"
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/application_structure.md -->

# NiceGUI Application Structure

## Minimal Application

```python
from nicegui import ui

ui.label('Hello World')

ui.run()
```

## Production Application Structure

**Critical**: Always wrap `ui.run()` in the multiprocessing guard for production:

```python
from nicegui import ui

@ui.page('/')
def index():
    ui.label('Hello World')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```

### Why This Guard?

- **`__main__`** - Normal script execution
- **`__mp_main__`** - Multiprocessing spawn context (used on macOS/Windows)

Without the guard:
1. **Multiprocessing** - Worker processes would start their own servers
2. **Import safety** - Importing your module would start the server
3. **Testing** - Test frameworks would trigger `ui.run()`
4. **Reload mode** - Hot reload would create duplicate servers

## Recommended Project Structure

### Multi-Page Application (with @ui.page)

```
my_app/
├── main.py              # Entry point with ui.run()
├── pages/
│   ├── __init__.py
│   ├── home.py          # @ui.page('/') 
│   ├── about.py         # @ui.page('/about')
│   └── dashboard.py     # @ui.page('/dashboard')
├── components/
│   ├── __init__.py
│   ├── header.py        # Reusable header component
│   └── sidebar.py       # Reusable sidebar
├── static/              # Static files (images, CSS)
├── requirements.txt
└── pyproject.toml
```

### SPA with Sub Pages (Recommended for Dashboards)

For single-page applications with client-side routing:

```
my_app/
├── main.py              # Server setup only (static files, page discovery, ui.run)
├── layout.py            # AppLayout class (header, drawer, routing, auth checks)
├── models/
│   ├── __init__.py      # Exports AuthSession, etc.
│   └── auth.py          # AuthSession dataclass, USERS, ROLE_PERMISSIONS
├── pages/
│   ├── home/
│   │   ├── __init__.py      # Exports only
│   │   └── home.py          # Implementation
│   ├── settings/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── ...
├── static/
│   ├── css/
│   │   └── app.css          # Custom styles
│   └── js/
│       └── app.js           # Custom JavaScript
└── pyproject.toml
```

### Separation of Concerns

**`main.py`** - Server setup only:
```python
from pathlib import Path
from nicegui import app, ui
from layout import AppLayout

STATIC_DIR = Path(__file__).parent / 'static'
PAGES_DIR = Path(__file__).parent / 'pages'

app.add_static_files('/static', STATIC_DIR)
AppLayout.discover_pages(str(PAGES_DIR), exclude={'login'})

def root():
    AppLayout.current().build()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        root,
        title='My App',
        reload=True,
        uvicorn_reload_includes='*.py,*.js,*.css',
    )
```

**`layout.py`** - All UI logic (header, drawer, navigation, auth checks)

### Module Organization

Keep `__init__.py` files minimal - they should only export:

```python
# pages/home/__init__.py
"""Home page module."""
from .home import HomePage

__all__ = ['HomePage']
```

Implementation goes in a separate file:

```python
# pages/home/home.py
"""Home page implementation."""
from nicegui import ui

class HomePage:
    PAGE = {'path': '/', 'label': 'Home', 'icon': 'home'}
    
    async def build(self) -> None:
        ui.label('Welcome!')
```

This pattern:
- Keeps imports clean
- Avoids circular dependencies  
- Makes it clear what each module exports
- Allows IDE navigation to the actual implementation
- **Names files after content** - `home.py` not `page.py` or `dashboard.py`

### main.py
```python
from nicegui import app, ui

# Import pages to register routes
from pages import home, about, dashboard

# Serve static files
app.add_static_files('/static', 'static')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='My App',
        port=8080,
    )
```

### pages/home.py
```python
from nicegui import ui
from components.header import create_header

@ui.page('/')
def home():
    create_header()
    ui.label('Welcome!')
```

### components/header.py
```python
from nicegui import ui

def create_header():
    with ui.header().classes('bg-blue-500'):
        ui.label('My App').classes('text-xl text-white')
        with ui.row():
            ui.link('Home', '/').classes('text-white')
            ui.link('About', '/about').classes('text-white')
```

## ui.run() Options

```python
ui.run(
    # Server
    host='0.0.0.0',          # Bind address (default: '127.0.0.1')
    port=8080,               # Port (default: 8080)
    
    # Display
    title='My App',          # Browser tab title
    dark=None,               # Dark mode: True, False, or None (auto)
    
    # Development
    reload=True,             # Hot reload on file changes
    show=True,               # Open browser on start
    
    # Native mode
    native=False,            # Run in native window
    window_size=(800, 600),  # Native window size
    
    # Storage
    storage_secret='secret', # Secret for signed storage
)
```

## Lifecycle Hooks

```python
from nicegui import app, ui

@app.on_startup
async def startup():
    """Called once when app starts"""
    print('App starting...')
    # Initialize database, load config, etc.

@app.on_shutdown  
async def shutdown():
    """Called once when app stops"""
    print('App shutting down...')
    # Cleanup resources

@app.on_connect
async def connect():
    """Called when each client connects"""
    print('Client connected')

@app.on_disconnect
async def disconnect():
    """Called when each client disconnects"""
    print('Client disconnected')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```

## Integration with FastAPI

For existing FastAPI applications:

```python
from fastapi import FastAPI
from nicegui import ui

app = FastAPI()

@app.get('/api/data')
def get_data():
    return {'value': 42}

@ui.page('/')
def index():
    ui.label('NiceGUI + FastAPI')

ui.run_with(app)  # Attach to existing FastAPI app
```

## Environment-Based Configuration

```python
import os
from nicegui import ui

DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

@ui.page('/')
def index():
    ui.label('My App')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        host='0.0.0.0' if not DEBUG else '127.0.0.1',
        port=int(os.getenv('PORT', 8080)),
        reload=DEBUG,
        show=DEBUG,
    )
```

## Common Mistakes

### ❌ Missing main guard
```python
from nicegui import ui

ui.label('Hello')
ui.run()  # Will cause issues with multiprocessing/reload
```

### ✅ With main guard
```python
from nicegui import ui

ui.label('Hello')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```

### ❌ Code after ui.run()
```python
if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
    print('This never executes!')  # ui.run() blocks
```

### ✅ Use lifecycle hooks instead
```python
@app.on_startup
async def init():
    print('This runs at startup')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/pages.md -->

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

## Root Page Mechanism

When you pass a `root` function to `ui.run()`, it acts as a **catch-all** for any URL that doesn't match an explicit `@ui.page` route:

```python
from nicegui import ui

@ui.page('/about')
def about():
    ui.label('About')  # Only handles /about

def root():
    ui.label('Main')   # Handles /, /foo, /bar/baz, etc.

ui.run(root)
```

This works via the 404 exception handler - unmatched URLs trigger the root page instead of showing an error.

### Route Precedence

1. Explicit `@ui.page` routes are matched first
2. Internal `/_nicegui/*` routes (uploads, static files) are matched next
3. If nothing matches, the root page is served (if defined)

See [Routing Architecture](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/routing.md) for detailed explanation.

## Important Notes

1. **One function per route** - Each path needs its own decorated function
2. **Function runs on each visit** - Don't put expensive setup in page functions
3. **Elements are scoped** - UI elements belong to the page/client that created them
4. **Use storage for persistence** - `app.storage.user` persists across page visits
5. **Root page catches all** - When using `ui.run(root)`, unmatched URLs go to root



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/sub_pages.md -->

# NiceGUI Sub Pages - Client-Side Routing

`ui.sub_pages` enables **Single Page Application (SPA)** routing within NiceGUI. Navigation between views happens client-side without full page reloads.

## Key Advantages

- **Persistent State**: `app.storage.client` stays alive across sub-page navigation - objects remain "living"
- **Fast Navigation**: No script reload, instant view switching
- **Shared Layout**: Header, sidebar, and other elements persist across routes

## How It Works with Server Routing

When using `ui.sub_pages` with a root page, two routing layers work together:

1. **Server-side (404 fallback)**: The root page catches ALL unmatched URLs
2. **Client-side (sub_pages)**: JavaScript handles navigation without page reloads

```
Browser requests /about
    ↓
Server: No explicit @ui.page('/about') route
    ↓
404 handler: core.root exists → serve root page
    ↓
Client: ui.sub_pages matches '/about' → render about content
```

This is why you **don't need** a catch-all `@ui.page('/{_:path}')` pattern - the root page mechanism already captures all URLs.

See [Routing Architecture](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/routing.md) for detailed explanation of route precedence.

## Basic Usage

```python
from nicegui import ui

@ui.page('/')
def main_page():
    with ui.header():
        ui.button('Home', on_click=lambda: ui.navigate.to('/'))
        ui.button('About', on_click=lambda: ui.navigate.to('/about'))
        ui.button('User', on_click=lambda: ui.navigate.to('/user/123'))
    
    ui.sub_pages({
        '/': home_page,
        '/about': about_page,
        '/user/{id}': user_page,
    })

def home_page():
    ui.label('Welcome to the home page')

def about_page():
    ui.label('About us')

def user_page(id: str):
    ui.label(f'User profile: {id}')

ui.run()
```

> **Note**: The catch-all pattern `@ui.page('/{_:path}')` is **not required**. `ui.sub_pages` handles client-side routing internally - navigation between sub-pages happens without server round-trips.

## Route Patterns

Routes support path parameters using `{param_name}` syntax:

| Pattern | Matches | Parameters |
|---------|---------|------------|
| `/` | Exact root | None |
| `/about` | Exact path | None |
| `/user/{id}` | `/user/123` | `id='123'` |
| `/post/{category}/{id}` | `/post/tech/42` | `category='tech'`, `id='42'` |

## Page Builder Functions

Builder functions receive path parameters as keyword arguments:

```python
def user_page(id: str):
    ui.label(f'Viewing user {id}')

def product_page(category: str, product_id: str):
    ui.label(f'Product {product_id} in {category}')
```

## PageArguments for Advanced Access

Use `PageArguments` type hint for full route information:

```python
from nicegui.page_arguments import PageArguments

def search_page(args: PageArguments):
    ui.label(f'Path: {args.path}')
    ui.label(f'Parameters: {args.parameters}')
    ui.label(f'Query: {args.query_params.get("q")}')  # ?q=value
    ui.label(f'Fragment: {args.fragment}')             # #section
```

## Constructor Parameters

```python
ui.sub_pages(
    routes={...},              # Path pattern → builder function
    root_path='/app',          # Path prefix to strip (reverse proxy)
    data={'key': 'value'},     # Data passed to all builders
    show_404=True,             # Show 404 for unmatched routes
)
```

## Dynamic Route Addition

```python
router = ui.sub_pages({'/': home})
router.add('/settings', settings_page)
router.add('/profile/{username}', profile_page)
```

## Nested Sub Pages

```python
def admin_section():
    ui.label('Admin Panel')
    ui.sub_pages({
        '/users': admin_users,
        '/settings': admin_settings,
    })

# Main router includes admin section
ui.sub_pages({
    '/': home,
    '/admin': admin_section,  # Nested routing
})
```

## Navigation

```python
ui.button('Home', on_click=lambda: ui.navigate.to('/'))
ui.button('Search', on_click=lambda: ui.navigate.to('/search?q=nicegui'))
ui.button('Section', on_click=lambda: ui.navigate.to('/docs#installation'))
```

## Async Page Builders

```python
async def user_page(id: str):
    ui.spinner()
    user = await fetch_user(id)
    ui.label(f'Name: {user.name}')
```

## Persistent Client State Example

Since `app.storage.client` persists across sub-page navigation, you can maintain live objects:

```python
from nicegui import app, ui

@ui.page('/')
def spa():
    # Initialize once, persists across all sub-pages
    if 'counter' not in app.storage.client:
        app.storage.client['counter'] = 0
    
    with ui.header():
        ui.label().bind_text_from(app.storage.client, 'counter', 
                                   backward=lambda c: f'Count: {c}')
        ui.button('+', on_click=lambda: app.storage.client.update(
            counter=app.storage.client['counter'] + 1))
    
    ui.sub_pages({
        '/': page_a,
        '/other': page_b,
    })

def page_a():
    ui.label('Page A - counter persists when navigating!')
    ui.button('Go to B', on_click=lambda: ui.navigate.to('/other'))

def page_b():
    ui.label('Page B - same counter value!')
    ui.button('Go to A', on_click=lambda: ui.navigate.to('/'))
```

## Custom 404 Handling

Subclass `SubPages` for custom error pages:

```python
from nicegui.elements.sub_pages import SubPages

class CustomSubPages(SubPages):
    def _render_404(self):
        ui.label('Page not found!').classes('text-red-500')
        ui.button('Go Home', on_click=lambda: ui.navigate.to('/'))

# Use instead of ui.sub_pages
CustomSubPages({'/': home, '/about': about})
```

## Route Protection

Since sub pages only render **after** the parent page executes, authentication checks belong in the parent/layout page - not in individual sub pages.

See [Authentication Pattern](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/authentication.md) for a complete example with login page, session management, and role-based access.

## Layout Constraints

### Header/Drawer Must Be Outside sub_pages

Top-level layout elements (`ui.header`, `ui.left_drawer`, `ui.footer`) **cannot** be nested inside `ui.sub_pages`. They must be created in the parent:

```python
# CORRECT - header/drawer at root level
def root():
    header = ui.header()
    drawer = ui.left_drawer()
    
    with ui.column():
        ui.sub_pages({...})

# WRONG - will cause RuntimeError
def root():
    ui.sub_pages({
        '/': lambda: ui.header()  # Error!
    })
```

### Hiding Header/Drawer on Login Page

Store references and toggle visibility. **Key pattern**: Call `show()` at the start of every regular page builder to handle back button navigation from login:

```python
class AppLayout:
    def __init__(self):
        self.header = None
        self.drawer = None
    
    def hide(self):
        if self.header:
            self.header.set_visibility(False)
        if self.drawer:
            self.drawer.set_visibility(False)
            self.drawer.hide()
    
    def show(self):
        if self.header:
            self.header.set_visibility(True)
        if self.drawer:
            self.drawer.set_visibility(True)
            self.drawer.show()
    
    def build_login_page(self):
        self.hide()  # Hide on login
        # ... login form
    
    def make_page_builder(self, page_info):
        async def builder():
            self.show()  # Always show on regular pages (handles back button)
            # ... page content
        return builder
    
    def build(self):
        self.header = ui.header()
        self.drawer = ui.left_drawer()
        
        ui.sub_pages({
            '/login': self.build_login_page,
            '/': self.make_page_builder({'path': '/'}),
        })
```

This pattern ensures header/drawer are restored when:
- User clicks Cancel on login
- User presses browser back button from login
- User navigates to any regular page

### Full-Width Content

By default, NiceGUI may constrain content width. Add CSS to ensure full width:

```css
.nicegui-content,
.nicegui-sub-pages,
.q-page,
.q-page-container {
    width: 100% !important;
    max-width: 100% !important;
}
```

## Login Page Integration

**Key insight**: The login page should be a sub_page route, not a separate `@ui.page('/login')`:

```python
ui.sub_pages({
    '/login': build_login_page,  # Part of same SPA
    '/': home_page,
    '/settings': settings_page,
})
```

Benefits:
- Session state (`app.storage.client`) persists across navigation
- Header/drawer can be hidden/shown dynamically
- No full page reload on login/logout

## Avoiding Global Variables

Don't use global variables for UI references. Instead, use a class stored in `app.storage.client`:

```python
class AppLayout:
    @classmethod
    def current(cls) -> 'AppLayout':
        if 'layout' not in app.storage.client:
            app.storage.client['layout'] = cls()
        return app.storage.client['layout']

def root():
    AppLayout.current().build()
```

## Documentation

- [NiceGUI Sub Pages](https://nicegui.io/documentation/sub_pages)



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/container_updates.md -->

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

### Append Without Clearing

To add elements without rebuilding the entire container, just enter the context:

```python
from nicegui import ui

container = ui.column()

def add_item():
    # No clear() - just append to existing content
    with container:
        ui.label(f'Item {len(container)}')

ui.button('Add Item', on_click=add_item)
```

### Clear and Rebuild

To replace all content, use `clear()` first:

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

1. **Append vs Rebuild** - Use `with container:` alone to append, add `.clear()` to rebuild
2. **Store container reference** - You need the reference to call `.clear()` and enter context
3. **Context is required** - Elements created outside `with` go to the default parent
4. **Refreshable is simpler** - Prefer `@ui.refreshable` when possible



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/data_modeling.md -->

# Data Modeling in NiceGUI

Best practices for managing user data in NiceGUI applications.

## Core Principles

1. **Use dataclasses or Pydantic** for data structures
2. **Never use global variables** - NiceGUI serves concurrent users
3. **Group user data in a class** instead of scattered variables
4. **Store per-user data in `app.storage.client`**

## User Data Class Pattern

```python
from dataclasses import dataclass, field
from nicegui import app, ui


@dataclass
class UserData:
    """Per-user application state."""
    name: str = ''
    email: str = ''
    items: list[str] = field(default_factory=list)
    
    @classmethod
    def get_current(cls) -> 'UserData':
        """Get or create UserData for the current user."""
        if 'user_data' not in app.storage.client:
            app.storage.client['user_data'] = cls()
        return app.storage.client['user_data']
```

## Usage in Pages

```python
@ui.page('/')
def index():
    data = UserData.get_current()
    
    ui.input('Name').bind_value(data, 'name')
    ui.input('Email').bind_value(data, 'email')
```

## With Pydantic

```python
from pydantic import BaseModel, Field
from nicegui import app, ui


class UserData(BaseModel):
    """Per-user application state with validation."""
    name: str = ''
    email: str = ''
    age: int = 0
    
    class Config:
        # Allow mutation for binding
        frozen = False
    
    @classmethod
    def get_current(cls) -> 'UserData':
        """Get or create UserData for the current user."""
        if 'user_data' not in app.storage.client:
            app.storage.client['user_data'] = cls()
        return app.storage.client['user_data']
```

## Dashboard with Computed Values

For dashboards where inputs affect computed results:

```python
from dataclasses import dataclass
from nicegui import app, ui


@dataclass
class DashboardData:
    quantity: int = 0
    unit_price: float = 0.0
    total: float = 0.0  # Computed field
    
    def compute_total(self):
        """Recompute derived values."""
        self.total = self.quantity * self.unit_price
    
    @classmethod
    def get_current(cls) -> 'DashboardData':
        if 'dashboard' not in app.storage.client:
            app.storage.client['dashboard'] = cls()
        return app.storage.client['dashboard']


@ui.page('/dashboard')
def dashboard():
    data = DashboardData.get_current()
    
    def on_input_change(e):
        data.compute_total()
    
    # Inputs bound to data, trigger recomputation on change
    ui.number('Quantity', min=0).bind_value(data, 'quantity').on_value_change(on_input_change)
    ui.number('Unit Price', min=0, format='%.2f').bind_value(data, 'unit_price').on_value_change(on_input_change)
    
    # Result automatically updates via bind_text_from
    ui.label().bind_text_from(data, 'total', lambda t: f'Total: ${t:.2f}')
```

## Why Not Global Variables?

```python
# BAD: Global state shared between all users!
user_name = ''
user_items = []

@ui.page('/')
def index():
    global user_name  # All users see/modify the same data!
    ui.input('Name').bind_value(globals(), 'user_name')


# GOOD: Per-user state via app.storage.client
@ui.page('/')
def index():
    data = UserData.get_current()  # Each user gets their own instance
    ui.input('Name').bind_value(data, 'name')
```

## Storage Scopes

| Storage | Scope | Use Case |
|---------|-------|----------|
| `app.storage.client` | Per browser tab | User session data |
| `app.storage.user` | Per authenticated user | Persistent user preferences |
| `app.storage.general` | Shared across all users | App-wide settings |

## Complete Example

```python
from dataclasses import dataclass, field
from nicegui import app, ui


@dataclass
class OrderData:
    customer_name: str = ''
    items: list[dict] = field(default_factory=list)
    discount_percent: float = 0.0
    subtotal: float = 0.0
    total: float = 0.0
    
    def add_item(self, name: str, price: float):
        self.items.append({'name': name, 'price': price})
        self.recompute()
    
    def recompute(self):
        self.subtotal = sum(item['price'] for item in self.items)
        self.total = self.subtotal * (1 - self.discount_percent / 100)
    
    @classmethod
    def get_current(cls) -> 'OrderData':
        if 'order' not in app.storage.client:
            app.storage.client['order'] = cls()
        return app.storage.client['order']


@ui.page('/')
def index():
    order = OrderData.get_current()
    
    ui.input('Customer').bind_value(order, 'customer_name')
    
    ui.number('Discount %', min=0, max=100).bind_value(
        order, 'discount_percent'
    ).on_value_change(lambda: order.recompute())
    
    ui.label().bind_text_from(order, 'subtotal', lambda v: f'Subtotal: ${v:.2f}')
    ui.label().bind_text_from(order, 'total', lambda v: f'Total: ${v:.2f}')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='your-secret-key')  # Required for storage
```

## Documentation

- [Storage](https://nicegui.io/documentation/storage)
- [Data Binding](https://nicegui.io/documentation/section_binding_properties)



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/binding_and_state.md -->

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



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/event_binding.md -->

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



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/styling.md -->

# Styling in NiceGUI

NiceGUI provides multiple ways to style elements: Tailwind CSS classes, inline styles, Quasar props, and custom CSS.

## .classes() - Tailwind CSS

Apply Tailwind CSS utility classes to any element:

```python
from nicegui import ui

# Text styling
ui.label('Title').classes('text-2xl font-bold text-blue-600')

# Spacing and layout
ui.card().classes('p-4 m-2 w-full max-w-md')

# Flexbox
ui.row().classes('gap-4 justify-between items-center')

# Background and borders
ui.label('Alert').classes('bg-red-100 border border-red-400 rounded p-2')

# Responsive design
ui.label('Responsive').classes('text-sm md:text-base lg:text-xl')
```

### Common Tailwind Classes

| Category | Examples |
|----------|----------|
| **Text** | `text-xl`, `font-bold`, `text-gray-500`, `text-center` |
| **Spacing** | `p-4`, `m-2`, `px-6`, `mt-4`, `gap-2` |
| **Width/Height** | `w-full`, `w-80`, `max-w-md`, `h-screen` |
| **Flexbox** | `flex`, `justify-between`, `items-center`, `gap-4` |
| **Background** | `bg-white`, `bg-gray-100`, `bg-blue-500` |
| **Border** | `border`, `rounded`, `rounded-lg`, `border-gray-300` |

## .style() - Inline CSS

Apply inline CSS for specific styling needs:

```python
from nicegui import ui

# Direct CSS properties
ui.label('Custom').style('color: red; font-size: 24px')

# Complex styling
ui.label('Gradient').style('''
    background: linear-gradient(90deg, #ff0000, #0000ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
''')

# Dynamic styling
size = 20
ui.label('Dynamic').style(f'font-size: {size}px')
```

### When to Use .style()

- CSS properties not available in Tailwind
- Gradients, transforms, animations
- Dynamic values computed at runtime
- Vendor-specific prefixes

## .props() - Quasar Properties

NiceGUI uses Quasar components. Use `.props()` for Quasar-specific styling:

```python
from nicegui import ui

# Button variants
ui.button('Outlined').props('outlined')
ui.button('Flat').props('flat')
ui.button('Round').props('round')

# Input styling
ui.input('Dense').props('dense filled')
ui.input('Outlined').props('outlined')

# Colors (Quasar color palette)
ui.button('Primary').props('color=primary')
ui.button('Negative').props('color=negative')

# Icons
ui.button(icon='home').props('flat round')
```

## ui.add_head_html() - Custom CSS

Add custom CSS rules to the page `<head>`:

```python
from nicegui import ui

# Add custom CSS
ui.add_head_html('''
<style>
    .my-custom-class {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .highlight:hover {
        transform: scale(1.05);
        transition: transform 0.2s;
    }
</style>
''')

# Use the custom class
ui.label('Custom Styled').classes('my-custom-class')
ui.card().classes('highlight')
```

## External CSS Files (Recommended)

For larger applications, use external CSS files:

### Setup Static Files

```python
from pathlib import Path
from nicegui import app, ui

# Serve static files
STATIC_DIR = Path(__file__).parent / 'static'
app.add_static_files('/static', STATIC_DIR)

def root():
    # Include CSS file
    ui.add_head_html('<link rel="stylesheet" href="/static/css/app.css">')
    # ... rest of page
```

### CSS File with Variables

```css
/* static/css/app.css */

/* CSS Variables for theming */
:root {
    --primary-color: #4f46e5;
    --primary-hover: #4338ca;
    --text-primary: #1e293b;
    --bg-primary: #ffffff;
    --border-color: #e2e8f0;
}

/* Dark mode overrides */
.body--dark {
    --text-primary: #f1f5f9;
    --bg-primary: #0f172a;
    --border-color: #334155;
}

/* Ensure full-width layouts */
.nicegui-content,
.nicegui-sub-pages,
.q-page,
.q-page-container {
    width: 100% !important;
    max-width: 100% !important;
}

/* Dashboard content max-width */
.dashboard-content {
    width: 100%;
    max-width: 1920px;
}

/* Custom component styles */
.login-card {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2rem;
}
```

### File Organization

```
my_app/
├── static/
│   ├── css/
│   │   └── app.css
│   └── js/
│       └── app.js
├── main.py
└── ...
```

### Global Styles

```python
from nicegui import ui

ui.add_head_html('''
<style>
    /* Override default styles */
    body {
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
</style>
''')
```

### Loading External Fonts

```python
from nicegui import ui

ui.add_head_html('''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    body { font-family: 'Inter', sans-serif; }
</style>
''')
```

## Full-Width Layout Fix

NiceGUI's default content container may have a max-width. Override with CSS:

```css
/* Ensure all layout containers fill available width */
.nicegui-content,
.nicegui-sub-pages,
.q-page,
.q-page-container {
    width: 100% !important;
    max-width: 100% !important;
}

/* Sub-pages content should also be full width */
.nicegui-sub-pages > * {
    width: 100%;
}
```

## ui.add_css() - Simpler CSS Addition

For just CSS (no full HTML), use `ui.add_css()`:

```python
from nicegui import ui

ui.add_css('''
    .card-hover:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
''')
```

## Combining Approaches

```python
from nicegui import ui

# Custom CSS for complex effects
ui.add_head_html('''
<style>
    .gradient-border {
        border: 3px solid transparent;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #667eea, #764ba2) border-box;
    }
</style>
''')

# Combine Tailwind + custom class + inline style
ui.card().classes('p-4 rounded-lg gradient-border').style('min-width: 300px')
```

## Dark Mode

```python
from nicegui import ui

# Enable dark mode
ui.dark_mode().enable()

# Or toggle
dark = ui.dark_mode()
ui.button('Toggle Dark', on_click=dark.toggle)

# Tailwind dark: prefix works automatically
ui.label('Adaptive').classes('text-black dark:text-white bg-white dark:bg-gray-800')
```

## Summary

| Method | Use Case |
|--------|----------|
| `.classes()` | Tailwind utilities, most common styling |
| `.style()` | Inline CSS, dynamic values, complex CSS |
| `.props()` | Quasar component properties |
| `ui.add_head_html()` | Custom CSS rules, fonts, global styles |
| `ui.add_css()` | Simple CSS additions |

## Documentation

- [Styling & Appearance](https://nicegui.io/documentation/section_styling_appearance)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Quasar Components](https://quasar.dev/vue-components)



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/background_execution.md -->

# Background Execution in NiceGUI

NiceGUI provides several mechanisms for running code in the background without blocking the UI. This document covers the key patterns and when to use each.

## Overview

| Method | Use Case | Blocks Event Loop | Thread Pool |
|--------|----------|-------------------|-------------|
| `run.io_bound()` | I/O or CPU-intensive sync functions | No | Yes |
| `run.cpu_bound()` | CPU-intensive work (process pool) | No | Process pool |
| `background_tasks.create()` | Fire-and-forget async tasks | No | No |
| `ui.timer()` | Periodic execution | No | No |
| `asyncio.create_task()` | Standard async task | No | No |

## Choosing Between io_bound and cpu_bound

### When to Use `run.io_bound()`

- **C++ Extension Libraries**: Libraries like **OpenCV**, **PIL/Pillow**, **NumPy**, and **pandas** do most of their heavy lifting in C/C++ code that releases the GIL. Using `run.io_bound()` is more efficient because:
  - No process boundary overhead (no pickling/unpickling)
  - Shared memory access (no data copying)
  - Lower latency for frequent calls
  
- **I/O Operations**: File reading, network requests, database queries

- **Example**: Video processing with OpenCV
  ```python
  def process_frame(frame):
      # OpenCV operations release the GIL
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      edges = cv2.Canny(gray, 100, 200)
      return edges
  
  result = await run.io_bound(process_frame, frame)
  ```

### When to Use `run.cpu_bound()`

- **Pure Python Computation**: When the bottleneck is Python code itself (loops, string processing, custom algorithms)
- **Small Data Transfer**: When data passed to/from the process is small (large objects must be pickled, which is slow)
- **Long-running Tasks**: Tasks that run for seconds or longer, where process startup overhead is negligible

- **Example**: Pure Python number crunching
  ```python
  def compute_primes(n):
      # Pure Python loop - holds the GIL
      primes = []
      for num in range(2, n):
          if all(num % p != 0 for p in primes):
              primes.append(num)
      return primes
  
  result = await run.cpu_bound(compute_primes, 100000)
  ```

### Decision Guide

```
Is the heavy work in C/C++ extensions (OpenCV, NumPy, PIL)?
  → Use run.io_bound()

Is it pure Python code AND data is small?
  → Use run.cpu_bound()

Is it I/O (file, network, database)?
  → Use run.io_bound()

Unsure?
  → Start with run.io_bound() (simpler, lower overhead)
```

## run.io_bound

Use `run.io_bound()` to run synchronous blocking functions in a thread pool without blocking the event loop.

### Basic Usage

```python
from nicegui import run

# Blocking function that would freeze the UI
def slow_operation(data: str) -> str:
    time.sleep(2)  # Simulates I/O or CPU work
    return f"Processed: {data}"

# Run in background thread
async def handle_click():
    result = await run.io_bound(slow_operation, "input data")
    ui.notify(result)
```

### Key Points

- **Returns a coroutine**: Must be awaited or wrapped in a task
- **Thread pool**: Uses Python's `ThreadPoolExecutor`
- **Arguments**: Pass function arguments after the function
- **Return value**: Returns whatever the function returns

### Non-blocking Pattern

To start work without waiting for completion:

```python
import asyncio
from nicegui import run

# Start without blocking
task = asyncio.create_task(run.io_bound(slow_function, arg1, arg2))

# Later, check if done
if task.done():
    result = task.result()
```

### With ui.timer for Polling

```python
class Worker:
    def __init__(self):
        self._pending_task = None
        self._timer = ui.timer(0.1, self._check_task)
    
    def start_work(self):
        if self._pending_task is None:
            self._pending_task = asyncio.create_task(
                run.io_bound(self._do_work)
            )
    
    def _check_task(self):
        if self._pending_task and self._pending_task.done():
            try:
                result = self._pending_task.result()
                # Handle result
            finally:
                self._pending_task = None
```

## background_tasks.create

Use `background_tasks.create()` for fire-and-forget async tasks that should run independently.

### Basic Usage

```python
from nicegui import background_tasks

async def long_running_task():
    await asyncio.sleep(10)
    print("Task completed")

# Fire and forget - no await needed
background_tasks.create(long_running_task())
```

### With run.io_bound

Combine for non-blocking background work:

```python
async def start_video_reader():
    await run.io_bound(read_video_loop, state, video_file)

# Start without blocking the page load
background_tasks.create(start_video_reader())
```

### Key Points

- **No await**: The task runs independently
- **Exception handling**: Exceptions are logged but don't crash the app
- **Lifecycle**: Tasks continue even if the creating context ends

## Thread-Safe State Sharing

When background threads need to share state with the UI thread, use locks:

```python
from dataclasses import dataclass, field
import threading

@dataclass
class SharedState:
    data: str | None = None
    is_running: bool = True
    lock: threading.Lock = field(default_factory=threading.Lock)

# Background thread writes
def background_worker(state: SharedState):
    while state.is_running:
        result = compute_something()
        with state.lock:
            state.data = result

# UI thread reads
def get_current_data(state: SharedState) -> str | None:
    with state.lock:
        return state.data
```

## Cleanup on Disconnect

Always clean up background tasks when the client disconnects:

```python
@ui.page('/')
def index():
    state = SharedState()
    state.is_running = True
    
    # Start background work
    background_tasks.create(start_worker(state))
    
    # Cleanup when client disconnects
    async def cleanup():
        state.is_running = False
    
    ui.context.client.on_disconnect(cleanup)
```

## Common Patterns

### Long-Running Video/Stream Processing

```python
def read_stream(state: StreamState):
    """Runs in background thread via run.io_bound."""
    while state.is_running:
        frame = capture_frame()
        with state.lock:
            state.current_frame = frame

@ui.page('/')
def index():
    state = StreamState()
    
    async def start():
        await run.io_bound(read_stream, state)
    
    background_tasks.create(start())
```

### Periodic Data Fetching

```python
async def fetch_data():
    while True:
        data = await run.io_bound(api_call)
        update_ui(data)
        await asyncio.sleep(5)

background_tasks.create(fetch_data())
```

### Request-Response with Timeout

```python
async def fetch_with_timeout():
    try:
        result = await asyncio.wait_for(
            run.io_bound(slow_api_call),
            timeout=10.0
        )
        return result
    except asyncio.TimeoutError:
        return None
```

## Anti-Patterns

### ❌ Blocking the Event Loop

```python
# BAD - blocks the entire UI
def handle_click():
    time.sleep(5)  # UI freezes!
    ui.notify("Done")
```

### ❌ Using asyncio.run() Inside Handlers

```python
# BAD - creates nested event loop
def handle_click():
    asyncio.run(some_coroutine())  # Error!
```

### ❌ Forgetting to Await run.io_bound

```python
# BAD - coroutine never executes
def handle_click():
    run.io_bound(slow_function)  # Returns coroutine, doesn't run!
```

### ❌ Accessing `self` or Instance State from Background Thread

```python
# BAD - race condition! self._value may change during execution
class MyComponent:
    def process(self):
        task = asyncio.create_task(run.io_bound(self._do_work))
    
    def _do_work(self):
        # DANGER: accessing self from background thread
        return self._value * 2  # Race condition!
```

### ✅ Correct Patterns

```python
# GOOD - await the coroutine
async def handle_click():
    result = await run.io_bound(slow_function)

# GOOD - create task for fire-and-forget
def handle_click():
    background_tasks.create(run.io_bound(slow_function))

# GOOD - create task and poll
def handle_click():
    task = asyncio.create_task(run.io_bound(slow_function))

# GOOD - capture values BEFORE entering background thread
class MyComponent:
    def process(self):
        # Capture all needed values on main thread
        value = self._value
        format_type = self._format
        
        # Pass captured values to static method
        task = asyncio.create_task(
            run.io_bound(MyComponent._do_work, value, format_type)
        )
    
    @staticmethod
    def _do_work(value: int, format_type: str) -> int:
        # Safe: no instance access, only uses passed arguments
        return value * 2
```

## Asyncio Context Issues

**Critical**: When using `asyncio.create_task()` directly, the task runs outside of any client's execution context. This means you **cannot access UI elements** from within the task - NiceGUI won't know which client to update.

### ❌ Problem: Lost Client Context

```python
async def fetch_and_update():
    data = await run.io_bound(slow_api_call)
    ui.notify(data)  # ERROR: No client context!

def handle_click():
    asyncio.create_task(fetch_and_update())  # Context lost!
```

### ✅ Solution 1: Use `ui.timer` with `once=True`

For delayed execution that preserves client context, use a one-shot timer:

```python
def handle_click():
    async def delayed_work():
        data = await run.io_bound(slow_api_call)
        ui.notify(data)  # Works! Timer preserves context
    
    # Execute immediately (0 delay) but within client context
    ui.timer(0, delayed_work, once=True)
```

### ✅ Solution 2: Use `background_tasks.create()`

NiceGUI's `background_tasks` preserves the client context:

```python
async def fetch_and_update():
    data = await run.io_bound(slow_api_call)
    ui.notify(data)  # Works! Context preserved

def handle_click():
    background_tasks.create(fetch_and_update())
```

### When to Use Each

| Method | Context Preserved | Use Case |
|--------|-------------------|----------|
| `ui.timer(0, fn, once=True)` | ✅ Yes | Deferred execution, UI updates |
| `background_tasks.create()` | ✅ Yes | Fire-and-forget with UI access |
| `asyncio.create_task()` | ❌ No | Only for non-UI background work |

## Race Conditions in Background Threads

**Critical**: Functions executed via `run.io_bound()` run in a separate thread. Accessing instance attributes (`self.xxx`) from these functions creates race conditions because:

1. The main thread may modify the attribute while the background thread reads it
2. The background thread may read partially-updated state
3. Multiple background tasks may interfere with each other

### Safe Pattern: Capture Before Thread

```python
def start_background_work(self):
    # 1. Capture all needed values on main thread (safe)
    callback = self._callback
    config = self._config
    data = self._data.copy()  # Copy mutable data!
    
    # 2. Pass as arguments to static/module-level function
    task = asyncio.create_task(
        run.io_bound(process_data, callback, config, data)
    )

def process_data(callback, config, data):
    """Static function - no self access, thread-safe."""
    result = callback(data)
    return format_result(result, config)
```

### What Can Be Safely Accessed

| Safe | Unsafe |
|------|--------|
| Function arguments | `self.xxx` attributes |
| Local variables | Global mutable state |
| Immutable data | Shared mutable objects |
| Thread-safe objects | UI elements |

## Performance Considerations

1. **Thread pool size**: Default pool has limited threads; don't saturate it
2. **Lock contention**: Keep critical sections short
3. **Memory**: Large data in shared state consumes memory
4. **Timer frequency**: Don't poll too frequently (5-100ms is usually fine)

## See Also

- [Custom Components](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/custom_components.md) - Building JS components that use background execution
- [Three.js Integration](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/threejs_integration.md) - Example of background rendering
- Sample: `samples/video_custom_component` - Complete example with video processing



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/custom_components.md -->

# Custom JavaScript/Vue Components

NiceGUI allows you to create custom UI components that combine Python and JavaScript/Vue.js. This enables wrapping existing JavaScript libraries or creating entirely custom interactive elements.

## Architecture Overview

NiceGUI components consist of:
1. **Python class** - Extends `Element`, handles server-side logic
2. **JavaScript/Vue module** - Handles client-side rendering and interaction
3. **Communication layer** - Props, events, and method calls between Python and JS

## Creating a Custom Component

### Basic Structure

```
my_component/
├── __init__.py           # Export the component
├── my_component.py       # Python class
└── my_component.js       # Vue component definition
```

### Python Side

Subclass `Element` and specify the JavaScript component file:

```python
from nicegui.element import Element

class MyCounter(Element, component='counter.js'):
    """A simple counter component."""
    
    def __init__(self, initial_value: int = 0) -> None:
        super().__init__()
        # Set props that will be passed to the Vue component
        self._props['count'] = initial_value
    
    def increment(self) -> None:
        """Increment the counter from Python."""
        self._props['count'] += 1
        self.update()  # Push changes to client
```

### JavaScript Side (Vue Component)

Create a Vue component module:

```javascript
// counter.js
export default {
  // HTML template
  template: `
    <div>
      <span>Count: {{ count }}</span>
      <button @click="increment">+</button>
    </div>
  `,
  
  // Props received from Python
  props: {
    count: Number,
  },
  
  // Component lifecycle
  mounted() {
    console.log('Component mounted');
  },
  
  unmounted() {
    console.log('Component unmounted');
  },
  
  // Methods callable from template or Python
  methods: {
    increment() {
      // Emit event to Python
      this.$emit('increment', this.count + 1);
    },
  },
};
```

## Class Registration Options

The `Element` subclass accepts several class-level parameters:

```python
class MyComponent(Element,
    component='my_component.js',           # Vue component file
    dependencies=['lib1.js', 'lib2.js'],   # Additional JS libraries
    esm={'module-name': 'dist'},           # ESM module mapping
    default_classes='my-component',        # Default CSS classes
    default_style='color: blue',           # Default inline styles
    default_props='outlined',              # Default Quasar props
):
    pass
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `component` | Path to the Vue component `.js` file (relative to Python file) |
| `dependencies` | List of additional JS/CSS files to load |
| `esm` | Dict mapping ESM module names to local paths for bundled libraries |
| `default_classes` | Default CSS classes applied to all instances |
| `default_style` | Default inline styles |
| `default_props` | Default Quasar props |

## Props (Python → JavaScript)

Props are the primary way to pass data from Python to JavaScript.

### Setting Props

```python
class MyComponent(Element, component='my_component.js'):
    def __init__(self, title: str, items: list) -> None:
        super().__init__()
        self._props['title'] = title
        self._props['items'] = items
    
    def set_title(self, title: str) -> None:
        self._props['title'] = title
        self.update()  # Required to push changes
```

### Receiving Props in JavaScript

```javascript
export default {
  props: {
    title: String,
    items: Array,
  },
  template: `<div>{{ title }}</div>`,
};
```

### Dynamic Props (JavaScript Expressions)

Props starting with `:` are evaluated as JavaScript:

```python
self._props[':onClick'] = 'console.log("clicked")'
self._props[':data'] = '{"key": "value"}'
```

## Events (JavaScript → Python)

Events allow the JavaScript component to communicate back to Python.

### Emitting Events from JavaScript

```javascript
methods: {
  handleClick(data) {
    // Emit event to Python
    this.$emit('my-event', { value: data });
  },
},
```

### Handling Events in Python

```python
class MyComponent(Element, component='my_component.js'):
    def __init__(self) -> None:
        super().__init__()
        # Register event handler
        self.on('my-event', self._handle_event)
    
    def _handle_event(self, e) -> None:
        print(f'Received: {e.args}')
```

### Custom Event Arguments

Define typed event arguments by inheriting from `UiEventArguments`:

```python
from dataclasses import dataclass
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.events import UiEventArguments

@dataclass(**KWONLY_SLOTS)
class MyEventArgs(UiEventArguments):
    """Custom event arguments.
    
    Inherits sender and client from UiEventArguments.
    """
    data: dict
```

### Event Handler Signature

```python
from nicegui.events import GenericEventArguments, Handler, handle_event
from typing_extensions import Self

def on_custom_event(self, callback: Handler[MyEventArgs]) -> Self:
    """Register a handler for custom events."""
    def handler(e: GenericEventArguments) -> None:
        args = MyEventArgs(sender=self, client=self.client, data=e.args)
        handle_event(callback, args)
    self.on('custom-event', handler)
    return self
```

## Methods (Python → JavaScript)

Call JavaScript methods from Python using `run_method()`.

### Python Side

```python
class MyComponent(Element, component='my_component.js'):
    def focus(self) -> AwaitableResponse:
        """Focus the component."""
        return self.run_method('focus')
    
    async def get_value(self) -> str:
        """Get value from JavaScript (async)."""
        return await self.run_method('getValue')
    
    def set_data(self, data: dict) -> None:
        """Call JS method with arguments."""
        self.run_method('setData', data)
```

### JavaScript Side

```javascript
methods: {
  focus() {
    this.$el.focus();
  },
  getValue() {
    return this.internalValue;
  },
  setData(data) {
    this.data = data;
  },
},
```

### Awaiting Results

`run_method()` returns an `AwaitableResponse`:

```python
# Fire and forget
self.run_method('doSomething')

# Wait for result
result = await self.run_method('getValue', timeout=2.0)
```

## JavaScript → Python Method Calls

Use `ui.run_javascript()` or emit events for complex communication:

```javascript
// In Vue component
methods: {
  async callPython() {
    // Emit event that Python handles
    this.$emit('request-data', { query: 'test' });
  },
},
```

## Vue Component Lifecycle

### Lifecycle Hooks

```javascript
export default {
  template: '<div ref="container"></div>',
  
  // Before component is mounted
  beforeMount() {
    // Initialize state
  },
  
  // After component is mounted to DOM
  mounted() {
    // Access DOM: this.$el, this.$refs.container
    // Initialize third-party libraries
    this.chart = new Chart(this.$refs.container);
  },
  
  // Before component is updated
  beforeUpdate() {
    // Save state before re-render
  },
  
  // After component is updated
  updated() {
    // React to prop changes
  },
  
  // Before component is unmounted
  beforeUnmount() {
    // Start cleanup
  },
  
  // After component is unmounted
  unmounted() {
    // Final cleanup
    this.chart?.destroy();
  },
};
```

### Watching Props

```javascript
export default {
  props: {
    data: Object,
  },
  watch: {
    data: {
      handler(newVal, oldVal) {
        this.updateChart(newVal);
      },
      deep: true,  // Watch nested changes
    },
  },
};
```

## Loading External Libraries

### ESM Modules

For bundled npm packages:

```python
class MyChart(Element,
    component='chart.js',
    esm={'my-chart-lib': 'dist'}  # Maps import name to local path
):
    pass
```

```javascript
// chart.js
import { Chart } from 'my-chart-lib';

export default {
  mounted() {
    this.chart = new Chart(this.$el);
  },
};
```

### Adding Resources

For CSS and other static files:

```python
from pathlib import Path

class MyComponent(Element, component='my_component.js'):
    def __init__(self) -> None:
        super().__init__()
        self.add_resource(Path(__file__).parent / 'dist')
```

Access in JavaScript:

```javascript
import { loadResource } from '../../static/utils/resources.js';

export default {
  async mounted() {
    await loadResource(window.path_prefix + `${this.resource_path}/styles.css`);
  },
  props: {
    resource_path: String,
  },
};
```

## Complete Example: Terminal Wrapper

Here's how NiceGUI wraps xterm.js:

### Python (xterm.py)

```python
from pathlib import Path
from nicegui.element import Element
from nicegui.events import GenericEventArguments, handle_event

class Xterm(Element, component='xterm.js', esm={'nicegui-xterm': 'dist'}):
    
    def __init__(self, options: dict | None = None) -> None:
        super().__init__()
        self.add_resource(Path(__file__).parent / 'dist')
        self._props['options'] = options or {}
    
    def on_data(self, callback) -> Self:
        """Handle user input."""
        def handle(e: GenericEventArguments) -> None:
            handle_event(callback, XtermDataEventArgs(
                sender=self, client=self.client, data=e.args
            ))
        self.on('data', handle)
        return self
    
    def write(self, data: str) -> AwaitableResponse:
        """Write data to terminal."""
        return self.run_method('write', data)
    
    async def get_rows(self) -> int:
        """Get terminal rows."""
        return await self.run_method('getRows')
```

### JavaScript (xterm.js)

```javascript
import { Terminal, FitAddon } from 'nicegui-xterm';
import { loadResource } from '../../static/utils/resources.js';

export default {
  template: '<div></div>',
  
  props: {
    options: Object,
    resource_path: String,
  },
  
  mounted() {
    // Create terminal
    this.terminal = new Terminal(this.options);
    this.terminal.loadAddon(this.fit_addon = new FitAddon());
    this.terminal.open(this.$el);
    
    // Re-emit terminal events to Vue/Python
    Object.getOwnPropertyNames(Object.getPrototypeOf(this.terminal))
      .filter(key => key.startsWith('on') && typeof this.terminal[key] === 'function')
      .forEach(key => {
        this.terminal[key](e => this.$emit(key.slice(2).toLowerCase(), e));
      });
    
    // Load CSS
    this.$nextTick().then(() => 
      loadResource(window.path_prefix + `${this.resource_path}/xterm.css`)
    );
  },
  
  methods: {
    getRows() {
      return this.terminal.rows;
    },
    fit() {
      this.fit_addon.fit();
    },
    write(data) {
      return this.terminal.write(data);
    },
  },
};
```

## Development Setup

Enable hot-reloading of JavaScript, CSS, and HTML files during development:

```python
ui.run(reload=True, uvicorn_reload_includes='*.js,*.css,*.html')
```

This watches your component files for changes and automatically reloads the browser.

## Dynamic Route Registration

Components that need server endpoints (like file uploads) can register routes dynamically at runtime.

### Registering Routes

```python
from nicegui import app
from nicegui.element import Element

class MyUploader(Element, component='uploader.js'):
    def __init__(self) -> None:
        super().__init__()
        # Build unique URL using client and element IDs
        self._props['url'] = f'/_nicegui/client/{self.client.id}/upload/{self.id}'
        
        # Register the route dynamically
        @app.post(self._props['url'])
        async def upload_route(request: Request) -> dict:
            # Handle the upload...
            return {'status': 'success'}
```

### URL Pattern Guidelines

| Pattern | Example | Use Case |
|---------|---------|----------|
| `/_nicegui/client/{client_id}/{action}/{element_id}` | `/_nicegui/client/abc123/upload/42` | Per-client, per-element endpoints |
| `/_nicegui/auto/static/{hash}/{filename}` | `/_nicegui/auto/static/def456/file.pdf` | Auto-generated static files |

**Important**: Always use the `/_nicegui/` prefix for dynamic routes to avoid conflicts with user-defined pages and the root page fallback.

### Cleaning Up Routes

Always remove routes when the element is deleted to prevent memory leaks:

```python
class MyUploader(Element, component='uploader.js'):
    def __init__(self) -> None:
        super().__init__()
        self._props['url'] = f'/_nicegui/client/{self.client.id}/upload/{self.id}'
        
        @app.post(self._props['url'])
        async def upload_route(request: Request) -> dict:
            return {'status': 'success'}
    
    def _handle_delete(self) -> None:
        # Remove the route when element is deleted
        app.remove_route(self._props['url'])
        super()._handle_delete()
```

### Why Dynamic Routes Work with Root Pages

Dynamic routes are registered as real FastAPI routes, which are matched **before** the 404 handler that serves root pages. This means:

1. Request to `/_nicegui/client/.../upload/...` → matches the dynamic route
2. Request to `/any/other/path` → no match → 404 handler → root page (if defined)

See [Routing Architecture](https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/routing.md) for details on route precedence.

## Best Practices

1. **Cleanup in unmounted** - Always destroy third-party library instances
2. **Use props for data flow** - Avoid direct DOM manipulation when possible
3. **Emit events for user actions** - Let Python handle business logic
4. **Bundle dependencies** - Use ESM for npm packages
5. **Handle async initialization** - Use `mounted()` for setup that needs DOM
6. **Validate props** - Define prop types in JavaScript
7. **Clean up dynamic routes** - Always call `app.remove_route()` in `_handle_delete()`

## Debugging

### Browser Console

```javascript
// Access component instance
getElement(123)  // By element ID

// Check props
getElement(123).count
```

### Python Side

```python
# Check current props
print(element._props)

# Force update
element.update()
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/threejs_integration.md -->

# Three.js Integration

NiceGUI includes a bundled Three.js library (`nicegui-scene`) that you can use for custom 3D visualizations beyond the basic `ui.scene` component.

## Basic Setup

Create a custom element that imports from `nicegui-scene`:

```python
# threejs_scene.py
from nicegui.element import Element

class ThreeJSScene(Element, component='threejs_scene.js'):
    """Custom Three.js scene component."""
    
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            self._props[key] = value
    
    def update_settings(self, settings: dict) -> None:
        """Send settings to JavaScript."""
        self.run_method('updateSettings', settings)
```

## JavaScript Component

Import Three.js from NiceGUI's bundled module:

```javascript
// threejs_scene.js
import SceneLib from "nicegui-scene";
const { THREE, OrbitControls } = SceneLib;

export default {
  template: `<div ref="container" style="width: 100%; height: 100%;"></div>`,
  
  props: {
    // Define your props here
  },
  
  mounted() {
    this.initScene();
    this.animate();
  },
  
  methods: {
    initScene() {
      // Setup Three.js scene, camera, renderer
    },
    animate() {
      requestAnimationFrame(() => this.animate());
      // Render loop
    }
  }
};
```

## Critical: Vue Reactivity Conflict

**Problem**: Vue wraps objects in reactive proxies, but Three.js objects have non-configurable properties that break when proxied.

**Error message**:
```
TypeError: 'get' on proxy: property 'modelViewMatrix' is a read-only 
and non-configurable data property on the proxy target but the proxy 
did not return its actual value
```

**Solution**: Store Three.js objects outside Vue's reactivity system using a `WeakMap`:

```javascript
import SceneLib from "nicegui-scene";
const { THREE, OrbitControls } = SceneLib;

// Store Three.js objects outside Vue reactivity
const threeState = new WeakMap();

export default {
  data() {
    return {
      // Only store simple values here, NOT Three.js objects
      isPaused: false,
      settings: {},
    };
  },

  mounted() {
    // Initialize non-reactive Three.js state
    threeState.set(this, {
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      clock: null,
    });
    
    this.$nextTick(() => {
      this.initScene();
      this.animate();
    });
  },

  methods: {
    // Helper to access Three.js state
    getState() {
      return threeState.get(this);
    },
    
    initScene() {
      const state = this.getState();
      const container = this.$refs.container;
      
      state.scene = new THREE.Scene();
      state.camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
      state.renderer = new THREE.WebGLRenderer({ antialias: true });
      state.renderer.setSize(container.clientWidth, container.clientHeight);
      container.appendChild(state.renderer.domElement);
      
      state.controls = new OrbitControls(state.camera, state.renderer.domElement);
      state.clock = new THREE.Clock();
    },
    
    animate() {
      requestAnimationFrame(() => this.animate());
      const state = this.getState();
      if (!state || !state.renderer) return;
      
      state.controls.update();
      state.renderer.render(state.scene, state.camera);
    }
  }
};
```

## Custom Shaders

Three.js ShaderMaterial works with the bundled version:

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color(0xff6600) },
  },
  vertexShader: `
    varying vec3 vPosition;
    void main() {
      vPosition = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform vec3 uColor;
    varying vec3 vPosition;
    void main() {
      gl_FragColor = vec4(uColor, 1.0);
    }
  `,
  transparent: true,
  blending: THREE.AdditiveBlending,
});
```

**Note**: When using `vertexColors: true`, do NOT declare `attribute vec3 color` in your shader - Three.js adds it automatically. Declaring it causes:
```
ERROR: 0:72: 'color' : redefinition
```

## Full-Screen Layout

To prevent scrollbars in full-screen 3D scenes:

```python
ui.add_head_html('''<style>
    html, body { 
        margin: 0; 
        padding: 0; 
        overflow: hidden;
        background-color: #000 !important; 
    }
    .nicegui-content { 
        padding: 0 !important;
        overflow: hidden;
    }
    .q-page { padding: 0 !important; }
</style>''')

with ui.element('div').classes('w-full h-screen relative'):
    scene = ThreeJSScene().classes('absolute inset-0')
```

## Python → JavaScript Communication

Use `run_method` to call JavaScript methods:

```python
class ThreeJSScene(Element, component='threejs_scene.js'):
    def update_settings(self, settings: dict) -> None:
        self.run_method('updateSettings', settings)
    
    def reset_camera(self) -> None:
        self.run_method('resetCamera')
```

```javascript
methods: {
  updateSettings(settings) {
    const state = this.getState();
    // Update uniforms, recreate geometry, etc.
  },
  
  resetCamera() {
    const state = this.getState();
    state.camera.position.set(0, 5, 15);
    state.controls.target.set(0, 0, 0);
  }
}
```

## Available Three.js Exports

The `nicegui-scene` module exports:

```javascript
import SceneLib from "nicegui-scene";
const {
  THREE,           // Full Three.js library
  OrbitControls,   // Camera controls
  DragControls,    // Object dragging
  CSS2DRenderer,   // 2D labels
  CSS3DRenderer,   // 3D CSS elements
  GLTFLoader,      // GLTF model loader
  STLLoader,       // STL model loader
  TWEEN,           // Animation tweening
  Stats,           // Performance stats
} = SceneLib;
```

## Common Pitfalls

1. **Don't use external CDN imports** - Use the bundled `nicegui-scene` module
2. **Don't store Three.js objects in Vue `data()`** - Use WeakMap pattern
3. **Don't redeclare `color` attribute** with `vertexColors: true`
4. **Wait for `$nextTick`** before accessing `$refs.container` dimensions
5. **Check for null state** in animate loop (component may unmount)

## Example: Particle System

See `samples/threejs_tornado/` for a complete example with:
- 15,000+ animated particles
- Custom GLSL vertex/fragment shaders
- Real-time parameter controls
- Additive blending for glow effects
- OrbitControls for camera interaction



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/configuration_deployment.md -->

# Configuration & Deployment

## ui.run() Parameters

The `ui.run()` function starts the NiceGUI server with various configuration options:

```python
from nicegui import ui

ui.label('Hello World')

ui.run(
    host='0.0.0.0',
    port=8080,
    title='My App',
    reload=True,
)
```

### Core Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `host` | `'127.0.0.1'` | Host to bind to (`'0.0.0.0'` for all interfaces) |
| `port` | `8080` | Port to bind to |
| `title` | `'NiceGUI'` | Page title shown in browser tab |
| `favicon` | `None` | Path to favicon, emoji, SVG, or base64 image |
| `dark` | `None` | Dark mode (`True`, `False`, or `None` for auto) |
| `language` | `'en-US'` | Quasar language pack |
| `show` | `True` | Open browser automatically on startup |

### Development Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `reload` | `True` | Auto-reload on Python file changes |
| `uvicorn_reload_dirs` | cwd | Comma-separated directories to watch |
| `uvicorn_reload_includes` | `'*.py'` | Glob patterns that trigger reload |
| `uvicorn_reload_excludes` | `'.*, .py[cod], .sw.*, ~*'` | Glob patterns to ignore |
| `uvicorn_logging_level` | `'warning'` | Uvicorn log level |

### Port Conflicts

If you see `Address already in use` errors, **do not change the port**. Instead, kill the existing process:

```bash
# Kill process using port 8080
lsof -ti :8080 | xargs kill
```

Changing ports leads to confusion with multiple servers running simultaneously.

**Tip:** For custom component development, include JS/CSS/HTML files:

```python
ui.run(reload=True, uvicorn_reload_includes='*.py,*.js,*.css,*.html')
```

### Storage & Security

| Parameter | Default | Description |
|-----------|---------|-------------|
| `storage_secret` | `None` | Secret for browser storage (required for `ui.storage.browser`) |
| `session_middleware_kwargs` | `{}` | Additional SessionMiddleware options |

### Connection Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `binding_refresh_interval` | `0.1` | Seconds between binding updates |
| `reconnect_timeout` | `3.0` | Max seconds to wait for browser reconnect |
| `message_history_length` | `1000` | Messages stored for reconnection (0 to disable) |

### Native Window Mode

| Parameter | Default | Description |
|-----------|---------|-------------|
| `native` | `False` | Open in native window instead of browser |
| `window_size` | `None` | Native window size, e.g., `(1024, 768)` |
| `fullscreen` | `False` | Open in fullscreen native window |
| `frameless` | `False` | Remove window frame |

```python
# Native desktop app
ui.run(native=True, window_size=(1200, 800))
```

### SSL/HTTPS

```python
ui.run(
    port=443,
    ssl_certfile='/path/to/cert.pem',
    ssl_keyfile='/path/to/key.pem',
)
```

### Other Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `tailwind` | `True` | Enable Tailwind CSS |
| `prod_js` | `True` | Use production Vue/Quasar builds |
| `on_air` | `False` | Enable NiceGUI On Air remote access |
| `show_welcome_message` | `True` | Show startup message |
| `fastapi_docs` | `False` | Enable FastAPI Swagger/ReDoc |
| `endpoint_documentation` | `'none'` | OpenAPI docs (`'none'`, `'internal'`, `'page'`, `'all'`) |
| `cache_control_directives` | long cache | Cache headers for static files |

## Favicon Options

### Emoji Favicon

```python
ui.run(favicon='🚀')
```

### SVG Favicon

```python
smiley = '''
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <circle cx="100" cy="100" r="78" fill="#ffde34"/>
</svg>
'''
ui.run(favicon=smiley)
```

### Base64 Favicon

```python
icon = 'data:image/png;base64,iVBORw0KGgo...'
ui.run(favicon=icon)
```

## Server Hosting

### Direct Deployment

```python
# Production settings
ui.run(
    host='0.0.0.0',
    port=80,
    reload=False,
    show=False,
)
```

### Docker Deployment

Use the official NiceGUI Docker image:

```bash
docker run -it --restart always \
    -p 80:8080 \
    -e PUID=$(id -u) \
    -e PGID=$(id -g) \
    -v $(pwd)/:/app/ \
    zauberzeug/nicegui:latest
```

Or with docker-compose:

```yaml
app:
    image: zauberzeug/nicegui:latest
    restart: always
    ports:
        - 80:8080
    environment:
        - PUID=1000
        - PGID=1000
    volumes:
        - ./:/app/
```

### Reverse Proxy (NGINX)

For production, use a reverse proxy like NGINX or Traefik to handle SSL termination.

## Packaging with PyInstaller

Bundle your app as a standalone executable:

```python
# main.py
from nicegui import native, ui

def root():
    ui.label('Hello from PyInstaller')

ui.run(root, reload=False, port=native.find_open_port())
```

```bash
nicegui-pack --onefile --name "myapp" main.py
```

### Packaging Options

| Option | Description |
|--------|-------------|
| `--onefile` | Single executable (slower startup) |
| `--onedir` | Directory with executable (faster startup) |
| `--windowed` | No console window (use with `native=True`) |

### macOS Packaging

Add at the top of your main file:

```python
from multiprocessing import freeze_support  # noqa
freeze_support()  # noqa

# rest of your code
```

## NiceGUI On Air

Share your local app over the internet:

```python
# Random URL (1 hour)
ui.run(on_air=True)

# Fixed URL with token from https://on-air.nicegui.io
ui.run(on_air='<your-token>')
```

## Custom Startup Handler

```python
from nicegui import app, ui

ui.label('My App')

app.on_startup(lambda: print('URLs:', app.urls))

ui.run(show_welcome_message=False)
```

## Environment-Based Configuration

```python
import os
from nicegui import ui

ui.run(
    host=os.getenv('HOST', '127.0.0.1'),
    port=int(os.getenv('PORT', 8080)),
    reload=os.getenv('ENV') == 'development',
    storage_secret=os.getenv('STORAGE_SECRET'),
)
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/mechanics/coding_style.md -->

# NiceGUI Coding Style Guide

This document describes the coding conventions used in the NiceGUI codebase. Follow these patterns when writing NiceGUI applications and custom components.

## Line Length and Formatting

- **Max line length**: ~120 characters (flexible, readability over strict limits)
- **Imports**: One import per line for `from` imports, grouped by stdlib → third-party → local
- **String quotes**: Single quotes `'` for strings (not double quotes `"`)
- **Trailing commas**: Used in multi-line collections and function signatures

## Type Hints

NiceGUI uses comprehensive type hints throughout:

```python
from typing import Any, Callable, Optional, Union
from typing_extensions import Self

def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
    """Add a callback to be invoked when the button is clicked."""
    ...
    return self
```

### Common Patterns

- `Optional[X]` for nullable parameters
- `Self` for method chaining return types
- `TypeVar` for generic functions
- `ClassVar` for class-level attributes
- `TYPE_CHECKING` block for import-only types (avoids circular imports)

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
    from .element import Element
```

## Docstrings

**Sphinx-style with `:param:` syntax**:

```python
def __init__(self,
             label: Optional[str] = None, *,
             placeholder: Optional[str] = None,
             value: str = '',
             on_change: Optional[Handler[ValueChangeEventArguments]] = None,
             ) -> None:
    """Text Input

    This element is based on Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component.
    The `on_change` event is called on every keystroke and the value updates accordingly.

    :param label: displayed label for the text input
    :param placeholder: text to show if no value is entered
    :param value: the current value of the text input
    :param on_change: callback to execute when the value changes
    """
```

### Docstring Guidelines

- First line: Brief description of the class/method
- Reference Quasar docs with RST link syntax: `` `QBtn <url>`_ ``
- Document all parameters with `:param name: description`
- Note version additions: `(*added in version 2.9.0*)`

## Class Structure

### Mixin-Based Composition

```python
class Button(IconElement, TextElement, DisableableElement, BackgroundColorElement):
    pass

class Input(LabelElement, ValidationElement, DisableableElement, component='input.js'):
    VALUE_PROP: str = 'value'
    LOOPBACK = False
```

### Class Variables

```python
class Element:
    component: Component | None = None
    exposed_libraries: ClassVar[list[Library]] = []
    _default_props: ClassVar[dict[str, Any]] = {}
    _default_classes: ClassVar[list[str]] = []
```

- Use `ClassVar` for class-level attributes
- Prefix private attributes with `_`
- Use UPPER_CASE for class constants

## Method Signatures

### Keyword-Only Arguments After `*`

```python
def __init__(self,
             text: str = '', *,
             on_click: Optional[Handler[ClickEventArguments]] = None,
             color: Optional[str] = 'primary',
             icon: Optional[str] = None,
             ) -> None:
```

- Positional args before `*`
- Keyword-only args after `*`
- Trailing comma on last parameter

### Method Chaining with `Self`

```python
def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
    """Add a callback..."""
    self.on('click', lambda _: handle_event(callback, ...), [])
    return self
```

## Dataclasses

Use `@dataclass` with `**KWONLY_SLOTS` for event arguments:

```python
from dataclasses import dataclass
from .dataclasses import KWONLY_SLOTS

@dataclass(**KWONLY_SLOTS)
class ClickEventArguments(UiEventArguments):
    pass

@dataclass(**KWONLY_SLOTS)
class ValueChangeEventArguments(UiEventArguments):
    value: Any
```

## WeakRef for Circular References

```python
self._client = weakref.ref(client)
self._parent_slot: weakref.ref[Slot] | None = None

@property
def client(self) -> Client:
    client = self._client()
    if client is None:
        raise RuntimeError('The client has been deleted.')
    return client
```

## Linter Directives

When necessary, use inline comments for linter suppression:

```python
global process_pool  # pylint: disable=global-statement # noqa: PLW0603
cast(Self, sender)._handle_value_change(value)  # pylint: disable=protected-access
```

## Import Organization

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import asyncio
from typing import Any, Optional

# 3. Third-party
from typing_extensions import Self

# 4. Local imports (relative)
from . import core, helpers
from .element import Element
from .events import Handler, ClickEventArguments
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `ValueElement`, `ClickEventArguments` |
| Functions/Methods | snake_case | `on_value_change`, `handle_event` |
| Constants | UPPER_SNAKE | `VALUE_PROP`, `LOOPBACK` |
| Private | `_` prefix | `_props`, `_handle_change` |
| Module-private | `_` prefix | `_running_tasks` |

## Error Handling

```python
@property
def client(self) -> Client:
    client = self._client()
    if client is None:
        raise RuntimeError('The client this element belongs to has been deleted.')
    return client
```

- Use `RuntimeError` for programming errors
- Provide descriptive error messages
- Check for None/deleted references before use

## Async Patterns

```python
async def _invoke_callback(self) -> None:
    try:
        result = self.callback()
        if isinstance(result, Awaitable) and not isinstance(result, AwaitableResponse):
            await result
    except Exception as e:
        core.app.handle_exception(e)
```

- Check if result is `Awaitable` before awaiting
- Forward exceptions to central handler
- Use `asyncio.create_task()` for fire-and-forget (but prefer `background_tasks.create()`)



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/events/value_events.md -->

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



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/events/button_events.md -->

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



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/events/element_events.md -->

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



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/events/lifecycle_events.md -->

# Lifecycle Events

Application and client lifecycle hooks.

## Application Lifecycle

### on_startup
Called once when the app starts:

```python
from nicegui import app, ui

@app.on_startup
async def startup():
    print('App starting...')
    # Initialize database, load config, etc.
```

### on_shutdown
Called once when the app stops:

```python
@app.on_shutdown
async def shutdown():
    print('App shutting down...')
    # Close connections, save state, etc.
```

## Client Lifecycle

### on_connect
Called when a client connects (including reconnects):

```python
@app.on_connect
async def connect():
    print('Client connected')
    # Initialize client-specific state
```

### on_disconnect
Called when a client disconnects:

```python
@app.on_disconnect
async def disconnect():
    print('Client disconnected')
    # Cleanup client resources
```

### on_delete
Called when a client is deleted (no reconnect expected):

```python
@app.on_delete
async def delete():
    print('Client deleted')
    # Final cleanup
```

## Exception Handlers

### on_exception
Called on any exception:

```python
@app.on_exception
async def handle_exception(e):
    print(f'Exception: {e}')
    # Log error, notify admin, etc.
```

### on_page_exception
Called when exception occurs during page build:

```python
@app.on_page_exception
async def handle_page_exception(e):
    ui.label(f'Error: {e}').classes('text-red-500')
```

## Timer Events

Periodic or delayed execution:

```python
from nicegui import ui

# Periodic timer
def update():
    label.text = str(datetime.now())

label = ui.label()
timer = ui.timer(1.0, update)  # Every 1 second

# One-shot timer
ui.timer(5.0, lambda: ui.notify('5 seconds passed'), once=True)

# Control timer
timer.active = False  # Pause
timer.active = True   # Resume
timer.cancel()        # Stop permanently
```

## Page Load Events

```python
@ui.page('/')
async def index():
    # This runs when page is requested
    ui.label('Loading...')
    
    # Use timer for post-load actions
    async def on_load():
        data = await fetch_data()
        container.clear()
        with container:
            ui.label(f'Data: {data}')
    
    container = ui.column()
    ui.timer(0.1, on_load, once=True)
```

## Documentation

- [Lifecycle](https://nicegui.io/documentation/section_configuration_deployment)
- [Timer](https://nicegui.io/documentation/timer)



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/events/keyboard_events.md -->

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



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/events/upload_events.md -->

# Upload Events

File upload handling.

## on_upload Event

Fires when a file is uploaded:

```python
from nicegui import ui

def handle_upload(e):
    ui.notify(f'Uploaded: {e.name}')
    content = e.content.read()  # File bytes
    # Process file...

# Constructor style
ui.upload(on_upload=handle_upload)

# Method style (post-constructor)
upload = ui.upload()
upload.on_upload(handle_upload)
```

## Upload Event Properties

```python
def handler(e):
    e.name      # Original filename
    e.type      # MIME type (e.g., 'image/png')
    e.content   # SpooledTemporaryFile (file-like object)
    e.sender    # The upload element
```

## Multiple Files

```python
def handle_uploads(e):
    ui.notify(f'Uploaded: {e.name}')

ui.upload(multiple=True, on_upload=handle_uploads)
# on_upload fires once per file
```

## Auto Upload

Upload immediately when file is selected:

```python
ui.upload(auto_upload=True, on_upload=handler)
```

## File Type Restrictions

```python
# Accept only images
ui.upload(on_upload=handler).props('accept=".jpg,.png,.gif,image/*"')

# Accept only PDFs
ui.upload(on_upload=handler).props('accept=".pdf,application/pdf"')
```

## Max File Size

```python
# Limit to 5MB
ui.upload(on_upload=handler, max_file_size=5_000_000)
```

## Upload Progress

```python
upload = ui.upload(on_upload=handler)

# Show progress
progress = ui.linear_progress(value=0)

def update_progress(e):
    progress.value = e.progress

upload.on('progress', update_progress)
```

## Rejected Files

```python
def on_rejected(e):
    ui.notify(f'Rejected: {e.name} - {e.reason}', type='warning')

ui.upload(
    on_upload=handler,
    on_rejected=on_rejected,
    max_file_size=1_000_000,
)
```

## Common Patterns

### Image Preview
```python
import base64

def show_preview(e):
    content = e.content.read()
    b64 = base64.b64encode(content).decode()
    image.source = f'data:{e.type};base64,{b64}'

image = ui.image().classes('w-64')
ui.upload(on_upload=show_preview).props('accept="image/*"')
```

### Save to Disk
```python
from pathlib import Path

UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(e):
    path = UPLOAD_DIR / e.name
    path.write_bytes(e.content.read())
    ui.notify(f'Saved: {path}')

ui.upload(on_upload=save_file)
```

## Documentation

- [Upload](https://nicegui.io/documentation/upload)



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/controls.md -->

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



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/layout.md -->

# NiceGUI Layout Elements

Elements for structuring and organizing the UI.

## Container Classes

| Class | Description |
|-------|-------------|
| `ui.card` | Card container |
| `ui.card_section` | Section within card |
| `ui.card_actions` | Actions area in card |
| `ui.column` | Vertical flex container |
| `ui.row` | Horizontal flex container |
| `ui.grid` | CSS grid container |
| `ui.list` | List container |
| `ui.item` | List item |
| `ui.item_section` | Section within list item |
| `ui.item_label` | Label within list item |
| `ui.expansion` | Expandable/collapsible panel |
| `ui.scroll_area` | Scrollable container |
| `ui.splitter` | Resizable split panels |

## Navigation Classes

| Class | Description |
|-------|-------------|
| `ui.tabs` | Tab container |
| `ui.tab` | Individual tab |
| `ui.tab_panels` | Tab panel container |
| `ui.tab_panel` | Individual tab panel |
| `ui.stepper` | Step wizard |
| `ui.step` | Individual step |
| `ui.stepper_navigation` | Stepper navigation buttons |
| `ui.carousel` | Image/content carousel |
| `ui.carousel_slide` | Carousel slide |
| `ui.pagination` | Pagination control |
| `ui.menu` | Dropdown menu |
| `ui.menu_item` | Menu item |
| `ui.context_menu` | Right-click context menu |

## Page Layout Classes

| Class | Description |
|-------|-------------|
| `ui.header` | Page header |
| `ui.footer` | Page footer |
| `ui.drawer` | Side drawer |
| `ui.left_drawer` | Left side drawer |
| `ui.right_drawer` | Right side drawer |
| `ui.page_sticky` | Sticky positioned element |
| `ui.page_scroller` | Page scroll button |

## Utility Classes

| Class | Description |
|-------|-------------|
| `ui.separator` | Visual separator line |
| `ui.space` | Flexible spacer |
| `ui.skeleton` | Loading skeleton placeholder |
| `ui.slide_item` | Swipeable list item |
| `ui.fullscreen` | Fullscreen control |
| `ui.teleport` | Move element in DOM |
| `ui.timeline` | Timeline display |
| `ui.timeline_entry` | Timeline entry |
| `ui.tooltip` | Tooltip popup |
| `ui.dialog` | Modal dialog |
| `ui.notification` | Notification element |

## Examples

### Basic Containers
```python
with ui.row():
    ui.label('Left')
    ui.label('Right')

with ui.column():
    ui.label('Top')
    ui.label('Bottom')

with ui.grid(columns=3):
    for i in range(9):
        ui.label(f'Cell {i}')
```

### Card
```python
with ui.card():
    ui.label('Card Title').classes('text-xl')
    ui.label('Card content')
    with ui.card_actions():
        ui.button('Action')
```

### Page Layout
```python
with ui.header():
    ui.label('My App').classes('text-xl')

with ui.left_drawer():
    ui.link('Home', '/')
    ui.link('About', '/about')

with ui.footer():
    ui.label('© 2024')
```

### Tabs
```python
with ui.tabs() as tabs:
    tab1 = ui.tab('Tab 1')
    tab2 = ui.tab('Tab 2')

with ui.tab_panels(tabs, value=tab1):
    with ui.tab_panel(tab1):
        ui.label('Content 1')
    with ui.tab_panel(tab2):
        ui.label('Content 2')
```

### Stepper
```python
with ui.stepper() as stepper:
    with ui.step('Step 1'):
        ui.label('First step')
        with ui.stepper_navigation():
            ui.button('Next', on_click=stepper.next)
    with ui.step('Step 2'):
        ui.label('Second step')
        with ui.stepper_navigation():
            ui.button('Back', on_click=stepper.previous)
            ui.button('Done')
```

### Dialog
```python
with ui.dialog() as dialog:
    with ui.card():
        ui.label('Dialog content')
        ui.button('Close', on_click=dialog.close)

ui.button('Open', on_click=dialog.open)
```

### Expansion
```python
with ui.expansion('Click to expand'):
    ui.label('Hidden content')
```

### Splitter
```python
with ui.splitter() as splitter:
    with splitter.before:
        ui.label('Left panel')
    with splitter.after:
        ui.label('Right panel')
```

### Menu
```python
with ui.button('Menu'):
    with ui.menu():
        ui.menu_item('Item 1', on_click=lambda: print('1'))
        ui.menu_item('Item 2', on_click=lambda: print('2'))
```

### Context Menu
```python
with ui.label('Right-click me'):
    with ui.context_menu():
        ui.menu_item('Copy')
        ui.menu_item('Paste')
```

### Tooltip
```python
ui.button('Hover me').tooltip('This is a tooltip')
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/text_elements.md -->

# NiceGUI Text Elements

Elements for displaying text and formatted content.

## Classes

| Class | Description |
|-------|-------------|
| `ui.label` | Display text |
| `ui.link` | Hyperlink element |
| `ui.link_target` | Anchor target for navigation |
| `ui.chat_message` | Chat-style message bubble |
| `ui.element` | Generic HTML element |
| `ui.markdown` | Render Markdown content |
| `ui.restructured_text` | Render reStructuredText |
| `ui.mermaid` | Render Mermaid diagrams |
| `ui.html` | Raw HTML content |

## Examples

### Label
```python
ui.label('Hello World')
ui.label('Styled').classes('text-2xl text-blue-500')
```

### Link
```python
ui.link('Go to NiceGUI', 'https://nicegui.io')
ui.link('Internal', '/about')
```

### Markdown
```python
ui.markdown('# Heading\n\nSome **bold** text')
ui.markdown('''
    ## Code Example
    ```python
    print("Hello")
    ```
''')
```

### Chat Message
```python
ui.chat_message('Hello!', name='User', sent=True)
ui.chat_message('Hi there!', name='Bot', avatar='🤖')
```

### HTML
```python
ui.html('<strong>Bold</strong> and <em>italic</em>')
```

### Mermaid Diagrams
```python
ui.mermaid('''
    graph TD
    A[Start] --> B[Process]
    B --> C[End]
''')
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/data_elements.md -->

# NiceGUI Data Elements

Elements for displaying data, charts, and visualizations.

## Classes

| Class | Description |
|-------|-------------|
| `ui.table` | Data table |
| `ui.aggrid` | AG Grid data table |
| `ui.highchart` | Highcharts chart |
| `ui.echart` | Apache ECharts |
| `ui.pyplot` | Matplotlib pyplot context |
| `ui.matplotlib` | Matplotlib figure |
| `ui.line_plot` | Simple line plot |
| `ui.plotly` | Plotly chart |
| `ui.linear_progress` | Linear progress bar |
| `ui.circular_progress` | Circular progress indicator |
| `ui.spinner` | Loading spinner |
| `ui.scene` | 3D scene (Three.js) |
| `ui.scene_view` | Additional view of 3D scene |
| `ui.leaflet` | Leaflet map |
| `ui.tree` | Tree view |
| `ui.log` | Log viewer |
| `ui.editor` | WYSIWYG editor |
| `ui.code` | Code display with syntax highlighting |
| `ui.json_editor` | JSON editor |

## Examples

### Table
```python
columns = [
    {'name': 'name', 'label': 'Name', 'field': 'name'},
    {'name': 'age', 'label': 'Age', 'field': 'age'},
]
rows = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
]
ui.table(columns=columns, rows=rows)
```

### AG Grid
```python
ui.aggrid({
    'columnDefs': [{'field': 'name'}, {'field': 'age'}],
    'rowData': [{'name': 'Alice', 'age': 30}],
})
```

### EChart
```python
ui.echart({
    'xAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
    'yAxis': {'type': 'value'},
    'series': [{'type': 'bar', 'data': [10, 20, 30]}],
})
```

### Plotly
```python
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(x=['A', 'B'], y=[10, 20]))
ui.plotly(fig)
```

### Progress
```python
ui.linear_progress(value=0.7)
ui.circular_progress(value=0.5)
ui.spinner()
ui.spinner('dots')
```

### 3D Scene
```python
with ui.scene() as scene:
    scene.box()
    scene.sphere().move(2, 0, 0)
```

### Leaflet Map
```python
m = ui.leaflet(center=(51.5, -0.1), zoom=10)
m.marker(latlng=(51.5, -0.1))
```

### Tree
```python
ui.tree([
    {'id': '1', 'label': 'Root', 'children': [
        {'id': '2', 'label': 'Child 1'},
        {'id': '3', 'label': 'Child 2'},
    ]}
], label_key='label')
```

### Log
```python
log = ui.log(max_lines=100)
log.push('Log message')
```

### Code Display
```python
ui.code('print("Hello")', language='python')
```

### JSON Editor
```python
ui.json_editor({'key': 'value', 'list': [1, 2, 3]})
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/audiovisual.md -->

# NiceGUI Audiovisual Elements

Elements for displaying images, audio, video, and icons.

## Classes

| Class | Description |
|-------|-------------|
| `ui.image` | Display image |
| `ui.interactive_image` | Image with SVG overlays |
| `ui.audio` | Audio player |
| `ui.video` | Video player |
| `ui.icon` | Icon display |
| `ui.avatar` | Avatar/profile image |

## Examples

### Image
```python
ui.image('https://example.com/image.png')
ui.image('/static/logo.png').classes('w-32')
ui.image('data:image/png;base64,...')  # Base64
```

### Interactive Image
```python
with ui.interactive_image('image.png') as img:
    img.svg_content = '<circle cx="100" cy="100" r="50" fill="red"/>'
```

### Audio
```python
audio = ui.audio('https://example.com/sound.mp3')
audio.play()
audio.pause()
```

### Video
```python
video = ui.video('https://example.com/video.mp4')
video.play()
ui.video('video.mp4', autoplay=True, muted=True, loop=True)
```

### Icon
```python
ui.icon('home')
ui.icon('favorite', color='red')
ui.icon('star', size='xl')
# Material Icons: https://fonts.google.com/icons
```

### Avatar
```python
ui.avatar('A')  # Letter avatar
ui.avatar(icon='person')
ui.avatar('https://example.com/photo.jpg')
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/app_and_config.md -->

# NiceGUI App & Configuration

App-level configuration, storage, and lifecycle management.

## App Namespace: `app`

### Storage

| Property | Scope | Persistence |
|----------|-------|-------------|
| `app.storage.tab` | Per browser tab | Server memory |
| `app.storage.client` | Per client connection | Server memory |
| `app.storage.user` | Per user (browser) | Server file |
| `app.storage.general` | App-wide shared | Server file |
| `app.storage.browser` | Per browser | Browser localStorage |

### Lifecycle Hooks

| Method | When Called |
|--------|-------------|
| `app.on_connect()` | Client connects (including reconnect) |
| `app.on_disconnect()` | Client disconnects |
| `app.on_delete()` | Client deleted (no reconnect) |
| `app.on_startup()` | App starts |
| `app.on_shutdown()` | App shuts down |
| `app.on_exception()` | Exception occurs |
| `app.on_page_exception()` | Exception during page build |

### Static Files

| Method | Description |
|--------|-------------|
| `app.add_static_files(url_path, local_path)` | Serve directory |
| `app.add_static_file(url_path, local_path)` | Serve single file |
| `app.add_media_files(url_path, local_path)` | Serve media (streaming) |
| `app.add_media_file(url_path, local_path)` | Serve single media file |

### Other

| Property/Method | Description |
|-----------------|-------------|
| `app.native` | Native mode configuration |
| `app.shutdown()` | Shut down the app |

## Examples

### Storage
```python
from nicegui import app, ui

# Per-user storage (persists across sessions)
app.storage.user['theme'] = 'dark'
theme = app.storage.user.get('theme', 'light')

# Per-tab storage
app.storage.tab['counter'] = 0

# App-wide storage
app.storage.general['total_visits'] = 0
```

### Lifecycle Hooks
```python
from nicegui import app, ui

@app.on_startup
async def startup():
    print('App starting...')

@app.on_shutdown
async def shutdown():
    print('App shutting down...')

@app.on_connect
async def connect():
    print('Client connected')

@app.on_disconnect
async def disconnect():
    print('Client disconnected')
```

### Static Files
```python
from nicegui import app

app.add_static_files('/static', 'static')
app.add_media_files('/media', 'media')
```

### Native Mode
```python
from nicegui import ui

ui.run(native=True, window_size=(800, 600))

# Or configure via app.native
app.native.window_args['size'] = (800, 600)
```

---

## UI Functions

### Page & Navigation

| Function | Description |
|----------|-------------|
| `ui.page(path)` | Decorator to define a page route |
| `ui.navigate.to(url)` | Navigate to URL |
| `ui.navigate.back()` | Go back in history |
| `ui.navigate.forward()` | Go forward in history |
| `ui.navigate.reload()` | Reload page |
| `ui.page_title(title)` | Change page title |

### Styling & Appearance

| Function | Description |
|----------|-------------|
| `ui.colors(primary=..., ...)` | Set color theme |
| `ui.dark_mode(value)` | Set dark mode |
| `ui.dark_mode.enable()` | Enable dark mode |
| `ui.dark_mode.disable()` | Disable dark mode |
| `ui.dark_mode.toggle()` | Toggle dark mode |
| `ui.query(selector)` | Query HTML elements |
| `ui.add_css(css)` | Add CSS to page |
| `ui.add_head_html(html)` | Add HTML to `<head>` |
| `ui.add_body_html(html)` | Add HTML to `<body>` |

### Interaction

| Function | Description |
|----------|-------------|
| `ui.notify(message)` | Show notification toast |
| `ui.download(data, filename)` | Trigger file download |
| `ui.clipboard.write(text)` | Write to clipboard |
| `ui.clipboard.read()` | Read from clipboard |
| `ui.keyboard(on_key=...)` | Keyboard event handler |
| `ui.timer(interval, callback)` | Periodic function calls |
| `ui.on(event, handler)` | Register event handler |

### Execution

| Function | Description |
|----------|-------------|
| `ui.run(...)` | Start NiceGUI server |
| `ui.run_with(app)` | Attach to FastAPI app |
| `ui.run_javascript(code)` | Execute JS on client |
| `ui.update(*elements)` | Send updates to client |

## Examples

### Page Definition
```python
from nicegui import ui

@ui.page('/')
def index():
    ui.label('Home')

@ui.page('/user/{user_id}')
def user_page(user_id: str):
    ui.label(f'User: {user_id}')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```

### Navigation
```python
ui.button('Go Home', on_click=lambda: ui.navigate.to('/'))
ui.button('Back', on_click=ui.navigate.back)
```

### Notifications
```python
ui.notify('Success!', type='positive')
ui.notify('Warning!', type='warning')
ui.notify('Error!', type='negative')
ui.notify('Info', position='top', close_button=True)
```

### Timer
```python
def update():
    label.text = str(datetime.now())

label = ui.label()
ui.timer(1.0, update)  # Update every second
```

### Dark Mode
```python
ui.dark_mode(True)  # Enable
ui.switch('Dark mode', on_change=lambda e: ui.dark_mode(e.value))
```

### Run Options
```python
ui.run(
    host='0.0.0.0',
    port=8080,
    title='My App',
    dark=True,
    reload=False,
    show=True,  # Open browser
)
```



<!-- Source: https://github.com/Alyxion/nice-prompt/blob/main/docs/classes/utilities.md -->

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



---

## Sample Applications

Reference implementations demonstrating NiceGUI patterns:


### dashboard

**Location**: `https://github.com/Alyxion/nice-prompt/tree/main/samples/dashboard/`

Analytics dashboard showcasing 8 chart types and input controls with OO architecture.
Demonstrates: Dashboard class with current(), DashboardData dataclass, ui.echart()
for line/bar/pie/gauge/radar/heatmap/scatter/candlestick, ui.timer() for real-time
updates, ui.dialog() for settings, filter controls that update all charts/KPIs.


### threejs_tornado

**Location**: `https://github.com/Alyxion/nice-prompt/tree/main/samples/threejs_tornado/`

Three.js particle tornado with custom GLSL shaders using NiceGUI's bundled Three.js.
Demonstrates: Element subclass with nicegui-scene module, WeakMap for Vue reactivity
workaround, custom vertex/fragment shaders, OrbitControls, real-time parameter updates.
But most importantly: How to visualize 3D scenes in NiceGUI.


### video_custom_component

**Location**: `https://github.com/Alyxion/nice-prompt/tree/main/samples/video_custom_component/`

Custom JavaScript/Vue component with real-time video processing.
Demonstrates: Element subclass with component='*.js', run_method(), run.io_bound(),
background_tasks.create(), ui.timer() for async polling, 16 OpenCV filters,
thread-safe state sharing, event-driven frame requests, base64 JPEG transfer.


### multi_dashboard

**Location**: `https://github.com/Alyxion/nice-prompt/tree/main/samples/multi_dashboard/`

Full SPA with authentication, signed cookie persistence, role-based permissions.
Demonstrates: ui.sub_pages, AppLayout class, login page as sub_page, header/drawer
visibility toggle, page auto-discovery, external CSS/JS, ECharts, dark mode.
Key files: main.py (server setup), layout.py (AppLayout), models/auth.py (AuthSession
with signed cookies), pages/ (auto-discovered page modules), static/ (CSS/JS).


### stock_peers

**Location**: `https://github.com/Alyxion/nice-prompt/tree/main/samples/stock_peers/`

Stock comparison dashboard with async data loading.
Demonstrates: dark mode, run.io_bound() for API calls, ui.echart(),
ui.chip() for toggles, ui.timer() for initial load, custom CSS.


### sub_pages_demo

**Location**: `https://github.com/Alyxion/nice-prompt/tree/main/samples/sub_pages_demo/`

SPA navigation with persistent client state. Single-file demo of ui.sub_pages.
Demonstrates: nested sub_pages, app.storage.client persistence, navigation drawer,
timer that keeps running across navigation, notes that persist during session.

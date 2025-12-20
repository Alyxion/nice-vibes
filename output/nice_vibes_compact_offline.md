# NiceGUI Master Prompt

Complete reference for AI agents building NiceGUI applications.

---


<!-- Source: docs/nicegui_prompt.md -->

# NiceGUI Development Guide for AI Agents

This document helps AI coding agents build NiceGUI applications correctly.

## Quick Start

### New Project Setup (Always Use Poetry)

When creating a new NiceGUI project, **always use Poetry** for dependency management:

```bash
poetry new my-app
cd my-app
poetry add nicegui
```

Or for an existing directory:

```bash
cd my-app
poetry init
poetry add nicegui
```

Always use the newest NiceGUI version, currently 3.3.1 or above via `poetry add nicegui`.

**Basic Poetry project structure:**

```
my-app/
├── my_app/              # Package folder (underscore, not hyphen)
│   └── __init__.py      # Required for Python package
├── main.py              # Entry point with ui.run()
├── pyproject.toml       # Poetry config (auto-generated)
├── README.md            # Project documentation
└── AGENTS.md            # AI agent rules (see below)
```

**AGENTS.md for new projects:**
When creating a new NiceGUI project, always add an `AGENTS.md` file if one doesn't exist yet. Copy it from:
`https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/docs/mechanics/AGENTS.md`

This file contains project rules for AI agents working on NiceGUI projects.

Run your app with:

```bash
poetry run python main.py
```

If the user does not have installed Poetry yet, you can guide him here: https://python-poetry.org/docs/

### Minimal Example

```python
from nicegui import ui

ui.label('Hello World')
ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='My App', show=False)
```

Remark: For professioal applications do not build the root context but use the ui.page() decorator instead, example:

```python
from nicegui import ui

@ui.page('/')
def index():
    ui.label('Hello World')
    ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False)
```

For an even more ambitious projects use object orientation and build a class for each page. As an initializer can not be async we usually define a build() method that is called after the object is initialized. Example:

```python
from nicegui import ui

class Page:
    def __init__(self):
        pass

    async def build(self):
        ui.label('Hello World')
        ui.button('Click me', on_click=lambda: ui.notify('Clicked!'))

@ui.page('/')
async def index():
    await Page().build()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='My App', show=False)
```

## Events

Event handling documentation in the events folder:

| Topic | File | Description |
|-------|------|-------------|
| **Element Events** | [element_events.md](docs/events/element_events.md) | Base `.on()` handler, DOM events |
| **Value Events** | [value_events.md](docs/events/value_events.md) | `on_change` for inputs, selects, etc. |
| **Button Events** | [button_events.md](docs/events/button_events.md) | `on_click` for buttons |
| **Keyboard Events** | [keyboard_events.md](docs/events/keyboard_events.md) | Global keyboard handling |
| **Lifecycle Events** | [lifecycle_events.md](docs/events/lifecycle_events.md) | App/client lifecycle hooks |
| **Upload Events** | [upload_events.md](docs/events/upload_events.md) | File upload handling |

## Core Mechanics

Essential patterns for building NiceGUI applications in the mechanics folder:

| Topic | File | Description |
|-------|------|-------------|
| **Application Structure** | [application_structure.md](docs/mechanics/application_structure.md) | Project setup, `ui.run()`, main guard |
| **Pages & Routing** | [pages.md](docs/mechanics/pages.md) | `@ui.page`, URL parameters, navigation |
| **Container Updates** | [container_updates.md](docs/mechanics/container_updates.md) | Dynamic content with `clear()` + `with` |
| **Event Binding** | [event_binding.md](docs/mechanics/event_binding.md) | Constructor vs method, `on_value_change` |
| **Binding & State** | [binding_and_state.md](docs/mechanics/binding_and_state.md) | Data binding, refreshable UI |
| **Data Modeling** | [data_modeling.md](docs/mechanics/data_modeling.md) | Dataclasses, per-user storage, dashboards |
| **Styling** | [styling.md](docs/mechanics/styling.md) | `.classes()`, `.style()`, custom CSS |
| **Background Execution** | [background_execution.md](docs/mechanics/background_execution.md) | `run.io_bound`, `background_tasks`, threading |
| **Custom Components** | [custom_components.md](docs/mechanics/custom_components.md) | Building Python/JS components |
| **Three.js Integration** | [threejs_integration.md](docs/mechanics/threejs_integration.md) | 3D rendering with Three.js |
| **Coding Style** | [coding_style.md](docs/mechanics/coding_style.md) | NiceGUI conventions, formatting, type hints |

## Class Reference by Category

Find detailed documentation for each category in the classes folder:

| Category | File | Description |
|----------|------|-------------|
| **Text Elements** | [text_elements.md](docs/classes/text_elements.md) | Labels, links, markdown, HTML |
| **Controls** | [controls.md](docs/classes/controls.md) | Buttons, inputs, selects, sliders |
| **Audiovisual** | [audiovisual.md](docs/classes/audiovisual.md) | Images, audio, video, icons |
| **Data Elements** | [data_elements.md](docs/classes/data_elements.md) | Tables, charts, 3D scenes, maps |
| **Layout** | [layout.md](docs/classes/layout.md) | Containers, navigation, dialogs |
| **App & Config** | [app_and_config.md](docs/classes/app_and_config.md) | Storage, lifecycle, routing |
| **Utilities** | [utilities.md](docs/classes/utilities.md) | Background tasks, testing, HTML |

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

## Sample Applications

When implementing a feature, **search the Sample Applications section by tags** to find relevant reference implementations. Each sample includes tags like `#charts`, `#authentication`, `#threejs`, `#custom-component`, `#spa`, etc. that help identify which sample demonstrates the pattern you need.

---

*This prompt should be updated when major documentation changes are made (new folders, new mechanics, new patterns).*



<!-- Source: docs/mechanics/poetry_setup.md -->

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



<!-- Source: docs/mechanics/application_structure.md -->

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
└── AGENTS.md
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
└── AGENTS.md
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



<!-- Source: docs/mechanics/pages.md -->

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

See [Routing Architecture](docs/mechanics/routing.md) for detailed explanation.

## Important Notes

1. **One function per route** - Each path needs its own decorated function
2. **Function runs on each visit** - Don't put expensive setup in page functions
3. **Elements are scoped** - UI elements belong to the page/client that created them
4. **Use storage for persistence** - `app.storage.user` persists across page visits
5. **Root page catches all** - When using `ui.run(root)`, unmatched URLs go to root



<!-- Source: docs/mechanics/sub_pages.md -->

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

See [Routing Architecture](docs/mechanics/routing.md) for detailed explanation of route precedence.

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

See [Authentication Pattern](docs/mechanics/authentication.md) for a complete example with login page, session management, and role-based access.

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



<!-- Source: docs/mechanics/container_updates.md -->

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



<!-- Source: docs/mechanics/data_modeling.md -->

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



<!-- Source: docs/mechanics/binding_and_state.md -->

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



<!-- Source: docs/mechanics/event_binding.md -->

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



<!-- Source: docs/mechanics/testing.md -->

# NiceGUI Testing Guide

This repository uses **pytest** and NiceGUI’s built-in **testing utilities** to test UI logic without needing a real browser.

## Recommended stack

- **pytest** for the test runner
- **pytest-asyncio** for `async def` tests
- **nicegui.testing.User** for simulated UI interaction
- **nicegui.testing.user_plugin** pytest plugin to provide the `user` fixture

In this repo, the plugin is enabled in `tests/conftest.py`:

```python
pytest_plugins = ['nicegui.testing.user_plugin']
```

## Writing a basic unit test

NiceGUI tests typically:

1. Define a test page with `@ui.page('/some_route')`
2. Use the `user` fixture to open the route
3. Interact with elements and assert visible text

Example:

```python
import pytest
from nicegui import ui
from nicegui.testing import User


@pytest.mark.asyncio
async def test_button_click(user: User) -> None:
    @ui.page('/test_button')
    def page():
        ui.button('Click me', on_click=lambda: ui.notify('Clicked'))

    await user.open('/test_button')
    user.find('Click me').click()
    await user.should_see('Clicked')
```

## How the `User` fixture works

- `User` simulates a client session.
- `await user.open('/path')` renders the page.
- `user.find('text')` finds an element by visible text.
- `await user.should_see('text')` waits until the UI shows the text.

This style is ideal for testing:

- **binding logic** (e.g. `bind_text_from`, `bind_value`)
- **event handlers** (`on_click`, `on_change`)
- **simple state updates**

## Important gotcha: `@ui.page` registrations are global

`@ui.page(...)` registrations are global within the Python process.

That means:

- Defining the *same route* in multiple tests can cause conflicts.
- Tests can influence each other if pages share routes.

Recommended patterns:

- **Use unique routes per test**, e.g. `/test_counter`, `/test_checkbox`.
- If you use parametrized tests, ensure each parameter uses a unique route.

## Testing state updates

A good pattern is to store state in a local object and update a bound label:

```python
import pytest
from nicegui import ui
from nicegui.testing import User


@pytest.mark.asyncio
async def test_counter_increment(user: User) -> None:
    @ui.page('/test_counter')
    def page():
        counter = {'value': 0}
        label = ui.label('Count: 0')

        def inc():
            counter['value'] += 1
            label.text = f"Count: {counter['value']}"

        ui.button('Increment', on_click=inc)

    await user.open('/test_counter')
    await user.should_see('Count: 0')
    user.find('Increment').click()
    await user.should_see('Count: 1')
```

## Async handlers

If your UI handler is async, you can define it normally:

```python
@ui.page('/test_async')
def page():
    async def load():
        ui.notify('loaded')

    ui.button('Load', on_click=load)
```

Then test it the same way.

## What not to test with `User`

The `User` fixture is great for unit-style tests but not ideal for:

- pixel-perfect layout assertions
- real browser behavior and client-side rendering details
- complex JS/WebGL behavior (e.g. Three.js scenes)

For those, prefer a separate **integration/E2E** approach (e.g. Playwright/Selenium) and keep it opt-in because it requires more dependencies.

## Running tests

From the repo root:

```bash
poetry run pytest
```

If you’re only working on UI unit tests:

```bash
poetry run pytest -q tests/test_basic.py
```



<!-- Source: docs/mechanics/styling.md -->

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



---

## Additional Documentation

The following documentation is not included in this prompt but available for reference:


### Advanced Mechanics

- **background_execution.md** (`docs/mechanics/background_execution.md`): run.io_bound() for I/O and C++ libs (OpenCV, PIL, NumPy), run.cpu_bound() for pure Python, background_tasks.create(), ui.timer() polling, thread-safe state with locks
- **custom_components.md** (`docs/mechanics/custom_components.md`): Custom JS/Vue components: creating Python+JS elements, props, events, run_method(), Vue lifecycle hooks (mounted/unmounted), ESM modules, resource loading
- **threejs_integration.md** (`docs/mechanics/threejs_integration.md`): Custom Three.js scenes using nicegui-scene module, WeakMap pattern to avoid Vue reactivity conflicts, custom GLSL shaders, OrbitControls, particle systems
- **configuration_deployment.md** (`docs/mechanics/configuration_deployment.md`): ui.run() parameters, favicon options, Docker deployment, PyInstaller packaging, SSL/HTTPS, native window mode, NiceGUI On Air
- **coding_style.md** (`docs/mechanics/coding_style.md`): NiceGUI coding conventions: single quotes, ~120 char lines, type hints with Self/Optional, Sphinx docstrings, mixin composition, WeakRef patterns

### Events

- **value_events.md** (`docs/events/value_events.md`): on_change, on_value_change for inputs, selects, sliders; ValueChangeEventArguments
- **button_events.md** (`docs/events/button_events.md`): on_click for buttons; ClickEventArguments
- **element_events.md** (`docs/events/element_events.md`): Generic DOM events: on('click'), on('mouseover'), etc.
- **lifecycle_events.md** (`docs/events/lifecycle_events.md`): app.on_startup, app.on_shutdown, app.on_connect, app.on_disconnect
- **keyboard_events.md** (`docs/events/keyboard_events.md`): ui.keyboard for global key events; KeyEventArguments
- **upload_events.md** (`docs/events/upload_events.md`): on_upload, on_rejected for file uploads; UploadEventArguments

### Class Reference

- **controls.md** (`docs/classes/controls.md`): ui.button, ui.input, ui.select, ui.checkbox, ui.switch, ui.slider, ui.toggle, ui.radio, ui.number, ui.textarea, ui.date, ui.time, ui.upload, ui.color_input
- **layout.md** (`docs/classes/layout.md`): ui.row, ui.column, ui.card, ui.grid, ui.expansion, ui.tabs, ui.dialog, ui.menu, ui.splitter, ui.scroll_area, ui.header, ui.footer, ui.drawer
- **text_elements.md** (`docs/classes/text_elements.md`): ui.label, ui.markdown, ui.html, ui.link, ui.badge, ui.chip, ui.tooltip, ui.notify
- **data_elements.md** (`docs/classes/data_elements.md`): ui.table, ui.aggrid, ui.echart, ui.plotly, ui.highchart, ui.tree, ui.log, ui.json_editor, ui.code
- **audiovisual.md** (`docs/classes/audiovisual.md`): ui.image, ui.interactive_image, ui.video, ui.audio, ui.icon, ui.avatar, ui.scene (3D), ui.leaflet (maps)
- **app_and_config.md** (`docs/classes/app_and_config.md`): app.storage (browser/user/general), app.on_startup/shutdown, ui.run() config, ui.dark_mode, ui.colors
- **utilities.md** (`docs/classes/utilities.md`): ui.timer, ui.keyboard, ui.download, ui.navigate, ui.run_javascript, ui.context, background_tasks



---

## Sample Applications

Reference implementations demonstrating NiceGUI patterns. Search by tags to find relevant samples.


### dashboard

**Location**: `samples/dashboard/`

**Tags**: #charts, #echart, #dashboard, #analytics, #dark-mode, #timer, #dialog, #filters, #dataclass, #oo-architecture

Analytics dashboard showcasing 8 chart types and input controls with OO architecture.
Demonstrates: Dashboard class with current(), DashboardData dataclass, ui.echart()
for line/bar/pie/gauge/radar/heatmap/scatter/candlestick, ui.timer() for real-time
updates, ui.dialog() for settings, filter controls that update all charts/KPIs.


### threejs_tornado

**Location**: `samples/threejs_tornado/`

**Tags**: #threejs, #3d, #particles, #shaders, #glsl, #animation, #webgl, #custom-element, #orbit-controls, #visualization

Three.js particle tornado with custom GLSL shaders using NiceGUI's bundled Three.js.
Demonstrates: Element subclass with nicegui-scene module, WeakMap for Vue reactivity
workaround, custom vertex/fragment shaders, OrbitControls, real-time parameter updates.
But most importantly: How to visualize 3D scenes in NiceGUI.


### cone_spray

**Location**: `samples/cone_spray/`

**Tags**: #threejs, #3d, #particles, #physics, #simulation, #canvas-texture, #buffer-geometry, #lighting, #animation, #interactive

Hollow cone nozzle spray with particle physics using Three.js.
Demonstrates: Canvas texture for round particles (not square), emission accumulator
for frame-rate-independent spawning, frustumCulled=false for dynamic particles,
needsUpdate=true for BufferGeometry, multi-directional lighting for metallic materials,
real-time physics (gravity, air resistance), interactive parameter controls.


### video_custom_component

**Location**: `samples/video_custom_component/`

**Tags**: #custom-component, #javascript, #vue, #video, #opencv, #background-tasks, #io-bound, #threading, #base64, #real-time

Custom JavaScript/Vue component with real-time video processing.
Demonstrates: Element subclass with component='*.js', run_method(), run.io_bound(),
background_tasks.create(), ui.timer() for async polling, 16 OpenCV filters,
thread-safe state sharing, event-driven frame requests, base64 JPEG transfer.


### multi_dashboard

**Location**: `samples/multi_dashboard/`

**Tags**: #authentication, #spa, #sub-pages, #cookies, #permissions, #roles, #auto-discovery, #layout, #drawer, #header

Full SPA with authentication, signed cookie persistence, role-based permissions.
Demonstrates: ui.sub_pages, AppLayout class, login page as sub_page, header/drawer
visibility toggle, page auto-discovery, external CSS/JS, ECharts, dark mode.
Key files: main.py (server setup), layout.py (AppLayout), models/auth.py (AuthSession
with signed cookies), pages/ (auto-discovered page modules), static/ (CSS/JS).


### stock_peers

**Location**: `samples/stock_peers/`

**Tags**: #stocks, #finance, #async, #io-bound, #echart, #chips, #dark-mode, #api, #yfinance, #comparison

Stock comparison dashboard with async data loading.
Demonstrates: dark mode, run.io_bound() for API calls, ui.echart(),
ui.chip() for toggles, ui.timer() for initial load, custom CSS.


### sub_pages_demo

**Location**: `samples/sub_pages_demo/`

**Tags**: #spa, #sub-pages, #navigation, #storage, #persistence, #drawer, #nested-routes, #timer, #state, #client-storage

SPA navigation with persistent client state. Single-file demo of ui.sub_pages.
Demonstrates: nested sub_pages, app.storage.client persistence, navigation drawer,
timer that keeps running across navigation, notes that persist during session.


### calculator

**Location**: `samples/calculator/`

**Tags**: #beginner, #dataclass, #binding, #form, #calculator, #minimal

Minimal calculator app demonstrating NiceGUI best practices.
Demonstrates: dataclass for state, bind_value/bind_text for data binding,
proper @ui.page decorator, header, main guard with title and show=False.
This is the recommended minimal structure for any NiceGUI application.

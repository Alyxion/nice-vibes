# NiceGUI Project Creation Guide

This guide defines the rules and questionnaire for guided NiceGUI project creation.

## Resources

Before creating a project, consider using these resources:

### Master Prompts
Copy one of these into your AI context for comprehensive NiceGUI knowledge:

| Variant | Tokens | URL | Contents |
|---------|--------|-----|----------|
| **Compact** | ~14K | [nice_vibes_compact.md](https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_compact.md) | Core mechanics, basic events, essential styling. Good for simple UIs and quick tasks. |
| **Optimum** | ~23K | [nice_vibes.md](https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes.md) | Everything in Compact + authentication patterns, SPA navigation (ui.sub_pages), advanced events, class references (Element, Client, Storage). Recommended for most projects. |
| **Extended** | ~34K | [nice_vibes_extended.md](https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_extended.md) | Everything in Optimum + custom JavaScript/Vue components, deployment guides, Three.js 3D visualization, OpenCV integration. For advanced use cases. |

### Sample Applications & Components
Use MCP tools to explore available resources:

- `list_samples` - List all available sample applications with descriptions
- `get_sample_source` - Get the source code of a sample
- `get_component_info` - Get documentation, source code, and GitHub links for any NiceGUI component
- `get_component_docs` - Get official NiceGUI documentation for a component

CLI commands:
- `nice-vibes list` - List samples locally
- `nice-vibes copy <sample>` - Copy a sample as starting point

## How to Use This Guide

### Standard Flow
When a user wants to create a new NiceGUI project:

1. **Ask for project name** (required)
2. **Ask basic questions:**
   - **Project type:** What does the app do? (dashboard with charts, calculator/form, data viewer, admin panel, 3D visualization, etc.)
   - **Complexity level:** 
     - Beginner = simple code, single file, lots of comments
     - Intermediate = organized code with classes, separate files for models
     - Advanced = full architecture with pages/, models/, components/ folders
   - **Page structure:**
     - Single page = everything on one screen, simplest option
     - Multi page = separate pages with full browser reload between them
     - SPA (Single Page App) = smooth navigation without reload, like a mobile app feel
   - **Styling:**
     - Basic = use NiceGUI defaults, quick to set up
     - Custom = separate style file for colors, fonts, spacing customization
3. **Show summary and confirm:**
   ```
   Creating: My Dashboard App
   - Type: Dashboard
   - Level: Intermediate (OO patterns)
   - Pages: SPA (ui.sub_pages)
   - Styling: External CSS
   
   Would you like to customize anything else, or shall I create the project?
   ```
4. **If user wants more customization**, ask about:
   - Authentication (none/simple/roles/persistent)
   - Additional features (charts, tables, dark mode, dialogs, etc.)
5. **Generate the project**
6. **Preview the design:** If the server is NOT running and the user asks for a screenshot, run the app and take a screenshot.
   - Use `capture_app_screenshot` with the full path to `main.py` - this starts the app, takes a screenshot, and stops it automatically
   - The screenshot opens in the user's browser so they can see it
   - Review the visual design and suggest improvements
   - Ask the user: "How do you like the design? Would you like me to improve anything?"
7. **Run the app:** After the user approves the design
   - **Always use `poetry run`** when in a Poetry environment: `poetry run python main.py`
   - **Never open a browser without asking** - always ask the user first before using `open_browser` or opening a screenshot stored to disk in the browser.
   - **Do not take screenshots while the app is running** - if the user's app is already running, let them interact with it directly instead of creating screenshot HTML dumps
   - **Hot reload is automatic** - once the server is running, any code changes are automatically detected and the browser refreshes. No need to restart the server for code changes.

### Inferring from Context
If the user provides details upfront, use them and skip those questions:
- "Create a dashboard called Sales Analytics with authentication" → Already have name, type, auth
- "Simple calculator" → Implies beginner level, single page, no auth
- "Full admin panel with roles" → Implies advanced, SPA, role-based auth

## Mandatory Project Rules

Every generated NiceGUI project MUST follow these rules:

### 0. Always Use Poetry for Project Setup

**CRITICAL: Create ALL required files before running `poetry install`**

```bash
# 1. Create project directory
mkdir my_project && cd my_project

# 2. Create README.md FIRST (Poetry requires this)
echo "# My Project\n\nA NiceGUI application." > README.md

# 3. Create the package directory and __init__.py
mkdir my_project
touch my_project/__init__.py

# 4. Initialize Poetry with package-mode disabled (simpler for apps)
poetry init --name my-project --python "^3.12" --dependency nicegui --no-interaction

# 5. Add package-mode = false to pyproject.toml to avoid packaging issues
# This tells Poetry this is an application, not a library
```

**Required pyproject.toml structure:**
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "A NiceGUI application"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
package-mode = false  # IMPORTANT: Prevents "Readme path does not exist" errors

[tool.poetry.dependencies]
python = "^3.12"
nicegui = "^2.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Files to create BEFORE `poetry install`:**
1. `README.md` - Required by Poetry (even a one-liner is fine)
2. `pyproject.toml` - With `package-mode = false` for applications
3. `main.py` - Your application entry point
4. `AGENTS.md` - Copy from: `https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/docs/mechanics/AGENTS.md`

The `AGENTS.md` file contains project rules for AI agents. Always add it to new projects if one doesn't exist yet.

Never use plain `pip install` or `requirements.txt`.

### 1. Always Use Page Decorator
```python
@ui.page('/')
def index():
    # UI code here
```
Never create bare UI elements outside a page function.

### 2. Always Use Main Guard
```python
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='Project Name', show=False)
```
- Always include `title='Project Name'` for HTML title
- Always include `show=False` to prevent auto-opening browser
- **Never change the port** - NiceGUI defaults to 8080, keep it that way

### 3. If Port 8080 is Blocked
Never change the port to work around a blocked port. Instead, kill the old process:
```bash
# Find and kill process on port 8080
lsof -ti:8080 | xargs kill -9
```
Ask the user before killing processes. The default port 8080 should always be used.

### 4. Consider Adding a Header
```python
with ui.header().classes('bg-primary'):
    ui.label('Project Name').classes('text-xl font-bold')
```
Recommended for most apps, but optional for simple tools/calculators.

### 5. Always Use Dataclasses for State
```python
from dataclasses import dataclass, field

@dataclass
class AppState:
    value: float = 0.0
    result: str = field(default='')
    
    def compute(self):
        self.result = f'Result: {self.value * 2}'
```
Never use global variables or manual UI updates.

### 6. Always Use Data Binding
```python
state = AppState()
ui.number('Value').bind_value(state, 'value')
ui.label().bind_text(state, 'result')
```
Use `bind_value()`, `bind_text()`, `bind_visibility()` instead of callbacks that manually update UI.

---

## Project Creation Questionnaire

### Question 0: Project Name (Required)
**What is the name of your project?**

Used for:
- Folder name (snake_case)
- HTML title in browser tab
- Header text

Example: "My Calculator App", "Sales Dashboard", "Product Viewer"

---

### Question 1: Project Type
**What kind of application do you want to build?**

| Type | Description | Example Use Cases |
|------|-------------|-------------------|
| `calculator` | Input form → compute → show result | Loan calculator, unit converter, pricing estimator |
| `data_fetcher` | Input parameters → fetch/query → display | Stock lookup, weather checker, API explorer |
| `dashboard` | Charts, KPIs, filters, real-time updates | Analytics dashboard, monitoring panel |
| `form_app` | Multi-step forms, validation, submission | Registration, surveys, order forms |
| `admin_panel` | CRUD tables, search, bulk operations | User management, inventory system |
| `3d_visualization` | Three.js scenes, animations, controls | Product viewer, simulations, data viz |
| `realtime` | WebSocket/timer updates, live data | IoT monitor, chat, live charts |
| `custom_component` | JavaScript/Vue component development | Video player, custom widget |
| `general` | Basic structure, you decide | Starting point |

---

### Question 2: Complexity Level
**What's your experience level with NiceGUI?**

| Level | Code Style | File Structure |
|-------|------------|----------------|
| `beginner` | Functional with dataclasses, lots of comments | Single `main.py` |
| `intermediate` | OO patterns, organized code | `main.py` + `models/` |
| `advanced` | Full OO architecture, clean separation | `main.py`, `pages/`, `models/`, `components/` |

---

### Question 3: Page Structure
**How many pages will your app have?**

| Structure | Description | When to Use |
|-----------|-------------|-------------|
| `single` | One page application | Simple tools, calculators |
| `multi_page` | Multiple separate pages (`@ui.page`) | Different sections with full reload |
| `spa` | Single Page App (`ui.sub_pages`) | Smooth navigation, persistent state |

---

### Question 4: Authentication
**Does your app need user authentication?**

| Option | Description |
|--------|-------------|
| `none` | No login required |
| `simple` | Basic login (username/password check) |
| `roles` | Role-based permissions (admin, user, viewer) |
| `persistent` | Signed cookie persistence (stay logged in) |

---

### Question 5: UI Features (Multiple Choice)
**Which UI features do you need?**

| Feature | Description |
|---------|-------------|
| `dark_mode` | Dark/light theme toggle |
| `header` | Fixed header with navigation (always included) |
| `drawer` | Side navigation drawer |
| `charts` | ECharts visualizations |
| `tables` | Data tables with sorting/filtering |
| `forms` | Input forms with validation |
| `dialogs` | Modal dialogs |
| `notifications` | Toast notifications |

---

### Question 6: Data Handling
**How will your app handle data?**

| Option | Description |
|--------|-------------|
| `static` | Hardcoded/demo data |
| `api` | External API calls (use `run.io_bound()`) |
| `database` | Database connection |
| `files` | File upload/download |

---

### Question 7: Styling
**What styling approach do you prefer?**

| Option | Description |
|--------|-------------|
| `basic` | Inline styles with `.classes()`, NiceGUI/Quasar defaults |
| `external_css` | Separate CSS file for custom styling |

---

## Minimal Template (calculator/data_fetcher)

```python
"""{{PROJECT_NAME}} - A NiceGUI application."""

from dataclasses import dataclass, field

from nicegui import ui


@dataclass
class AppState:
    # Input fields
    input_value: float = 0.0
    
    # Output
    result: str = field(default='')

    def compute(self):
        """Compute result from inputs."""
        self.result = f'Result: {self.input_value * 2}'


@ui.page('/')
def index():
    state = AppState()

    with ui.header().classes('bg-primary'):
        ui.label('{{PROJECT_NAME}}').classes('text-xl font-bold')

    with ui.card().classes('max-w-md mx-auto mt-8 p-6'):
        ui.number('Input Value').bind_value(state, 'input_value')
        ui.button('Compute', on_click=state.compute)
        ui.label().bind_text(state, 'result').classes('text-lg font-bold mt-4')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='{{PROJECT_NAME}}', show=False)
```

---

## Summary Template

After collecting answers, summarize:

> **Creating NiceGUI project: {{PROJECT_NAME}}**
> - Type: {{TYPE}}
> - Level: {{LEVEL}}
> - Structure: {{STRUCTURE}}
> - Auth: {{AUTH}}
> - Features: {{FEATURES}}
> - Data: {{DATA}}
> - Styling: {{STYLING}}
> - Output: ./{{project_name_snake}}/

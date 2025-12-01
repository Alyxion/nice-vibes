#!/usr/bin/env python3
"""
Nice Vibes MCP Server - Provides AI assistants with NiceGUI documentation and visual debugging.

Features:
- Topic index and detailed documentation lookup
- Visual debugging: capture screenshots of running NiceGUI apps
- Sample listing and source code access

Usage:
    python -m nice_vibes.mcp
"""

import asyncio
import base64
import inspect
import io
import subprocess
import sys
import tempfile
import time
import webbrowser
from pathlib import Path
from typing import Any

import yaml
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    ImageContent,
    Tool,
    Resource,
)

# Paths - resolve to absolute paths to work regardless of CWD
# nice_vibes/mcp/server.py -> nice_vibes/mcp -> nice_vibes -> project root
_SCRIPT_DIR = Path(__file__).resolve().parent  # nice_vibes/mcp
_NICE_VIBES_DIR = _SCRIPT_DIR.parent  # nice_vibes
PACKAGE_DIR = _NICE_VIBES_DIR.parent  # project root (nice-prompt)
DOCS_DIR = PACKAGE_DIR / 'docs'
SAMPLES_DIR = PACKAGE_DIR / 'samples'
CONFIG_FILE = DOCS_DIR / 'prompt_config.yaml'

# Screenshot settings
SCREENSHOT_WIDTH = 1920
SCREENSHOT_HEIGHT = 1080
OUTPUT_WIDTH = 1920
DEFAULT_WAIT = 3
PORT = 8080

# Create server
server = Server(
    "nice-vibes",
    instructions="""NiceVibes MCP Server - Use this when working with NiceGUI applications.

NiceGUI is a Python framework for building web-based user interfaces, dashboards, and 3D visualizations.
It lets you create interactive web apps with pure Python - no HTML/CSS/JavaScript required.
Common use cases: data dashboards, admin panels, IoT interfaces, 3D scenes, real-time visualizations.

This server provides:
- Guided project creation with questionnaire and best-practice templates
- Documentation search and retrieval for NiceGUI components and patterns
- Source code inspection of NiceGUI classes from the installed package
- Visual debugging via screenshots of running NiceGUI applications
- Sample application browsing and source code access

Use these tools when:
- Creating a new NiceGUI project from scratch (use get_project_creation_guide)
- Building web UIs, dashboards, or visualizations with NiceGUI
- Looking up how NiceGUI components work (ui.button, ui.table, ui.echart, ui.scene, etc.)
- Debugging layout or styling issues in a running NiceGUI app
- Exploring NiceGUI sample applications for reference

IMPORTANT for project creation:
When a user wants to create a new NiceGUI project:
1. Use get_project_creation_guide to get the rules
2. Ask for: project name, type, complexity level, styling preference
3. Show a summary and ask if they want to customize further
4. ALWAYS use Poetry for project setup (poetry init, poetry add nicegui)
5. Never use pip install or requirements.txt
6. Never change the port from 8080 - kill old processes instead
7. Once the server is running, code changes are automatically hot-reloaded - no restart needed
8. Never open a browser without asking the user first
9. Do not take screenshots while the app is running - let users interact directly
"""
)


def load_config() -> dict:
    """Load prompt config."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return yaml.safe_load(f)
    return {}


def get_topic_index() -> dict[str, dict]:
    """Build topic index from config and docs."""
    config = load_config()
    topics = {}
    
    # Mechanics
    for item in config.get('mechanics', []):
        filename = item['file']
        name = filename.replace('.md', '')
        topics[name] = {
            'category': 'mechanics',
            'file': f'docs/mechanics/{filename}',
            'summary': item.get('summary', ''),
        }
    
    # Advanced mechanics
    for item in config.get('adv_mechanics', []):
        filename = item['file']
        name = filename.replace('.md', '')
        topics[name] = {
            'category': 'advanced',
            'file': f'docs/mechanics/{filename}',
            'summary': item.get('summary', ''),
        }
    
    # Events
    for item in config.get('events', []):
        filename = item['file']
        name = filename.replace('.md', '')
        topics[name] = {
            'category': 'events',
            'file': f'docs/events/{filename}',
            'summary': item.get('summary', ''),
        }
    
    # Classes
    for item in config.get('classes', []):
        filename = item['file']
        name = filename.replace('.md', '')
        topics[name] = {
            'category': 'classes',
            'file': f'docs/classes/{filename}',
            'summary': item.get('summary', ''),
        }
    
    # Samples
    for sample in config.get('samples', []):
        name = sample['name']
        topics[f"sample_{name}"] = {
            'category': 'samples',
            'path': sample['path'],
            'tags': sample.get('tags', []),
            'summary': sample.get('summary', '').strip().split('\n')[0],
        }
    
    return topics


def get_samples() -> dict[str, dict]:
    """Get sample information."""
    config = load_config()
    samples = {}
    for sample in config.get('samples', []):
        samples[sample['name']] = {
            'path': sample['path'],
            'tags': sample.get('tags', []),
            'summary': sample.get('summary', '').strip(),
        }
    return samples


def kill_port(port: int) -> bool:
    """Kill any process on the given port. Returns True if a process was killed."""
    try:
        result = subprocess.run(['lsof', '-ti', f':{port}'], capture_output=True, text=True)
        if result.stdout.strip():
            for pid in result.stdout.strip().split('\n'):
                subprocess.run(['kill', '-9', pid], capture_output=True)
            time.sleep(0.5)
            return True
        return False
    except Exception:
        return False


def save_screenshot_html(png_bytes: bytes, title: str, description: str = "", open_in_browser: bool = False) -> Path:
    """Save a screenshot as an HTML file for viewing.
    
    This is useful when the MCP client cannot display images inline.
    Creates an HTML file with the embedded image. The path is returned
    so the user can open it manually via file:// URL if needed.
    
    :param png_bytes: The PNG image data
    :param title: Title for the HTML page
    :param description: Optional description text
    :param open_in_browser: If True, automatically open the HTML file in the browser
    :return: Path to the created HTML file
    """
    b64_data = base64.standard_b64encode(png_bytes).decode('utf-8')
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        .description {{
            color: #888;
            margin-bottom: 20px;
        }}
        .screenshot {{
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            max-width: 100%;
            height: auto;
        }}
        .timestamp {{
            color: #666;
            font-size: 12px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <p class="description">{description}</p>
        <img src="data:image/png;base64,{b64_data}" alt="Screenshot" class="screenshot">
        <p class="timestamp">Captured by NiceVibes MCP Server</p>
    </div>
</body>
</html>'''
    
    # Create a temp file that won't be auto-deleted
    temp_dir = Path(tempfile.gettempdir()) / 'nice_vibes_screenshots'
    temp_dir.mkdir(exist_ok=True)
    
    # Use timestamp in filename for uniqueness
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    html_path = temp_dir / f'screenshot_{timestamp}.html'
    html_path.write_text(html_content)
    
    # Optionally open in browser
    if open_in_browser:
        webbrowser.open(f'file://{html_path}')
    
    return html_path


def get_nicegui_class(class_name: str):
    """Get a NiceGUI class by name.
    
    Supports formats like:
    - 'ui.button' -> nicegui.elements.button.Button
    - 'Button' -> nicegui.elements.button.Button
    - 'app.storage' -> nicegui.storage module
    """
    import nicegui
    from nicegui import ui, app
    
    # Try ui.xxx format
    if class_name.startswith('ui.'):
        attr_name = class_name[3:]
        if hasattr(ui, attr_name):
            obj = getattr(ui, attr_name)
            # If it's a function that returns a class instance, get the class
            if callable(obj) and hasattr(obj, '__self__'):
                return type(obj.__self__)
            elif isinstance(obj, type):
                return obj
            elif callable(obj):
                # It's a factory function, try to find the class it creates
                # Check if there's a corresponding class in elements
                class_name_pascal = ''.join(word.capitalize() for word in attr_name.split('_'))
                for module_name in dir(nicegui.elements):
                    module = getattr(nicegui.elements, module_name, None)
                    if module and hasattr(module, class_name_pascal):
                        return getattr(module, class_name_pascal)
                return obj
            return obj
    
    # Try app.xxx format
    if class_name.startswith('app.'):
        attr_name = class_name[4:]
        if hasattr(app, attr_name):
            return getattr(app, attr_name)
    
    # Try direct class name (e.g., 'Button', 'Element')
    # Search in nicegui.elements
    for module_name in dir(nicegui.elements):
        module = getattr(nicegui.elements, module_name, None)
        if module and hasattr(module, class_name):
            return getattr(module, class_name)
    
    # Try in nicegui directly
    if hasattr(nicegui, class_name):
        return getattr(nicegui, class_name)
    
    # Try ui module
    if hasattr(ui, class_name.lower()):
        return getattr(ui, class_name.lower())
    
    return None


# Raw GitHub URLs so AI can read the content directly
NICEGUI_GITHUB_RAW = "https://raw.githubusercontent.com/zauberzeug/nicegui/main"
# For linking with line numbers (view mode)
NICEGUI_GITHUB_VIEW = "https://github.com/zauberzeug/nicegui/blob/main"
# Documentation source (Python files with docstrings and examples)
NICEGUI_DOCS_RAW = "https://raw.githubusercontent.com/zauberzeug/nicegui/main/website/documentation/content"

# Map element names to their documentation file names
ELEMENT_DOC_FILES = {
    'button': 'button',
    'input': 'input',
    'select': 'select',
    'checkbox': 'checkbox',
    'switch': 'switch',
    'slider': 'slider',
    'table': 'table',
    'echart': 'echart',
    'aggrid': 'ag_grid',
    'plotly': 'plotly',
    'highchart': 'highchart',
    'leaflet': 'leaflet',
    'scene': 'scene',
    'log': 'log',
    'code': 'code',
    'json_editor': 'json_editor',
    'codemirror': 'codemirror',
    'tree': 'tree',
    'label': 'label',
    'markdown': 'markdown',
    'html': 'html',
    'image': 'image',
    'video': 'video',
    'audio': 'audio',
    'icon': 'icon',
    'avatar': 'avatar',
    'card': 'card',
    'dialog': 'dialog',
    'menu': 'menu',
    'tabs': 'tabs',
    'expansion': 'expansion',
    'scroll_area': 'scroll_area',
    'splitter': 'splitter',
    'row': 'row',
    'column': 'column',
    'grid': 'grid',
    'header': 'header',
    'footer': 'footer',
    'drawer': 'drawer',
    'timer': 'timer',
    'keyboard': 'keyboard',
    'upload': 'upload',
    'download': 'download',
    'notify': 'notify',
    'dark_mode': 'dark_mode',
}


def get_github_source_url(cls, raw: bool = True) -> str | None:
    """Get GitHub source URL for a NiceGUI class.
    
    :param cls: The class to get URL for
    :param raw: If True, return raw URL (readable by AI). If False, return view URL with line numbers.
    """
    try:
        file_path = inspect.getfile(cls)
        if 'nicegui' not in file_path:
            return None
        
        # Extract path relative to nicegui package
        rel_path = 'nicegui' + file_path.split('nicegui')[-1]
        
        if raw:
            return f"{NICEGUI_GITHUB_RAW}/{rel_path}"
        else:
            # Get line number for view URL
            try:
                lines, start_line = inspect.getsourcelines(cls)
                return f"{NICEGUI_GITHUB_VIEW}/{rel_path}#L{start_line}"
            except (TypeError, OSError):
                return f"{NICEGUI_GITHUB_VIEW}/{rel_path}"
    except (TypeError, OSError):
        return None


def get_docs_url(element_name: str) -> str | None:
    """Get raw NiceGUI documentation URL for an element (Python source with examples)."""
    # Check if there's a specific mapping
    doc_name = ELEMENT_DOC_FILES.get(element_name.lower(), element_name.lower())
    
    # Return raw Python documentation file URL
    return f"{NICEGUI_DOCS_RAW}/{doc_name}_documentation.py"


def get_component_info(cls, max_ancestors: int = 3, include_source: bool = True) -> str:
    """Get comprehensive info about a NiceGUI component.
    
    :param cls: The class to get info for
    :param max_ancestors: Maximum number of ancestor classes to include
    :param include_source: Whether to include source code
    :return: Formatted info string
    """
    result_parts = []
    
    if not isinstance(cls, type):
        # It's not a class, just get basic info
        name = cls.__name__ if hasattr(cls, '__name__') else str(cls)
        result_parts.append(f"# {name}")
        result_parts.append(f"Type: {type(cls).__name__}")
        if hasattr(cls, '__module__'):
            result_parts.append(f"Module: {cls.__module__}")
        try:
            source = inspect.getsource(cls)
            if include_source:
                result_parts.append(f"\n## Source\n\n```python\n{source}\n```")
        except (TypeError, OSError):
            pass
        return '\n'.join(result_parts)
    
    # Get the class and its MRO (Method Resolution Order)
    mro = cls.__mro__
    
    # Filter to only include nicegui classes and limit ancestors
    nicegui_classes = []
    for c in mro:
        module = getattr(c, '__module__', '')
        if 'nicegui' in module and c.__name__ != 'object':
            nicegui_classes.append(c)
            if len(nicegui_classes) > max_ancestors:
                break
    
    # Header with class name
    result_parts.append(f"# {cls.__name__}")
    result_parts.append("")
    
    # Inheritance chain
    if len(nicegui_classes) > 1:
        inheritance = " → ".join(c.__name__ for c in nicegui_classes)
        result_parts.append(f"**Inheritance:** {inheritance}")
        result_parts.append("")
    
    # Documentation links
    result_parts.append("## URLs (raw, AI-readable)")
    result_parts.append("")
    
    # Official docs URL
    element_name = cls.__name__.lower()
    # Try to find the ui.xxx name
    from nicegui import ui
    for attr in dir(ui):
        if not attr.startswith('_'):
            obj = getattr(ui, attr, None)
            if obj is cls or (isinstance(obj, type) and issubclass(obj, cls) and obj.__name__ == cls.__name__):
                element_name = attr
                break
    
    docs_url = get_docs_url(element_name)
    result_parts.append(f"- **Official Docs (raw md):** {docs_url}")
    
    # GitHub source URLs (raw for AI readability)
    for c in nicegui_classes[:2]:  # Main class and first parent
        github_url = get_github_source_url(c, raw=True)
        if github_url:
            result_parts.append(f"- **{c.__name__} Source (raw):** {github_url}")
    
    result_parts.append("")
    
    # Source code
    if include_source:
        result_parts.append("## Source Code")
        result_parts.append("")
        
        for c in nicegui_classes:
            try:
                source = inspect.getsource(c)
                file_path = inspect.getfile(c)
                if 'nicegui' in file_path:
                    file_path = 'nicegui' + file_path.split('nicegui')[-1]
                
                result_parts.append(f"### {c.__name__}")
                result_parts.append(f"*Module: {c.__module__} | File: {file_path}*")
                result_parts.append("")
                result_parts.append(f"```python\n{source}\n```")
                result_parts.append("")
            except (TypeError, OSError) as e:
                result_parts.append(f"*Could not get source for {c.__name__}: {e}*")
                result_parts.append("")
    
    return '\n'.join(result_parts)


def capture_screenshot_sync(
    url: str,
    wait_seconds: int = DEFAULT_WAIT,
    width: int = OUTPUT_WIDTH,
) -> bytes:
    """Capture a screenshot and return as PNG bytes."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from PIL import Image
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--window-size={SCREENSHOT_WIDTH},{SCREENSHOT_HEIGHT}')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(wait_seconds)
        
        # Capture screenshot
        png_data = driver.get_screenshot_as_png()
        
        # Resize
        img = Image.open(io.BytesIO(png_data))
        ratio = width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PNG bytes
        output = io.BytesIO()
        img.save(output, format='PNG')
        return output.getvalue()
        
    finally:
        driver.quit()


async def capture_screenshot(
    url: str,
    wait_seconds: int = DEFAULT_WAIT,
    width: int = OUTPUT_WIDTH,
) -> bytes:
    """Async wrapper for screenshot capture."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        capture_screenshot_sync,
        url,
        wait_seconds,
        width,
    )


async def capture_app_screenshot(
    app_dir: Path,
    path: str = '/',
    wait_seconds: int = DEFAULT_WAIT,
) -> bytes:
    """Start an app, capture screenshot, stop app."""
    kill_port(PORT)
    
    # Start server
    process = subprocess.Popen(
        [sys.executable, 'main.py'],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    try:
        # Wait for server to start
        await asyncio.sleep(2)
        
        if process.poll() is not None:
            raise RuntimeError("Server failed to start")
        
        # Capture screenshot
        url = f'http://localhost:{PORT}{path}'
        return await capture_screenshot(url, wait_seconds)
        
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        kill_port(PORT)


# ============================================================================
# MCP Tool Handlers
# ============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="list_topics",
            description="List all available NiceGUI documentation topics with summaries. Use this to discover what documentation is available.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category: mechanics, advanced, events, classes, samples. Leave empty for all.",
                        "enum": ["mechanics", "advanced", "events", "classes", "samples", ""],
                    },
                },
            },
        ),
        Tool(
            name="get_topic",
            description="Get detailed documentation for a specific topic. Use list_topics first to see available topics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic name (e.g., 'sub_pages', 'styling', 'custom_components')",
                    },
                },
                "required": ["topic"],
            },
        ),
        Tool(
            name="search_topics",
            description="Search topics by keyword. Returns matching topics and their summaries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for in topic names, summaries, and tags",
                    },
                },
                "required": ["keyword"],
            },
        ),
        Tool(
            name="list_samples",
            description="List available NiceGUI sample applications with descriptions.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_sample_source",
            description="Get the source code of a sample application.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sample": {
                        "type": "string",
                        "description": "Sample name (e.g., 'dashboard', 'multi_dashboard')",
                    },
                    "file": {
                        "type": "string",
                        "description": "Specific file to get (default: main.py)",
                        "default": "main.py",
                    },
                },
                "required": ["sample"],
            },
        ),
        Tool(
            name="capture_sample_screenshot",
            description="Capture a screenshot of a running sample application. Returns an image and also saves an HTML file to disk. The HTML path is included in the response for viewing via file:// URL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sample": {
                        "type": "string",
                        "description": "Sample name to capture",
                    },
                    "path": {
                        "type": "string",
                        "description": "URL path to capture (default: /)",
                        "default": "/",
                    },
                    "wait": {
                        "type": "integer",
                        "description": "Seconds to wait after page load (default: 3)",
                        "default": 3,
                    },
                    "open_browser": {
                        "type": "boolean",
                        "description": "Open the HTML file in browser to show it to the user (default: false)",
                        "default": False,
                    },
                },
                "required": ["sample"],
            },
        ),
        Tool(
            name="capture_url_screenshot",
            description="Capture a screenshot of any URL. Use this to visually debug a RUNNING NiceGUI application at localhost:8080. Returns an image and also saves an HTML file to disk. The HTML path is included in the response for viewing via file:// URL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Full URL to capture (e.g., http://localhost:8080/dashboard)",
                    },
                    "wait": {
                        "type": "integer",
                        "description": "Seconds to wait after page load (default: 3)",
                        "default": 3,
                    },
                    "open_browser": {
                        "type": "boolean",
                        "description": "Open the HTML file in browser to show it to the user (default: false)",
                        "default": False,
                    },
                },
                "required": ["url"],
            },
        ),
        Tool(
            name="capture_app_screenshot",
            description="Start a NiceGUI app from a main.py file, capture a screenshot, then stop it. Use this to preview a newly created project BEFORE running it. Provide the full path to the main.py file. Returns an image and also saves an HTML file to disk. The HTML path is included in the response for viewing via file:// URL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "main_file": {
                        "type": "string",
                        "description": "Full absolute path to the main.py file (e.g., /Users/me/my_project/main.py)",
                    },
                    "path": {
                        "type": "string",
                        "description": "URL path to capture (default: /)",
                        "default": "/",
                    },
                    "wait": {
                        "type": "integer",
                        "description": "Seconds to wait after page load (default: 3)",
                        "default": 3,
                    },
                    "open_browser": {
                        "type": "boolean",
                        "description": "Open the HTML file in browser to show it to the user (default: false)",
                        "default": False,
                    },
                },
                "required": ["main_file"],
            },
        ),
        Tool(
            name="get_component_info",
            description="Get comprehensive info about a NiceGUI component: documentation links, GitHub source URLs, inheritance chain, and source code.",
            inputSchema={
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "description": "Component name (e.g., 'ui.button', 'ui.table', 'Button', 'Element', 'ui.echart')",
                    },
                    "max_ancestors": {
                        "type": "integer",
                        "description": "Maximum number of ancestor classes to include (default: 3)",
                        "default": 3,
                    },
                    "include_source": {
                        "type": "boolean",
                        "description": "Whether to include full source code (default: true)",
                        "default": True,
                    },
                },
                "required": ["component"],
            },
        ),
        Tool(
            name="get_component_source",
            description="Get the source code of a NiceGUI component from the installed package. Fast, no network needed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "description": "Component name (e.g., 'ui.button', 'ui.table', 'button') or path (e.g., 'elements/button.py')",
                    },
                },
                "required": ["component"],
            },
        ),
        Tool(
            name="get_component_docs",
            description="Get the official NiceGUI documentation for a component. Downloads and caches locally.",
            inputSchema={
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "description": "Component name (e.g., 'ui.button', 'ui.table', 'button')",
                    },
                },
                "required": ["component"],
            },
        ),
        Tool(
            name="get_project_creation_guide",
            description="Get the guided project creation questionnaire and rules. Use this when the user wants to create a new NiceGUI project from scratch.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="kill_port_8080",
            description="Kill any process running on port 8080. Use this when you need to restart a NiceGUI app but the port is already in use. Always ask the user before calling this.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="open_browser",
            description="Open a URL in the user's default browser. Use this after starting a NiceGUI app to let the user interact with it. Default URL is http://localhost:8080.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to open (default: http://localhost:8080)",
                        "default": "http://localhost:8080",
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent]:
    """Handle tool calls."""
    
    if name == "list_topics":
        topics = get_topic_index()
        category = arguments.get('category', '')
        
        if category:
            topics = {k: v for k, v in topics.items() if v.get('category') == category}
        
        lines = ["# NiceGUI Documentation Topics\n"]
        
        # Group by category
        by_category: dict[str, list] = {}
        for topic_name, info in topics.items():
            cat = info.get('category', 'other')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((topic_name, info))
        
        for cat in ['mechanics', 'advanced', 'events', 'classes', 'samples']:
            if cat in by_category:
                lines.append(f"\n## {cat.title()}\n")
                for topic_name, info in by_category[cat]:
                    summary = info.get('summary', '')[:100]
                    lines.append(f"- **{topic_name}**: {summary}")
        
        return [TextContent(type="text", text='\n'.join(lines))]
    
    elif name == "get_topic":
        topic = arguments.get('topic', '')
        topics = get_topic_index()
        
        if topic not in topics:
            # Try partial match
            matches = [t for t in topics if topic.lower() in t.lower()]
            if matches:
                return [TextContent(
                    type="text",
                    text=f"Topic '{topic}' not found. Did you mean: {', '.join(matches)}?"
                )]
            return [TextContent(type="text", text=f"Topic '{topic}' not found. Use list_topics to see available topics.")]
        
        info = topics[topic]
        
        if info['category'] == 'samples':
            # Return sample info
            sample_path = PACKAGE_DIR / info['path']
            main_file = sample_path / 'main.py'
            if main_file.exists():
                content = main_file.read_text()
                return [TextContent(
                    type="text",
                    text=f"# Sample: {topic}\n\n{info.get('summary', '')}\n\n## main.py\n\n```python\n{content}\n```"
                )]
        else:
            # Return doc file
            doc_file = PACKAGE_DIR / info['file']
            if doc_file.exists():
                content = doc_file.read_text()
                return [TextContent(type="text", text=content)]
        
        return [TextContent(type="text", text=f"Could not load content for topic '{topic}'")]
    
    elif name == "search_topics":
        keyword = arguments.get('keyword', '').lower()
        topics = get_topic_index()
        
        matches = []
        for topic_name, info in topics.items():
            searchable = f"{topic_name} {info.get('summary', '')} {' '.join(info.get('tags', []))}".lower()
            if keyword in searchable:
                matches.append((topic_name, info))
        
        if not matches:
            return [TextContent(type="text", text=f"No topics found matching '{keyword}'")]
        
        lines = [f"# Topics matching '{keyword}'\n"]
        for topic_name, info in matches:
            summary = info.get('summary', '')[:100]
            lines.append(f"- **{topic_name}** ({info.get('category', '')}): {summary}")
        
        return [TextContent(type="text", text='\n'.join(lines))]
    
    elif name == "list_samples":
        samples = get_samples()
        
        lines = ["# NiceGUI Sample Applications\n"]
        for name, info in samples.items():
            tags = ', '.join(info.get('tags', [])[:5])
            summary = info.get('summary', '').split('\n')[0]
            lines.append(f"## {name}")
            lines.append(f"Tags: {tags}")
            lines.append(f"{summary}\n")
        
        return [TextContent(type="text", text='\n'.join(lines))]
    
    elif name == "get_sample_source":
        sample = arguments.get('sample', '')
        file = arguments.get('file', 'main.py')
        
        samples = get_samples()
        if sample not in samples:
            return [TextContent(type="text", text=f"Sample '{sample}' not found. Available: {', '.join(samples.keys())}")]
        
        sample_path = PACKAGE_DIR / samples[sample]['path']
        target_file = sample_path / file
        
        if not target_file.exists():
            # List available files
            files = [f.name for f in sample_path.iterdir() if f.is_file() and not f.name.startswith('.')]
            return [TextContent(type="text", text=f"File '{file}' not found. Available files: {', '.join(files)}")]
        
        content = target_file.read_text()
        return [TextContent(type="text", text=f"# {sample}/{file}\n\n```python\n{content}\n```")]
    
    elif name == "capture_sample_screenshot":
        sample = arguments.get('sample', '')
        path = arguments.get('path', '/')
        wait = arguments.get('wait', DEFAULT_WAIT)
        open_browser = arguments.get('open_browser', False)
        
        samples = get_samples()
        if sample not in samples:
            return [TextContent(type="text", text=f"Sample '{sample}' not found. Available: {', '.join(samples.keys())}")]
        
        sample_path = PACKAGE_DIR / samples[sample]['path']
        
        try:
            png_bytes = await capture_app_screenshot(sample_path, path, wait)
            b64_data = base64.standard_b64encode(png_bytes).decode('utf-8')
            
            # Also save as HTML for clients that can't display images
            html_path = save_screenshot_html(
                png_bytes, 
                f"Sample: {sample}",
                f"Screenshot of sample '{sample}' at path '{path}'",
                open_in_browser=open_browser
            )
            
            return [
                TextContent(type="text", text=f"Screenshot of {sample} at path '{path}':\n\n(HTML saved to: file://{html_path})"),
                ImageContent(type="image", data=b64_data, mimeType="image/png"),
            ]
        except Exception as e:
            return [TextContent(type="text", text=f"Error capturing screenshot: {e}")]
    
    elif name == "capture_url_screenshot":
        url = arguments.get('url', '')
        wait = arguments.get('wait', DEFAULT_WAIT)
        open_browser = arguments.get('open_browser', False)
        
        if not url:
            return [TextContent(type="text", text="URL is required")]
        
        try:
            png_bytes = await capture_screenshot(url, wait)
            b64_data = base64.standard_b64encode(png_bytes).decode('utf-8')
            
            # Also save as HTML for clients that can't display images
            html_path = save_screenshot_html(
                png_bytes, 
                f"Screenshot: {url}",
                f"Screenshot of {url}",
                open_in_browser=open_browser
            )
            
            return [
                TextContent(type="text", text=f"Screenshot of {url}:\n\n(HTML saved to: file://{html_path})"),
                ImageContent(type="image", data=b64_data, mimeType="image/png"),
            ]
        except Exception as e:
            return [TextContent(type="text", text=f"Error capturing screenshot: {e}")]
    
    elif name == "capture_app_screenshot":
        main_file = arguments.get('main_file', '')
        path = arguments.get('path', '/')
        wait = arguments.get('wait', DEFAULT_WAIT)
        open_browser = arguments.get('open_browser', False)
        
        if not main_file:
            return [TextContent(type="text", text="main_file is required (full path to main.py)")]
        
        main_path = Path(main_file)
        if not main_path.exists():
            return [TextContent(type="text", text=f"File not found: {main_file}")]
        
        if not main_path.name.endswith('.py'):
            return [TextContent(type="text", text=f"Expected a .py file, got: {main_path.name}")]
        
        app_dir = main_path.parent
        
        try:
            # Start the app, capture screenshot, stop it
            kill_port(PORT)
            
            process = subprocess.Popen(
                [sys.executable, main_path.name],
                cwd=app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            
            try:
                await asyncio.sleep(2)
                
                if process.poll() is not None:
                    stderr = process.stderr.read().decode() if process.stderr else ''
                    return [TextContent(type="text", text=f"App failed to start:\n{stderr}")]
                
                url = f'http://localhost:{PORT}{path}'
                png_bytes = await capture_screenshot(url, wait)
                b64_data = base64.standard_b64encode(png_bytes).decode('utf-8')
                
                # Also save as HTML for clients that can't display images
                html_path = save_screenshot_html(
                    png_bytes, 
                    f"App: {main_path.parent.name}",
                    f"Screenshot of {main_file} at path '{path}'",
                    open_in_browser=open_browser
                )
                
                return [
                    TextContent(type="text", text=f"Screenshot of {main_file} at path '{path}':\n\n(HTML saved to: file://{html_path})"),
                    ImageContent(type="image", data=b64_data, mimeType="image/png"),
                ]
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                kill_port(PORT)
                
        except Exception as e:
            return [TextContent(type="text", text=f"Error capturing screenshot: {e}")]
    
    elif name == "get_component_info":
        component = arguments.get('component', '')
        max_ancestors = arguments.get('max_ancestors', 3)
        include_source = arguments.get('include_source', True)
        
        if not component:
            return [TextContent(type="text", text="component is required")]
        
        try:
            cls = get_nicegui_class(component)
            if cls is None:
                # Provide helpful suggestions
                from nicegui import ui
                available = [attr for attr in dir(ui) if not attr.startswith('_')]
                return [TextContent(
                    type="text",
                    text=f"Component '{component}' not found.\n\nTry one of these formats:\n"
                         f"- ui.button, ui.table, ui.echart, etc.\n"
                         f"- Button, Table, Element (direct class names)\n\n"
                         f"Available ui elements: {', '.join(available[:30])}..."
                )]
            
            info = get_component_info(cls, max_ancestors, include_source)
            return [TextContent(type="text", text=info)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting component info: {e}")]
    
    elif name == "get_component_source":
        component = arguments.get('component', '')
        
        if not component:
            return [TextContent(type="text", text="component is required")]
        
        try:
            import nicegui
            nicegui_dir = Path(nicegui.__file__).parent
            
            # Check if it's a component name (ui.xxx format)
            if component.startswith('ui.'):
                element_name = component[3:]
                path = f"elements/{element_name}.py"
            elif '/' not in component and '.' not in component:
                # Assume it's an element name without ui. prefix
                path = f"elements/{component.lower()}.py"
            else:
                path = component
            
            # Read source code
            target_path = (nicegui_dir / path).resolve()
            
            # Security: ensure path doesn't escape nicegui directory
            if not str(target_path).startswith(str(nicegui_dir)):
                return [TextContent(type="text", text="Invalid path: cannot access files outside nicegui package")]
            
            if not target_path.exists():
                # Try without .py extension or with different casing
                alternatives = [
                    nicegui_dir / f"{path}.py",
                    nicegui_dir / f"elements/{path}.py",
                    nicegui_dir / f"elements/{path}",
                ]
                for alt in alternatives:
                    if alt.exists():
                        target_path = alt
                        break
                else:
                    # List available files/dirs at the requested level
                    parent = target_path.parent
                    if parent.exists() and parent.is_dir():
                        items = sorted([p.name for p in parent.iterdir() if not p.name.startswith('_')])
                        return [TextContent(
                            type="text",
                            text=f"File not found: {path}\n\nAvailable in {parent.relative_to(nicegui_dir)}:\n" + 
                                 '\n'.join(f"  - {item}" for item in items[:30])
                        )]
                    return [TextContent(type="text", text=f"File not found: {path}")]
            
            if target_path.is_dir():
                # List directory contents
                items = sorted([p.name for p in target_path.iterdir() if not p.name.startswith('_')])
                return [TextContent(
                    type="text",
                    text=f"# Directory: nicegui/{path}\n\n" + '\n'.join(f"- {item}" for item in items)
                )]
            
            # Read file
            content = target_path.read_text()
            rel_path = target_path.relative_to(nicegui_dir)
            return [TextContent(
                type="text",
                text=f"# nicegui/{rel_path}\n\n```python\n{content}\n```"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error reading source: {e}")]
    
    elif name == "get_component_docs":
        component = arguments.get('component', '')
        
        if not component:
            return [TextContent(type="text", text="component is required")]
        
        try:
            # Normalize component name
            if component.startswith('ui.'):
                doc_name = component[3:]
            else:
                doc_name = component.lower()
            
            # Check if we have local docs in nice-vibes
            local_doc = DOCS_DIR / 'classes' / f'{doc_name}.md'
            if local_doc.exists():
                content = local_doc.read_text()
                return [TextContent(type="text", text=f"# Documentation: {doc_name}\n\n{content}")]
            
            # Check cache directory
            cache_dir = PACKAGE_DIR / '.cache' / 'docs'
            cache_dir.mkdir(parents=True, exist_ok=True)
            cached_doc = cache_dir / f'{doc_name}.md'
            
            if cached_doc.exists():
                content = cached_doc.read_text()
                return [TextContent(type="text", text=f"# Documentation: {doc_name} (cached)\n\n{content}")]
            
            # Download from GitHub and cache
            docs_url = get_docs_url(doc_name)
            try:
                import urllib.request
                with urllib.request.urlopen(docs_url, timeout=10) as response:
                    content = response.read().decode('utf-8')
                
                # Cache it
                cached_doc.write_text(content)
                return [TextContent(type="text", text=f"# Documentation: {doc_name}\n\n{content}")]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"# Documentation for {doc_name}\n\n"
                         f"Could not fetch documentation: {e}\n\n"
                         f"**URL:** {docs_url}"
                )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting docs: {e}")]
    
    elif name == "get_project_creation_guide":
        guide_file = DOCS_DIR / 'project_creation_guide.md'
        if guide_file.exists():
            content = guide_file.read_text()
            return [TextContent(type="text", text=content)]
        return [TextContent(type="text", text="Project creation guide not found.")]
    
    elif name == "kill_port_8080":
        try:
            result = subprocess.run(
                'lsof -ti:8080 | xargs kill -9',
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return [TextContent(type="text", text="Killed process on port 8080. Port is now free.")]
            else:
                return [TextContent(type="text", text="No process found on port 8080. Port is already free.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error killing process: {e}")]
    
    elif name == "open_browser":
        url = arguments.get('url', 'http://localhost:8080')
        try:
            webbrowser.open(url)
            return [TextContent(type="text", text=f"Opened {url} in the default browser.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error opening browser: {e}")]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]


# ============================================================================
# MCP Resources (optional - for direct doc access)
# ============================================================================

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    resources = []
    
    # Add main prompt
    resources.append(Resource(
        uri="nicegui://prompt/optimum",
        name="NiceGUI Optimum Prompt",
        description="The optimum NiceGUI prompt (~24K tokens)",
        mimeType="text/markdown",
    ))
    
    # Add topic index
    resources.append(Resource(
        uri="nicegui://topics",
        name="Topic Index",
        description="Index of all NiceGUI documentation topics",
        mimeType="text/markdown",
    ))
    
    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource."""
    if uri == "nicegui://prompt/optimum":
        prompt_file = PACKAGE_DIR / 'output' / 'nice_vibes.md'
        if prompt_file.exists():
            return prompt_file.read_text()
        return "Prompt file not found. Run build_master_prompt.py first."
    
    elif uri == "nicegui://topics":
        topics = get_topic_index()
        lines = ["# NiceGUI Topic Index\n"]
        for name, info in topics.items():
            lines.append(f"- {name}: {info.get('summary', '')[:80]}")
        return '\n'.join(lines)
    
    return f"Unknown resource: {uri}"


# ============================================================================
# Main
# ============================================================================

async def main():
    """Run the MCP server."""
    import sys
    print("Nice Vibes MCP Server starting...", file=sys.stderr)
    print(f"Topics loaded: {len(get_topic_index())}", file=sys.stderr)
    print("Waiting for MCP client connection...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

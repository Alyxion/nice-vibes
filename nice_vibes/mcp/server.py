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
    format: str = 'JPEG',
    quality: int = 85,
) -> bytes:
    """Capture a screenshot and return as image bytes.

    Args:
        url: URL to capture
        wait_seconds: Time to wait for page to load
        width: Output image width
        format: Image format ('JPEG' or 'PNG')
        quality: JPEG quality (1-100), ignored for PNG
    """
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

        # Convert to RGB for JPEG (removes alpha channel)
        if format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')

        # Save to bytes
        output = io.BytesIO()
        save_kwargs = {'format': format.upper()}
        if format.upper() == 'JPEG':
            save_kwargs['quality'] = quality
        img.save(output, **save_kwargs)
        return output.getvalue()

    finally:
        driver.quit()


async def capture_screenshot(
    url: str,
    wait_seconds: int = DEFAULT_WAIT,
    width: int = OUTPUT_WIDTH,
    format: str = 'JPEG',
    quality: int = 85,
) -> bytes:
    """Async wrapper for screenshot capture."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: capture_screenshot_sync(url, wait_seconds, width, format, quality),
    )


async def capture_app_screenshot(
    app_dir: Path,
    path: str = '/',
    wait_seconds: int = DEFAULT_WAIT,
    format: str = 'JPEG',
    quality: int = 85,
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
        return await capture_screenshot(url, wait_seconds, format=format, quality=quality)

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
            name="capture_url_screenshot",
            description="Capture a screenshot of any URL. Use this to visually debug a RUNNING NiceGUI application at localhost:8080. Returns an image.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Full URL to capture (default: http://localhost:8080)",
                        "default": "http://localhost:8080",
                    },
                    "wait": {
                        "type": "integer",
                        "description": "Seconds to wait after page load (default: 3)",
                        "default": 3,
                    },
                    "format": {
                        "type": "string",
                        "description": "Image format: 'JPEG' or 'PNG' (default: JPEG)",
                        "enum": ["JPEG", "PNG"],
                        "default": "JPEG",
                    },
                    "quality": {
                        "type": "integer",
                        "description": "JPEG quality 1-100 (default: 85). Ignored for PNG.",
                        "default": 85,
                        "minimum": 1,
                        "maximum": 100,
                    },
                },
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
            name="project_setup",
            description="Get file and folder creation instructions for setting up a new NiceGUI project. Returns a structured list of folders to create and files with their content. Always uses clean Python package structure. IMPORTANT: Never overwrite existing files - check first before writing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Human-readable project name (e.g., 'My Dashboard App')",
                    },
                    "project_type": {
                        "type": "string",
                        "description": "Project structure: single_page (one page app) or spa (multi-page with ui.sub_pages, layout, components)",
                        "enum": ["single_page", "spa"],
                        "default": "single_page",
                    },
                    "include_mcp_rules": {
                        "type": "boolean",
                        "description": "Include MCP-based editor rules (default: true). Set to false for GitHub markdown-only rules.",
                        "default": True,
                    },
                },
                "required": ["project_name"],
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
    
    elif name == "capture_url_screenshot":
        url = arguments.get('url', 'http://localhost:8080')
        wait = arguments.get('wait', DEFAULT_WAIT)
        format = arguments.get('format', 'JPEG').upper()
        quality = arguments.get('quality', 85)

        try:
            image_bytes = await capture_screenshot(url, wait, format=format, quality=quality)
            b64_data = base64.standard_b64encode(image_bytes).decode('utf-8')
            mime_type = 'image/jpeg' if format == 'JPEG' else 'image/png'

            return [ImageContent(type="image", data=b64_data, mimeType=mime_type)]
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

    elif name == "project_setup":
        project_name = arguments.get('project_name', 'My NiceGUI App')
        project_type = arguments.get('project_type', 'single_page')
        include_mcp = arguments.get('include_mcp_rules', True)

        # Convert to snake_case for package name
        import re
        pkg = re.sub(r'[^a-zA-Z0-9]+', '_', project_name.lower()).strip('_')

        # Common rules content
        mcp_rules = '''- Use nice-vibes MCP tools for docs, samples, and component details
- Use `capture_url_screenshot` to verify visual changes
'''
        no_mcp_rules = '''- Reference Nice Vibes prompts for NiceGUI documentation:
  - https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes.md
'''
        rules_suffix = mcp_rules if include_mcp else no_mcp_rules

        # Build the setup instructions
        setup = {
            "project_name": project_name,
            "project_slug": pkg,
            "project_type": project_type,
            "instructions": "Create the folders and files below. NEVER overwrite existing files - skip any file that already exists.",
            "folders": [pkg],
            "files": []
        }

        # Run command depends on structure
        run_cmd = f"poetry run python -m {pkg}.main"

        # pyproject.toml
        setup["files"].append({
            "path": "pyproject.toml",
            "description": "Poetry project configuration",
            "content": f'''[tool.poetry]
name = "{pkg}"
version = "0.1.0"
description = "{project_name}"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
package-mode = false

[tool.poetry.dependencies]
python = "^3.12"
nicegui = "^3.3.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
'''
        })

        # README.md
        setup["files"].append({
            "path": "README.md",
            "description": "Project readme",
            "content": f'''# {project_name}

A NiceGUI application.

## Setup

```bash
poetry install
{run_cmd}
```

Then open http://localhost:8080 in your browser.
'''
        })

        # .gitignore
        setup["files"].append({
            "path": ".gitignore",
            "description": "Git ignore file",
            "content": '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
ENV/

# Poetry
poetry.lock

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# NiceGUI
.nicegui/
'''
        })

        # CLAUDE.md
        setup["files"].append({
            "path": "CLAUDE.md",
            "description": "Instructions for Claude Code",
            "content": f'''# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

{project_name} - A NiceGUI web application.

## Commands

```bash
# Install dependencies
poetry install

# Run the application
{run_cmd}

# Run tests
poetry run pytest -v
```

## Rules

- Always use `poetry run ...` to run commands
- Keep NiceGUI on port 8080 - if blocked, kill the existing process first
- NiceGUI hot-reloads on file changes - no need to restart the server
- Do not open a browser automatically
{rules_suffix}'''
        })

        # .windsurf/rules/rules.md
        setup["folders"].extend([".windsurf", ".windsurf/rules"])
        setup["files"].append({
            "path": ".windsurf/rules/rules.md",
            "description": "Instructions for Windsurf Cascade",
            "content": f'''# Windsurf Rules

## Project Overview

{project_name} - A NiceGUI web application.

## Commands

```bash
# Install dependencies
poetry install

# Run the application
{run_cmd}

# Run tests (do NOT pipe output)
poetry run pytest -v
```

## Rules

- Always use `poetry run ...` to run commands
- Keep NiceGUI on port 8080 - if blocked, kill the existing process first
- NiceGUI hot-reloads on file changes - no need to restart the server
- Do not open a browser automatically
{rules_suffix}'''
        })

        # AGENTS.md
        mcp_section = '''
## MCP Integration

If the nice-vibes MCP server is available:
- Use it for NiceGUI documentation, samples, and component details
- Use `capture_url_screenshot` to verify visual changes at http://localhost:8080
'''
        no_mcp_section = '''
## Documentation

Reference Nice Vibes prompts for NiceGUI documentation:
- Compact (~14K): https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_compact.md
- Optimum (~23K): https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes.md
- Extended (~34K): https://raw.githubusercontent.com/Alyxion/nice-vibes/refs/heads/main/output/nice_vibes_extended.md
'''
        setup["files"].append({
            "path": "AGENTS.md",
            "description": "General instructions for AI agents",
            "content": f'''# {project_name} - Project Rules

Rules for AI agents working on this repository.

## Environment

This is a Poetry project using NiceGUI.

## Commands

```bash
# Install dependencies
poetry install

# Run the application
{run_cmd}

# Run tests (do NOT pipe output)
poetry run pytest -v
```

## Rules

- Always use `poetry run ...` to run commands
- Keep NiceGUI on port 8080 - if blocked, kill the existing process first
- NiceGUI hot-reloads on file changes - no need to restart the server
- Do not open a browser automatically
{mcp_section if include_mcp else no_mcp_section}'''
        })

        # === Project type specific files ===

        if project_type == "single_page":
            # Simple single-page app
            setup["files"].append({
                "path": f"{pkg}/__init__.py",
                "description": "Package init",
                "content": f'"""{project_name} package."""\n'
            })

            setup["files"].append({
                "path": f"{pkg}/main.py",
                "description": "Application entry point",
                "content": f'''"""{project_name} - A NiceGUI application."""

from dataclasses import dataclass

from nicegui import ui


@dataclass
class AppState:
    """Application state."""
    value: str = ''


@ui.page('/')
def index():
    state = AppState()

    with ui.header().classes('bg-primary'):
        ui.label('{project_name}').classes('text-xl font-bold')

    with ui.card().classes('max-w-md mx-auto mt-8 p-6'):
        ui.input('Enter something').bind_value(state, 'value')
        ui.label().bind_text_from(state, 'value', lambda v: f'You entered: {{v}}')


if __name__ in {{'__main__', '__mp_main__'}}:
    ui.run(title='{project_name}', show=False)
'''
            })

        elif project_type == "spa":
            # SPA with layout, pages, components, static (following multi_dashboard patterns)
            setup["folders"].extend([
                f"{pkg}/pages",
                f"{pkg}/pages/home",
                f"{pkg}/pages/settings",
                f"{pkg}/components",
                f"{pkg}/static",
                f"{pkg}/static/css",
                f"{pkg}/static/js",
            ])

            setup["files"].append({
                "path": f"{pkg}/__init__.py",
                "description": "Package init",
                "content": f'"""{project_name} package."""\n'
            })

            setup["files"].append({
                "path": f"{pkg}/main.py",
                "description": "Application entry point",
                "content": f'''"""{project_name} - A NiceGUI SPA application.

Uses root page + ui.sub_pages for SPA-style navigation with persistent state.
"""
from pathlib import Path

from nicegui import app, ui

from .layout import AppLayout

# Static files
STATIC_DIR = Path(__file__).parent / 'static'
PAGES_DIR = Path(__file__).parent / 'pages'

app.add_static_files('/static', STATIC_DIR)

# Discover pages at startup
AppLayout.discover_pages(str(PAGES_DIR))


async def root():
    """Root page entry point."""
    await AppLayout.current().build()


if __name__ in {{'__main__', '__mp_main__'}}:
    ui.run(
        root,
        show=False,
        title='{project_name}',
        reload=True,
        uvicorn_reload_includes='*.py,*.js,*.css',
    )
'''
            })

            setup["files"].append({
                "path": f"{pkg}/layout.py",
                "description": "App layout with header, drawer, and sub_pages routing",
                "content": f'''"""Application layout with navigation."""
import importlib
from pathlib import Path

from nicegui import app, ui


class AppLayout:
    """Application layout managing header, drawer, and page routing."""

    # Class-level page registry (populated once at startup)
    _pages: list[dict] = None

    def __init__(self):
        self.header: ui.header = None
        self.drawer: ui.left_drawer = None

    @classmethod
    def current(cls) -> 'AppLayout':
        """Get or create the layout for this client."""
        if 'layout' not in app.storage.client:
            app.storage.client['layout'] = cls()
        return app.storage.client['layout']

    @classmethod
    def discover_pages(cls, package_path: str, exclude: set[str] = None) -> list[dict]:
        """Auto-discover page classes with PAGE = {{'path': '...', 'label': '...', 'icon': '...'}} attribute."""
        exclude = exclude or set()
        is_page = lambda obj: isinstance(obj, type) and isinstance(getattr(obj, 'PAGE', None), dict)
        pages = []
        for item in Path(package_path).iterdir():
            if item.is_dir() and item.name not in exclude and (item / '__init__.py').exists():
                module = importlib.import_module(f'{pkg}.pages.{{item.name}}')
                for name in dir(module):
                    obj = getattr(module, name)
                    if is_page(obj):
                        pages.append({{**obj.PAGE, 'page_class': obj}})
        cls._pages = sorted(pages, key=lambda p: (p['path'] != '/', p['path']))
        return cls._pages

    @classmethod
    def pages(cls) -> list[dict]:
        """Get all discovered pages."""
        return cls._pages or []

    def make_page_builder(self, page_info: dict):
        """Create an async builder for a page."""
        async def builder():
            await page_info['page_class']().build()
        return builder

    async def build(self) -> None:
        """Build the complete layout."""
        ui.add_head_html('<link rel="stylesheet" href="/static/css/app.css">')

        # Header
        self.header = ui.header().classes('bg-primary items-center')
        with self.header:
            ui.button(icon='menu', on_click=lambda: self.drawer.toggle()).props('flat round color=white')
            ui.label('{project_name}').classes('text-xl text-white ml-2')
            ui.space()
            dark = ui.dark_mode()
            ui.button(icon='dark_mode', on_click=lambda: setattr(dark, 'value', not dark.value)).props('flat round color=white')

        # Navigation Drawer
        self.drawer = ui.left_drawer(value=True).classes('bg-slate-50 dark:bg-slate-800')
        with self.drawer:
            ui.label('Navigation').classes('text-lg font-bold p-4')
            with ui.list().classes('w-full'):
                for page in self.pages():
                    with ui.item(on_click=lambda p=page['path']: ui.navigate.to(p)).classes('rounded-lg mx-2'):
                        with ui.item_section().props('avatar'):
                            ui.icon(page['icon']).classes('text-indigo-500')
                        with ui.item_section():
                            ui.item_label(page['label'])

        # Page content via sub_pages
        with ui.column().classes('w-full h-full p-0'):
            ui.sub_pages({{page['path']: self.make_page_builder(page) for page in self.pages()}})
'''
            })

            # Pages
            setup["files"].append({
                "path": f"{pkg}/pages/__init__.py",
                "description": "Pages package",
                "content": '"""Page modules."""\n'
            })

            setup["files"].append({
                "path": f"{pkg}/pages/home/__init__.py",
                "description": "Home page module",
                "content": 'from .home import HomePage\n\n__all__ = ["HomePage"]\n'
            })

            setup["files"].append({
                "path": f"{pkg}/pages/home/home.py",
                "description": "Home page implementation with async build",
                "content": '''"""Home page."""
from nicegui import ui


class HomePage:
    """Home page - the default landing page."""
    PAGE = {'path': '/', 'label': 'Home', 'icon': 'home'}

    async def build(self) -> None:
        """Build the page content."""
        with ui.column().classes('w-full p-6'):
            with ui.row().classes('items-center mb-4'):
                ui.icon('home').classes('text-3xl text-indigo-500')
                ui.label('Welcome').classes('text-2xl font-bold ml-2')

            with ui.card().classes('w-full max-w-2xl'):
                ui.label('This is the home page of your SPA application.')
                ui.label('Navigate using the drawer on the left.')
'''
            })

            setup["files"].append({
                "path": f"{pkg}/pages/settings/__init__.py",
                "description": "Settings page module",
                "content": 'from .settings import SettingsPage\n\n__all__ = ["SettingsPage"]\n'
            })

            setup["files"].append({
                "path": f"{pkg}/pages/settings/settings.py",
                "description": "Settings page implementation with async build",
                "content": '''"""Settings page."""
from nicegui import ui


class SettingsPage:
    """Settings page for application configuration."""
    PAGE = {'path': '/settings', 'label': 'Settings', 'icon': 'settings'}

    async def build(self) -> None:
        """Build the page content."""
        with ui.column().classes('w-full p-6'):
            with ui.row().classes('items-center mb-4'):
                ui.icon('settings').classes('text-3xl text-indigo-500')
                ui.label('Settings').classes('text-2xl font-bold ml-2')

            with ui.card().classes('w-full max-w-2xl'):
                ui.label('Application Settings').classes('font-semibold mb-4')
                ui.switch('Enable notifications')
                ui.switch('Dark mode by default')
'''
            })

            # Components
            setup["files"].append({
                "path": f"{pkg}/components/__init__.py",
                "description": "Reusable components package",
                "content": '"""Reusable UI components."""\n'
            })

            # Static files
            setup["files"].append({
                "path": f"{pkg}/static/css/app.css",
                "description": "Custom CSS styles",
                "content": '''/* Custom styles for the application */

.nav-drawer {
    border-right: 1px solid rgba(0, 0, 0, 0.1);
}

.dark .nav-drawer {
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}
'''
            })

            setup["files"].append({
                "path": f"{pkg}/static/js/app.js",
                "description": "Custom JavaScript",
                "content": '''// Custom JavaScript for the application
'''
            })

        import json
        return [TextContent(type="text", text=json.dumps(setup, indent=2))]

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
    # Be defensive: depending on MCP client/library versions, `uri` may include
    # surrounding whitespace or arrive wrapped in a dict.
    if isinstance(uri, dict) and 'uri' in uri:
        uri = uri['uri']
    uri = str(uri).strip()

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

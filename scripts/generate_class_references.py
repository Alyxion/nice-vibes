#!/usr/bin/env python3
"""
Generate reference files with source code paths and documentation URLs for each class.

Usage:
    python scripts/generate_class_references.py
"""

import inspect
import re
import sys
from pathlib import Path

import nicegui
from nicegui import ui, app, html, binding, run, background_tasks


# Base URLs
NICEGUI_DOCS_BASE = "https://nicegui.io/documentation"
NICEGUI_GITHUB_BASE = "https://github.com/zauberzeug/nicegui/blob/main"


def get_source_path(obj) -> str | None:
    """Get the source file path relative to nicegui package."""
    try:
        source_file = inspect.getfile(obj)
        # Get path relative to nicegui package
        nicegui_path = Path(nicegui.__file__).parent
        source_path = Path(source_file)
        
        if nicegui_path in source_path.parents or source_path.parent == nicegui_path:
            rel_path = source_path.relative_to(nicegui_path.parent)
            return str(rel_path)
    except (TypeError, OSError):
        pass
    return None


def get_doc_url(namespace: str, name: str) -> str:
    """Generate documentation URL for a class."""
    # Most ui elements have their own doc page
    if namespace == "ui":
        # Handle special cases
        doc_name = name.lower()
        return f"{NICEGUI_DOCS_BASE}/{doc_name}"
    elif namespace == "app":
        if "storage" in name:
            return f"{NICEGUI_DOCS_BASE}/storage"
        return f"{NICEGUI_DOCS_BASE}/section_configuration_deployment"
    elif namespace == "html":
        return f"{NICEGUI_DOCS_BASE}/html#other_html_elements"
    elif namespace == "binding":
        return f"{NICEGUI_DOCS_BASE}/section_binding_properties"
    elif namespace == "run":
        return f"{NICEGUI_DOCS_BASE}/section_action_events"
    elif namespace == "background_tasks":
        return f"{NICEGUI_DOCS_BASE}/section_action_events"
    
    return NICEGUI_DOCS_BASE


def resolve_object(full_name: str):
    """Resolve a dotted name to an object."""
    # Known runtime-only references
    RUNTIME_ONLY = {
        'app.storage.browser',
        'app.storage.user',
        'app.storage.tab',
        'app.storage.client',
        'app.storage.general',
        'app.native',
        'ui.context',
    }
    
    if full_name in RUNTIME_ONLY:
        return None
    
    parts = full_name.split('.')
    root = parts[0]
    
    modules = {
        'ui': ui,
        'app': app,
        'html': html,
        'binding': binding,
        'run': run,
        'background_tasks': background_tasks,
    }
    
    if root not in modules:
        return None
    
    obj = modules[root]
    
    for part in parts[1:]:
        try:
            obj = getattr(obj, part)
        except (AttributeError, RuntimeError):
            return None
    
    return obj


def get_base_classes(obj) -> list[str]:
    """Get relevant NiceGUI base classes for an object."""
    if not inspect.isclass(obj):
        return []
    
    # Important base classes to track
    important_bases = {
        'Element': 'ui.element',
        'ValueElement': 'ValueElement',
        'DisableableElement': 'DisableableElement',
        'ContentElement': 'ContentElement',
        'SourceElement': 'SourceElement',
        'ChoiceElement': 'ChoiceElement',
        'ValidationElement': 'ValidationElement',
    }
    
    bases = []
    for cls in obj.__mro__[1:]:  # Skip self
        cls_name = cls.__name__
        if cls_name in important_bases:
            bases.append(important_bases[cls_name])
        if cls_name == 'Element':
            break  # Stop at Element base
    
    return bases


def get_documented_classes(md_file: Path) -> dict[str, str]:
    """Extract all class references and their descriptions from a markdown file."""
    content = md_file.read_text()
    
    classes: dict[str, str] = {}
    
    # Pattern to match table rows with 2 columns: | `ui.class` | Description |
    table_pattern_2col = re.compile(r'\|\s*`(ui|app|html|binding|run|background_tasks)\.([a-zA-Z0-9_\.]+)`\s*\|\s*([^|]+)\s*\|')
    
    for match in table_pattern_2col.finditer(content):
        namespace = match.group(1)
        name = match.group(2)
        description = match.group(3).strip()
        full_name = f"{namespace}.{name}"
        
        # Keep the first (most specific) description found
        if full_name not in classes:
            classes[full_name] = description
    
    # Pattern to match table rows with 3 columns: | `app.storage.x` | Scope | Persistence |
    # Use scope as description
    table_pattern_3col = re.compile(r'\|\s*`(app)\.([a-zA-Z0-9_\.]+)`\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|')
    
    for match in table_pattern_3col.finditer(content):
        namespace = match.group(1)
        name = match.group(2)
        scope = match.group(3).strip()
        persistence = match.group(4).strip()
        full_name = f"{namespace}.{name}"
        
        if full_name not in classes:
            classes[full_name] = f"{scope} ({persistence})"
    
    # Also find any backtick references not in tables (fallback, no description)
    backtick_pattern = re.compile(r'`(ui|app|html|binding|run|background_tasks)\.([a-zA-Z0-9_\.]+)`')
    for match in backtick_pattern.finditer(content):
        namespace = match.group(1)
        name = match.group(2)
        full_name = f"{namespace}.{name}"
        if full_name not in classes:
            classes[full_name] = ""
    
    return classes


def generate_reference_content(classes: dict[str, str]) -> str:
    """Generate markdown content with source and doc references."""
    lines = [
        "# Class References",
        "",
        "Source code locations and documentation URLs for further investigation.",
        "",
        "| Class | Description | Inherits | Source | Documentation |",
        "|-------|-------------|----------|--------|---------------|",
    ]
    
    # Known descriptions for common classes without table entries
    KNOWN_DESCRIPTIONS = {
        'ui.element': 'Base class for all UI elements',
        'ui.refreshable': 'Decorator for refreshable UI sections',
        'ui.state': 'Reactive state for refreshable UI',
        'ui.context': 'Get current UI context',
        'ui.run': 'Start the NiceGUI server',
        'ui.page': 'Decorator to define a page route',
        'ui.navigate': 'Browser navigation control',
        'ui.notify': 'Show notification toast',
        'ui.timer': 'Periodic/delayed function calls',
        'ui.update': 'Send updates to client',
        'ui.download': 'Trigger file download',
        'ui.clipboard': 'Browser clipboard access',
        'ui.keyboard': 'Keyboard event handler',
        'ui.colors': 'Set color theme',
        'ui.dark_mode': 'Dark mode control',
        'ui.query': 'Query/modify HTML elements',
        'ui.add_css': 'Add CSS to page',
        'ui.add_head_html': 'Add HTML to <head>',
        'ui.add_body_html': 'Add HTML to <body>',
        'ui.run_javascript': 'Execute JavaScript on client',
        'ui.run_with': 'Attach to existing FastAPI app',
        'app.native': 'Native mode configuration',
        'app.shutdown': 'Shut down the app',
    }
    
    for class_name in sorted(classes.keys()):
        description = classes[class_name]
        
        # Use known description if empty
        if not description and class_name in KNOWN_DESCRIPTIONS:
            description = KNOWN_DESCRIPTIONS[class_name]
        
        parts = class_name.split('.')
        namespace = parts[0]
        name = parts[1] if len(parts) > 1 else ""
        
        # Get source path and base classes
        obj = resolve_object(class_name)
        if obj:
            source_path = get_source_path(obj)
            if source_path:
                source_link = f"[source]({NICEGUI_GITHUB_BASE}/{source_path})"
            else:
                source_link = "—"
            
            # Get base classes
            bases = get_base_classes(obj)
            inherits = " → ".join(bases) if bases else "—"
        else:
            # For runtime-only objects, try to guess the source
            if "storage" in class_name:
                source_link = f"[source]({NICEGUI_GITHUB_BASE}/nicegui/storage.py)"
            else:
                source_link = "—"
            inherits = "—"
        
        # Get doc URL
        doc_url = get_doc_url(namespace, name)
        doc_link = f"[docs]({doc_url})"
        
        lines.append(f"| `{class_name}` | {description} | {inherits} | {source_link} | {doc_link} |")
    
    lines.append("")
    return "\n".join(lines)


def main():
    docs_dir = Path(__file__).parent.parent / 'docs' / 'classes'
    
    if not docs_dir.exists():
        print(f"Error: {docs_dir} does not exist")
        sys.exit(1)
    
    print(f"Scanning {docs_dir}...\n")
    
    generated = 0
    
    for md_file in sorted(docs_dir.glob('*.md')):
        # Skip reference files
        if md_file.stem.endswith('_references'):
            continue
        
        classes = get_documented_classes(md_file)
        
        if not classes:
            continue
        
        # Generate reference file
        ref_file = md_file.with_stem(f"{md_file.stem}_references")
        content = generate_reference_content(classes)
        ref_file.write_text(content)
        
        print(f"✅ Generated {ref_file.name} ({len(classes)} classes)")
        generated += 1
    
    print(f"\nGenerated {generated} reference files")
    return 0


if __name__ in {'__main__', '__mp_main__'}:
    sys.exit(main())

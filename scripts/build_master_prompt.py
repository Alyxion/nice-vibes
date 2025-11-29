#!/usr/bin/env python3
"""Build master prompt files from all documentation.

Generates prompt variants in online and offline versions:
- compact: Core mechanics only (smallest)
- optimum: Core + events + classes (balanced)
- extended: Everything including advanced topics (full)

Online versions reference GitHub URLs for excluded content.
Offline versions reference local file paths.

Uses docs/prompt_config.yaml to control file order and exclusions.
"""

import argparse
import re
from fnmatch import fnmatch
from pathlib import Path
from dataclasses import dataclass, field

import tiktoken
import yaml


DEFAULT_GITHUB_URL = 'https://github.com/Alyxion/nice-prompt'


@dataclass
class PromptVariant:
    """Configuration for a prompt variant."""
    name: str
    suffix: str
    description: str
    include_adv_mechanics: bool
    include_events: bool
    include_classes: bool


@dataclass
class FileEntry:
    """A file entry with optional summary."""
    filename: str
    summary: str = ''


VARIANTS = [
    PromptVariant(
        name='compact',
        suffix='_compact',
        description='Core mechanics only - minimal token usage',
        include_adv_mechanics=False,
        include_events=False,
        include_classes=False,
    ),
    PromptVariant(
        name='optimum',
        suffix='',  # Default/main file
        description='Core + events + classes - balanced coverage',
        include_adv_mechanics=False,
        include_events=True,
        include_classes=True,
    ),
    PromptVariant(
        name='extended',
        suffix='_extended',
        description='Full documentation including advanced topics',
        include_adv_mechanics=True,
        include_events=True,
        include_classes=True,
    ),
]


def load_config() -> dict:
    """Load prompt configuration from YAML."""
    root = Path(__file__).parent.parent
    config_path = root / 'docs' / 'prompt_config.yaml'
    
    if not config_path.exists():
        raise FileNotFoundError(f'Config not found: {config_path}')
    
    with open(config_path) as f:
        return yaml.safe_load(f)


def parse_file_entries(items: list) -> list[FileEntry]:
    """Parse config items into FileEntry objects."""
    entries = []
    for item in items:
        if isinstance(item, str):
            entries.append(FileEntry(filename=item))
        elif isinstance(item, dict):
            entries.append(FileEntry(
                filename=item.get('file', item.get('filename', '')),
                summary=item.get('summary', '')
            ))
    return entries


def should_exclude(filename: str, exclude_patterns: list[str]) -> bool:
    """Check if file matches any exclude pattern."""
    for pattern in exclude_patterns:
        if fnmatch(filename, pattern):
            return True
    return False


def collect_files_and_refs(variant: PromptVariant) -> tuple[list[Path], list[tuple[str, str, str]]]:
    """Collect included files and references to excluded content.
    
    Returns:
        Tuple of (included_files, excluded_refs) where excluded_refs is
        list of (category, relative_path, summary) tuples.
    """
    root = Path(__file__).parent.parent
    docs_dir = root / 'docs'
    config = load_config()
    
    files = []
    excluded_refs = []
    exclude_patterns = config.get('exclude', [])
    
    # Main guide first (always included)
    main_guide = config.get('main_guide')
    if main_guide:
        files.append(docs_dir / main_guide)
    
    # Core mechanics (always included)
    mechanics_dir = docs_dir / 'mechanics'
    mechanics_entries = parse_file_entries(config.get('mechanics', []))
    for entry in mechanics_entries:
        path = mechanics_dir / entry.filename
        if path.exists() and not should_exclude(entry.filename, exclude_patterns):
            files.append(path)
    
    # Advanced mechanics
    adv_entries = parse_file_entries(config.get('adv_mechanics', []))
    for entry in adv_entries:
        path = mechanics_dir / entry.filename
        if path.exists() and not should_exclude(entry.filename, exclude_patterns):
            if variant.include_adv_mechanics:
                files.append(path)
            else:
                excluded_refs.append(('Advanced Mechanics', f'docs/mechanics/{entry.filename}', entry.summary))
    
    # Events
    events_dir = docs_dir / 'events'
    event_entries = parse_file_entries(config.get('events', []))
    for entry in event_entries:
        path = events_dir / entry.filename
        if path.exists() and not should_exclude(entry.filename, exclude_patterns):
            if variant.include_events:
                files.append(path)
            else:
                excluded_refs.append(('Events', f'docs/events/{entry.filename}', entry.summary))
    
    # Classes
    classes_dir = docs_dir / 'classes'
    class_entries = parse_file_entries(config.get('classes', []))
    for entry in class_entries:
        path = classes_dir / entry.filename
        if path.exists() and not should_exclude(entry.filename, exclude_patterns):
            if variant.include_classes:
                files.append(path)
            else:
                excluded_refs.append(('Class Reference', f'docs/classes/{entry.filename}', entry.summary))
    
    return files, excluded_refs


def convert_relative_paths(content: str, file_path: Path, github_url: str, online: bool, root: Path) -> str:
    """Convert relative markdown links to absolute paths.
    
    Converts links like [text](events/file.md) to absolute GitHub URLs or docs/ paths.
    """
    # Pattern matches markdown links: [text](relative/path.md)
    # Excludes links starting with http, https, #, or /
    pattern = r'\[([^\]]+)\]\((?!https?://|#|/)([^)]+\.md)\)'
    
    def replace_link(match: re.Match) -> str:
        text = match.group(1)
        relative_path = match.group(2)
        
        # Resolve the path relative to the file's directory
        file_dir = file_path.parent
        resolved = (file_dir / relative_path).resolve()
        
        # Get path relative to project root
        try:
            full_path = str(resolved.relative_to(root))
        except ValueError:
            # Fallback if resolution fails
            full_path = f'docs/{relative_path}'
        
        if online:
            return f'[{text}]({github_url}/blob/main/{full_path})'
        else:
            return f'[{text}]({full_path})'
    
    return re.sub(pattern, replace_link, content)


def build_references_section(excluded_refs: list[tuple[str, str, str]], github_url: str, online: bool) -> str:
    """Build a section listing excluded content with references."""
    if not excluded_refs:
        return ''
    
    lines = [
        '\n---\n',
        '## Additional Documentation\n',
        'The following documentation is not included in this prompt but available for reference:\n',
    ]
    
    # Group by category
    by_category: dict[str, list[tuple[str, str]]] = {}
    for category, path, summary in excluded_refs:
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((path, summary))
    
    for category, items in by_category.items():
        lines.append(f'\n### {category}\n')
        for path, summary in items:
            if online:
                ref = f'{github_url}/blob/main/{path}'
            else:
                ref = path
            
            filename = path.split('/')[-1]
            if summary:
                lines.append(f'- **{filename}** (`{ref}`): {summary}')
            else:
                lines.append(f'- **{filename}** (`{ref}`)')
    
    lines.append('\n')
    return '\n'.join(lines)


def build_master_prompt(files: list[Path], excluded_refs: list[tuple[str, str, str]], 
                        github_url: str, online: bool, root: Path) -> str:
    """Build the master prompt from all files."""
    sections = []
    
    # Header
    sections.append('# NiceGUI Master Prompt\n')
    sections.append('Complete reference for AI agents building NiceGUI applications.\n')
    if online:
        sections.append(f'Source: {github_url}\n')
    sections.append('---\n')
    
    seen_content = set()  # Track content hashes to avoid duplicates
    
    for file_path in files:
        content = file_path.read_text().strip()
        
        # Skip if we've seen very similar content
        content_hash = hash(content[:500])  # Hash first 500 chars
        if content_hash in seen_content:
            continue
        seen_content.add(content_hash)
        
        # Convert relative paths in content to absolute
        content = convert_relative_paths(content, file_path, github_url, online, root)
        
        # Add section separator with source reference
        relative_path = file_path.relative_to(root)
        if online:
            source_ref = f'{github_url}/blob/main/{relative_path}'
        else:
            source_ref = str(relative_path)
        sections.append(f'\n<!-- Source: {source_ref} -->\n')
        sections.append(content)
        sections.append('\n')
    
    # Add references to excluded content
    refs_section = build_references_section(excluded_refs, github_url, online)
    if refs_section:
        sections.append(refs_section)
    
    return '\n'.join(sections)


def count_tokens(text: str, model: str = 'gpt-4') -> int:
    """Count tokens using tiktoken."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding('cl100k_base')
    return len(encoding.encode(text))


def build_variant(variant: PromptVariant, github_url: str, output_dir: Path, root: Path, online: bool) -> dict:
    """Build a single prompt variant and return stats."""
    files, excluded_refs = collect_files_and_refs(variant)
    master_prompt = build_master_prompt(files, excluded_refs, github_url, online, root)
    
    # Determine filename based on online/offline
    mode_suffix = '' if online else '_offline'
    output_file = output_dir / f'nice_prompt{variant.suffix}{mode_suffix}.md'
    output_file.write_text(master_prompt)
    
    token_count = count_tokens(master_prompt)
    
    return {
        'name': variant.name,
        'mode': 'online' if online else 'offline',
        'file': output_file,
        'files_count': len(files),
        'refs_count': len(excluded_refs),
        'chars': len(master_prompt),
        'lines': master_prompt.count('\n'),
        'tokens': token_count,
        'description': variant.description,
    }


def main():
    parser = argparse.ArgumentParser(description='Build master prompt variants from documentation.')
    parser.add_argument(
        '--github-url',
        default=DEFAULT_GITHUB_URL,
        help=f'GitHub repository URL for source links (default: {DEFAULT_GITHUB_URL})'
    )
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent
    output_dir = root / 'output'
    output_dir.mkdir(exist_ok=True)
    
    print(f'GitHub URL: {args.github_url}')
    print('Building prompt variants (online + offline)...\n')
    
    results = []
    for variant in VARIANTS:
        print(f'[{variant.name}] {variant.description}')
        
        # Build online version
        stats_online = build_variant(variant, args.github_url, output_dir, root, online=True)
        results.append(stats_online)
        print(f'  -> {stats_online["file"].name}: {stats_online["files_count"]} files, {stats_online["refs_count"]} refs, {stats_online["tokens"]:,} tokens')
        
        # Build offline version
        stats_offline = build_variant(variant, args.github_url, output_dir, root, online=False)
        results.append(stats_offline)
        print(f'  -> {stats_offline["file"].name}: {stats_offline["files_count"]} files, {stats_offline["refs_count"]} refs, {stats_offline["tokens"]:,} tokens')
    
    # Summary table
    print('\n' + '=' * 80)
    print('SUMMARY')
    print('=' * 80)
    print(f'{"Variant":<10} {"Mode":<8} {"Files":<6} {"Refs":<6} {"Tokens":<10} {"File"}')
    print('-' * 80)
    
    for stats in results:
        print(f'{stats["name"]:<10} {stats["mode"]:<8} {stats["files_count"]:<6} {stats["refs_count"]:<6} {stats["tokens"]:<10,} {stats["file"].name}')
    
    print('-' * 80)
    print('\nVersions:')
    print('  - online:  References GitHub URLs for excluded docs (for web-connected AI)')
    print('  - offline: References local file paths (for local/IDE-integrated AI)')
    print('\nRecommendations:')
    print('  - compact:  Quick tasks, simple UI generation')
    print('  - optimum:  Most use cases, good balance of context and coverage')
    print('  - extended: Complex apps, custom components, deployment questions')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build a single master prompt file from all documentation.

Concatenates all docs into output/nice_prompt.md and reports token count.
Uses docs/prompt_config.yaml to control file order and exclusions.
"""

import argparse
from fnmatch import fnmatch
from pathlib import Path

import tiktoken
import yaml


DEFAULT_GITHUB_URL = 'https://github.com/Alyxion/nice-prompt'


def load_config() -> dict:
    """Load prompt configuration from YAML."""
    root = Path(__file__).parent.parent
    config_path = root / 'docs' / 'prompt_config.yaml'
    
    if not config_path.exists():
        raise FileNotFoundError(f'Config not found: {config_path}')
    
    with open(config_path) as f:
        return yaml.safe_load(f)


def should_exclude(filename: str, exclude_patterns: list[str]) -> bool:
    """Check if file matches any exclude pattern."""
    for pattern in exclude_patterns:
        if fnmatch(filename, pattern):
            return True
    return False


def collect_files() -> list[Path]:
    """Collect all markdown files in configured order."""
    root = Path(__file__).parent.parent
    docs_dir = root / 'docs'
    config = load_config()
    
    files = []
    exclude_patterns = config.get('exclude', [])
    
    # Main guide first
    main_guide = config.get('main_guide')
    if main_guide:
        files.append(docs_dir / main_guide)
    
    # Mechanics
    mechanics_dir = docs_dir / 'mechanics'
    for filename in config.get('mechanics', []):
        path = mechanics_dir / filename
        if path.exists() and not should_exclude(filename, exclude_patterns):
            files.append(path)
    
    # Events
    events_dir = docs_dir / 'events'
    for filename in config.get('events', []):
        path = events_dir / filename
        if path.exists() and not should_exclude(filename, exclude_patterns):
            files.append(path)
    
    # Classes
    classes_dir = docs_dir / 'classes'
    for filename in config.get('classes', []):
        path = classes_dir / filename
        if path.exists() and not should_exclude(filename, exclude_patterns):
            files.append(path)
    
    return files


def build_master_prompt(files: list[Path], github_url: str) -> str:
    """Build the master prompt from all files."""
    sections = []
    
    # Header
    sections.append('# NiceGUI Master Prompt\n')
    sections.append('Complete reference for AI agents building NiceGUI applications.\n')
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
        
        # Add section separator with GitHub URL
        relative_path = file_path.relative_to(file_path.parent.parent.parent)
        source_url = f'{github_url}/blob/main/{relative_path}'
        sections.append(f'\n<!-- Source: {source_url} -->\n')
        sections.append(content)
        sections.append('\n')
    
    return '\n'.join(sections)


def count_tokens(text: str, model: str = 'gpt-4') -> int:
    """Count tokens using tiktoken."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding('cl100k_base')
    return len(encoding.encode(text))


def main():
    parser = argparse.ArgumentParser(description='Build master prompt from documentation.')
    parser.add_argument(
        '--github-url',
        default=DEFAULT_GITHUB_URL,
        help=f'GitHub repository URL for source links (default: {DEFAULT_GITHUB_URL})'
    )
    args = parser.parse_args()
    
    root = Path(__file__).parent.parent
    output_dir = root / 'output'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'nice_prompt.md'
    
    print(f'GitHub URL: {args.github_url}')
    print('Collecting documentation files...')
    files = collect_files()
    print(f'  Found {len(files)} files')
    
    for f in files:
        print(f'    - {f.relative_to(root)}')
    
    print('\nBuilding master prompt...')
    master_prompt = build_master_prompt(files, args.github_url)
    
    # Write output
    output_file.write_text(master_prompt)
    print(f'\nWritten to: {output_file}')
    
    # Stats
    char_count = len(master_prompt)
    line_count = master_prompt.count('\n')
    token_count = count_tokens(master_prompt)
    
    print(f'\n--- Statistics ---')
    print(f'Characters: {char_count:,}')
    print(f'Lines:      {line_count:,}')
    print(f'Tokens:     {token_count:,} (GPT-4 encoding)')
    
    # Cost estimate (rough, based on GPT-4 input pricing)
    cost_per_1k = 0.03  # $0.03 per 1K tokens for GPT-4
    estimated_cost = (token_count / 1000) * cost_per_1k
    print(f'Est. cost:  ${estimated_cost:.4f} per prompt (GPT-4 input)')


if __name__ == '__main__':
    main()

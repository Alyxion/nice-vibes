#!/usr/bin/env python3
"""Generate PyPI-compatible README with absolute GitHub URLs.

Converts relative paths in README.md to absolute GitHub URLs for PyPI display.
"""

import re
from pathlib import Path

GITHUB_RAW = 'https://raw.githubusercontent.com/Alyxion/nice-vibes/main'
GITHUB_BLOB = 'https://github.com/Alyxion/nice-vibes/blob/main'
GITHUB_TREE = 'https://github.com/Alyxion/nice-vibes/tree/main'


def convert_readme_for_pypi(content: str) -> str:
    """Convert relative URLs to absolute GitHub URLs."""
    
    # Image sources in HTML: src="path" -> src="raw.githubusercontent..."
    def replace_img_src(match):
        path = match.group(1)
        if path.startswith('http'):
            return match.group(0)
        return f'src="{GITHUB_RAW}/{path}"'
    
    content = re.sub(r'src="([^"]+)"', replace_img_src, content)
    
    # Markdown images: ![alt](path) -> ![alt](raw.githubusercontent...)
    def replace_md_img(match):
        alt = match.group(1)
        path = match.group(2)
        if path.startswith('http'):
            return match.group(0)
        return f'![{alt}]({GITHUB_RAW}/{path})'
    
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_md_img, content)
    
    # HTML href for files: href="path" (not starting with http)
    def replace_href(match):
        path = match.group(1)
        if path.startswith('http'):
            return match.group(0)
        if path.endswith('/'):
            return f'href="{GITHUB_TREE}/{path.rstrip("/")}"'
        return f'href="{GITHUB_BLOB}/{path}"'
    
    content = re.sub(r'href="([^"]+)"', replace_href, content)
    
    # Markdown links to local files/folders: [text](path)
    # But not images (already handled) and not external URLs
    def replace_md_link(match):
        text = match.group(1)
        path = match.group(2)
        if path.startswith('http') or path.startswith('#'):
            return match.group(0)
        if path.endswith('/'):
            return f'[{text}]({GITHUB_TREE}/{path.rstrip("/")})'
        return f'[{text}]({GITHUB_BLOB}/{path})'
    
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_md_link, content)
    
    return content


def main():
    root = Path(__file__).parent.parent
    readme_path = root / 'README.md'
    pypi_readme_path = root / 'README_PYPI.md'
    
    content = readme_path.read_text()
    pypi_content = convert_readme_for_pypi(content)
    pypi_readme_path.write_text(pypi_content)
    
    print(f'Generated {pypi_readme_path.name} with absolute GitHub URLs')


if __name__ == '__main__':
    main()

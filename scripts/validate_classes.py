#!/usr/bin/env python3
"""
Validate that all NiceGUI classes referenced in documentation actually exist.
Also validates source file paths and documentation URLs in reference files.

Usage:
    python scripts/validate_classes.py [--check-urls] [--retry-failed]
    
Options:
    --check-urls    Also validate URLs in reference files (slower)
    --retry-failed  Only retry URLs that failed in the last run
"""

import argparse
import inspect
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

import nicegui
from nicegui import ui, app, html, binding, run, background_tasks


# Base URLs
NICEGUI_GITHUB_BASE = "https://github.com/zauberzeug/nicegui/blob/main"
NICEGUI_DOCS_BASE = "https://nicegui.io/documentation"

# File to store failed URLs for retry
FAILED_URLS_FILE = Path(__file__).parent / '.failed_urls.json'


def get_documented_classes(docs_dir: Path) -> dict[str, set[str]]:
    """Extract all ui.*, app.*, html.*, etc. references from markdown files."""
    
    # Pattern matches: ui.label, app.storage.user, html.div, binding.BindableProperty, etc.
    pattern = re.compile(r'`(ui|app|html|binding|run|background_tasks)\.([a-zA-Z_][a-zA-Z0-9_\.]*)`')
    
    results: dict[str, set[str]] = {}
    
    for md_file in docs_dir.rglob('*.md'):
        content = md_file.read_text()
        matches = pattern.findall(content)
        
        if matches:
            rel_path = str(md_file.relative_to(docs_dir))
            results[rel_path] = set()
            for namespace, name in matches:
                full_name = f"{namespace}.{name}"
                results[rel_path].add(full_name)
    
    return results


def check_exists(full_name: str) -> bool:
    """Check if a dotted name exists in NiceGUI."""
    
    # Known valid references that require runtime context
    KNOWN_VALID = {
        'app.storage.browser',
        'app.storage.user', 
        'app.storage.tab',
        'app.storage.client',
        'app.storage.general',
        'app.native',
        'ui.context',
    }
    
    if full_name in KNOWN_VALID:
        return True
    
    parts = full_name.split('.')
    
    # Get the root module
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
        return False
    
    obj = modules[root]
    
    # Navigate through the attribute chain
    for part in parts[1:]:
        try:
            obj = getattr(obj, part)
        except (AttributeError, RuntimeError):
            return False
    
    return True


def extract_links_from_references(docs_dir: Path) -> dict[str, list[tuple[str, str]]]:
    """Extract all source and doc links from reference files."""
    # Pattern matches markdown links: [text](url)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    results: dict[str, list[tuple[str, str]]] = {}
    
    for md_file in docs_dir.glob('*_references.md'):
        content = md_file.read_text()
        matches = link_pattern.findall(content)
        
        rel_path = md_file.name
        results[rel_path] = []
        
        for text, url in matches:
            # Skip relative links and anchors
            if url.startswith('http'):
                results[rel_path].append((text, url))
    
    return results


def check_url(url: str, timeout: int = 15, retries: int = 2) -> tuple[bool, str]:
    """Check if a URL is accessible. Returns (success, error_message)."""
    import time
    
    last_error = ""
    for attempt in range(retries + 1):
        try:
            response = urlopen(url, timeout=timeout)
            return True, ""
        except HTTPError as e:
            return False, f"HTTP {e.code}"
        except URLError as e:
            last_error = str(e.reason)
            if attempt < retries:
                time.sleep(1)  # Wait before retry
        except Exception as e:
            last_error = str(e)
            if attempt < retries:
                time.sleep(1)
    
    return False, last_error


def check_github_file(url: str) -> tuple[bool, str]:
    """Check if a GitHub file URL exists by checking raw content."""
    # Convert blob URL to raw URL for faster checking
    raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    return check_url(raw_url)


def load_failed_urls() -> set[str]:
    """Load previously failed URLs from file."""
    if FAILED_URLS_FILE.exists():
        try:
            data = json.loads(FAILED_URLS_FILE.read_text())
            return set(data.get('failed_urls', []))
        except (json.JSONDecodeError, KeyError):
            pass
    return set()


def save_failed_urls(urls: set[str]) -> None:
    """Save failed URLs to file for later retry."""
    FAILED_URLS_FILE.write_text(json.dumps({
        'failed_urls': sorted(urls)
    }, indent=2))


def clear_failed_urls() -> None:
    """Clear the failed URLs file."""
    if FAILED_URLS_FILE.exists():
        FAILED_URLS_FILE.unlink()


def validate_urls(docs_dir: Path, retry_only: bool = False) -> tuple[int, int, set[str]]:
    """
    Validate URLs in reference files.
    Returns (valid_count, invalid_count, failed_urls).
    """
    links = extract_links_from_references(docs_dir)
    
    total_links = sum(len(l) for l in links.values())
    print(f"Found {total_links} links in {len(links)} reference files\n")
    
    # Deduplicate URLs
    unique_urls: dict[str, list[tuple[str, str]]] = {}
    for file, file_links in links.items():
        for text, url in file_links:
            if url not in unique_urls:
                unique_urls[url] = []
            unique_urls[url].append((file, text))
    
    # Filter to only retry failed URLs if requested
    if retry_only:
        previous_failed = load_failed_urls()
        if not previous_failed:
            print("No previously failed URLs to retry.\n")
            return len(unique_urls), 0, set()
        
        urls_to_check = {url: sources for url, sources in unique_urls.items() 
                        if url in previous_failed}
        print(f"Retrying {len(urls_to_check)} previously failed URLs (8 threads)...\n")
    else:
        urls_to_check = unique_urls
        print(f"Checking {len(urls_to_check)} unique URLs (8 threads)...\n")
    
    if not urls_to_check:
        return len(unique_urls), 0, set()
    
    def check_single_url(url: str) -> tuple[str, bool, str]:
        """Check a single URL and return (url, success, error)."""
        if 'github.com' in url and '/blob/' in url:
            success, error = check_github_file(url)
        elif 'nicegui.io' in url:
            success, error = check_url(url)
        else:
            return url, True, ""
        return url, success, error
    
    # Check URLs in parallel
    url_results: dict[str, tuple[bool, str]] = {}
    checked = 0
    
    try:
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(check_single_url, url): url for url in urls_to_check}
            
            for future in as_completed(futures):
                checked += 1
                url, success, error = future.result()
                url_results[url] = (success, error)
                
                if checked % 10 == 0:
                    print(f"  Checked {checked}/{len(urls_to_check)} URLs...", end='\r')
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted! Cancelling remaining URL checks...")
        executor.shutdown(wait=False, cancel_futures=True)
        # Mark unchecked URLs as failed so they can be retried
        for url in urls_to_check:
            if url not in url_results:
                url_results[url] = (False, "Interrupted")
    
    print(f"  Checked {len(url_results)}/{len(urls_to_check)} URLs...    ")
    print()
    
    # Collect results
    invalid_links = []
    failed_urls = set()
    
    for url, sources in urls_to_check.items():
        success, error = url_results.get(url, (True, ""))
        if not success:
            failed_urls.add(url)
            for file, text in sources:
                invalid_links.append((file, text, url, error))
    
    if invalid_links:
        print("❌ INVALID LINKS:")
        for file, text, url, error in invalid_links:
            print(f"  {file}: [{text}]")
            print(f"    URL: {url}")
            print(f"    Error: {error}")
        print()
    
    valid_count = len(urls_to_check) - len(failed_urls)
    invalid_count = len(failed_urls)
    
    print(f"✅ Valid links: {valid_count}")
    print(f"❌ Invalid links: {invalid_count}")
    
    return valid_count, invalid_count, failed_urls


def main():
    parser = argparse.ArgumentParser(
        description='Validate NiceGUI class references in documentation.'
    )
    parser.add_argument(
        '--check-urls', 
        action='store_true',
        help='Also validate URLs in reference files (slower)'
    )
    parser.add_argument(
        '--retry-failed',
        action='store_true', 
        help='Only retry URLs that failed in the last run'
    )
    args = parser.parse_args()
    
    docs_dir = Path(__file__).parent.parent / 'docs' / 'classes'
    
    if not docs_dir.exists():
        print(f"Error: {docs_dir} does not exist")
        sys.exit(1)
    
    # Phase 1: Validate class references
    print("="*50)
    print("Validating class references...")
    print("="*50 + "\n")
    
    print(f"Scanning {docs_dir}...\n")
    
    documented = get_documented_classes(docs_dir)
    
    all_classes: set[str] = set()
    for classes in documented.values():
        all_classes.update(classes)
    
    # Check each class
    valid = []
    invalid = []
    
    for class_name in sorted(all_classes):
        if check_exists(class_name):
            valid.append(class_name)
        else:
            invalid.append(class_name)
    
    # Report results
    print(f"Found {len(all_classes)} unique class references\n")
    
    if invalid:
        print("❌ INVALID REFERENCES:")
        for name in invalid:
            files = [f for f, classes in documented.items() if name in classes]
            print(f"  {name}")
            for f in files:
                print(f"    └─ {f}")
        print()
    
    print(f"✅ Valid: {len(valid)}")
    print(f"❌ Invalid: {len(invalid)}")
    
    # Phase 2: Validate URLs (optional)
    url_errors = False
    
    if args.check_urls or args.retry_failed:
        print("\n" + "="*50)
        print("Validating reference file links...")
        print("="*50 + "\n")
        
        valid_urls, invalid_urls, failed_urls = validate_urls(
            docs_dir, 
            retry_only=args.retry_failed
        )
        
        # Save failed URLs for later retry
        if failed_urls:
            save_failed_urls(failed_urls)
            print(f"\n💾 Saved {len(failed_urls)} failed URLs to {FAILED_URLS_FILE.name}")
            print("   Run with --retry-failed to retry only these URLs")
            url_errors = True
        else:
            # Clear failed URLs file if all passed
            clear_failed_urls()
    else:
        print("\n💡 Tip: Run with --check-urls to also validate URLs in reference files")
    
    # Final result
    has_errors = bool(invalid) or url_errors
    
    if has_errors:
        print("\n❌ Validation failed!")
        sys.exit(1)
    
    print("\n✅ All validations passed!")
    return 0


if __name__ in {'__main__', '__mp_main__'}:
    sys.exit(main())

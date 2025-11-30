#!/usr/bin/env python3
"""
Build everything: screenshots, gallery, GIFs, and master prompts.

Usage:
    poetry run python scripts/build_all.py
    poetry run python scripts/build_all.py --skip-screenshots  # Skip slow screenshot capture
"""
import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run_script(name: str, *args: str) -> bool:
    """Run a script and return success status."""
    script = SCRIPTS_DIR / name
    cmd = [sys.executable, str(script), *args]
    print(f'\n{"="*60}')
    print(f'Running: {name}')
    print('='*60)
    result = subprocess.run(cmd, cwd=SCRIPTS_DIR.parent)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description='Build all project artifacts')
    parser.add_argument('--skip-screenshots', action='store_true',
                        help='Skip screenshot capture (faster)')
    parser.add_argument('--skip-validation', action='store_true',
                        help='Skip class validation')
    args = parser.parse_args()
    
    success = True
    
    # 1. Capture screenshots (slow - can skip)
    if not args.skip_screenshots:
        success = run_script('capture_screenshots.py') and success
    else:
        print('\n[Skipping screenshots]')
    
    # 2. Build samples gallery and showcase GIF
    success = run_script('build_samples_gallery.py') and success
    
    # 3. Generate class references
    success = run_script('generate_class_references.py') and success
    
    # 4. Validate classes
    if not args.skip_validation:
        success = run_script('validate_classes.py') and success
    else:
        print('\n[Skipping validation]')
    
    # 5. Build master prompts
    success = run_script('build_master_prompt.py') and success
    
    # 6. Build PyPI readme
    success = run_script('build_pypi_readme.py') and success
    
    # Summary
    print(f'\n{"="*60}')
    if success:
        print('✓ All builds completed successfully')
    else:
        print('✗ Some builds failed')
    print('='*60)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())

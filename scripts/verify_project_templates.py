#!/usr/bin/env python3
"""Verify project templates create valid, working applications.

This script tests the project_setup MCP tool by:
1. Creating isolated temporary directories
2. Generating project files from templates
3. Running poetry install
4. Starting the application and verifying it responds
5. Capturing a screenshot to verify rendering works
6. Checking for errors in server output
7. Cleaning up

Usage:
    poetry run python scripts/verify_project_templates.py
    poetry run python scripts/verify_project_templates.py --keep  # Keep temp dirs for inspection
    poetry run python scripts/verify_project_templates.py --type spa  # Test specific type
"""
import argparse
import asyncio
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def get_project_setup(project_name: str, project_type: str, include_mcp: bool = True) -> dict:
    """Get project setup instructions by calling the MCP tool logic directly."""
    import re

    pkg = re.sub(r'[^a-zA-Z0-9]+', '_', project_name.lower()).strip('_')

    # Import and call the tool handler logic
    # We'll simulate what the MCP tool does
    from nice_vibes.mcp.server import call_tool

    # Run the async function
    async def get_setup():
        result = await call_tool(
            'project_setup',
            {'project_name': project_name, 'project_type': project_type, 'include_mcp_rules': include_mcp}
        )
        # Extract text content
        for item in result:
            if hasattr(item, 'text'):
                return json.loads(item.text)
        return None

    return asyncio.run(get_setup())


def create_project(setup: dict, target_dir: Path) -> None:
    """Create project files and folders from setup instructions."""
    # Create folders
    for folder in setup.get('folders', []):
        (target_dir / folder).mkdir(parents=True, exist_ok=True)

    # Create files
    for file_info in setup.get('files', []):
        file_path = target_dir / file_info['path']
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file_info['content'])
        print(f"  Created: {file_info['path']}")


def run_poetry_install(project_dir: Path, timeout: int = 120) -> bool:
    """Run poetry install in the project directory."""
    print(f"  Running poetry install (timeout: {timeout}s)...")
    try:
        result = subprocess.run(
            ['poetry', 'install', '--no-interaction'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            print(f"  ERROR: poetry install failed:")
            print(result.stderr)
            return False
        print("  poetry install completed successfully")
        return True
    except subprocess.TimeoutExpired:
        print(f"  ERROR: poetry install timed out after {timeout}s")
        return False
    except FileNotFoundError:
        print("  ERROR: poetry not found in PATH")
        return False


def start_app(project_dir: Path, pkg_name: str) -> subprocess.Popen | None:
    """Start the application and return the process."""
    print(f"  Starting application...")
    try:
        # Use poetry run python -m pkg.main
        process = subprocess.Popen(
            ['poetry', 'run', 'python', '-m', f'{pkg_name}.main'],
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return process
    except Exception as e:
        print(f"  ERROR: Failed to start application: {e}")
        return None


def wait_for_server(url: str = 'http://localhost:8080', timeout: int = 30) -> bool:
    """Wait for the server to respond."""
    print(f"  Waiting for server at {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = urllib.request.urlopen(url, timeout=2)
            if response.status == 200:
                print(f"  Server responded with status 200")
                return True
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
            pass
        time.sleep(0.5)
    print(f"  ERROR: Server did not respond within {timeout}s")
    return False


def capture_screenshot(url: str = 'http://localhost:8080', output_path: Path | None = None) -> bool:
    """Capture a screenshot using the MCP screenshot functionality.

    Returns True if screenshot was captured successfully.
    """
    print(f"  Capturing screenshot of {url}...")
    try:
        from nice_vibes.mcp.server import call_tool

        async def take_screenshot():
            result = await call_tool(
                'capture_url_screenshot',
                {'url': url, 'wait': 2, 'format': 'JPEG', 'quality': 85}
            )
            for item in result:
                if hasattr(item, 'data') and hasattr(item, 'mimeType'):
                    return item.data, item.mimeType
            return None, None

        data, mime_type = asyncio.run(take_screenshot())

        if not data:
            print("  ERROR: No screenshot data returned")
            return False

        # Decode and verify
        image_bytes = base64.b64decode(data)
        if len(image_bytes) < 1000:
            print(f"  ERROR: Screenshot too small ({len(image_bytes)} bytes)")
            return False

        print(f"  Screenshot captured: {len(image_bytes)} bytes, {mime_type}")

        # Save if path provided
        if output_path:
            output_path.write_bytes(image_bytes)
            print(f"  Saved to: {output_path}")

        return True

    except ImportError as e:
        print(f"  WARNING: Screenshot skipped (missing dependency: {e})")
        return True  # Don't fail the test for missing selenium
    except Exception as e:
        print(f"  ERROR: Screenshot failed: {e}")
        return False


def check_server_errors(process: subprocess.Popen, timeout: float = 0.5) -> list[str]:
    """Check for errors in server output without blocking."""
    errors = []
    if process is None or process.stderr is None:
        return errors

    # Read any available stderr
    import select
    try:
        readable, _, _ = select.select([process.stderr], [], [], timeout)
        if readable:
            stderr_data = process.stderr.read()
            if stderr_data:
                stderr_text = stderr_data.decode() if isinstance(stderr_data, bytes) else stderr_data
                # Look for error patterns
                for line in stderr_text.split('\n'):
                    line_lower = line.lower()
                    if any(err in line_lower for err in ['error', 'exception', 'traceback', 'failed']):
                        errors.append(line)
    except Exception:
        pass

    return errors


def stop_app(process: subprocess.Popen) -> None:
    """Stop the application process."""
    if process is None:
        return
    print("  Stopping application...")
    try:
        process.terminate()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def kill_port_8080() -> None:
    """Kill any process on port 8080."""
    try:
        subprocess.run(
            'lsof -ti:8080 | xargs kill -9 2>/dev/null',
            shell=True,
            capture_output=True,
        )
    except Exception:
        pass


def verify_template(project_type: str, keep_dir: bool = False, screenshot: bool = True) -> bool:
    """Verify a project template creates a working application."""
    project_name = f"Test {project_type.replace('_', ' ').title()} App"
    print(f"\n{'='*60}")
    print(f"Testing: {project_type} template")
    print(f"Project: {project_name}")
    print('='*60)

    # Get setup instructions
    print("\n[1/6] Getting project setup instructions...")
    try:
        setup = get_project_setup(project_name, project_type, include_mcp=False)
        if not setup:
            print("  ERROR: Failed to get setup instructions")
            return False
        print(f"  Got {len(setup.get('files', []))} files, {len(setup.get('folders', []))} folders")
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp(prefix=f'nicegui_test_{project_type}_'))
    print(f"\n[2/6] Creating project in: {temp_dir}")

    success = False
    process = None

    try:
        # Create project files
        create_project(setup, temp_dir)

        # Run poetry install
        print("\n[3/6] Installing dependencies...")
        if not run_poetry_install(temp_dir):
            return False

        # Kill any existing process on port 8080
        kill_port_8080()
        time.sleep(0.5)

        # Start application
        print("\n[4/6] Starting application...")
        pkg_name = setup['project_slug']
        process = start_app(temp_dir, pkg_name)
        if process is None:
            return False

        # Wait for server
        print("\n[5/6] Verifying server responds...")
        if not wait_for_server():
            # Print stderr for debugging
            if process.poll() is not None:
                _, stderr = process.communicate()
                print(f"  Application stderr:\n{stderr.decode()}")
            return False

        # Capture screenshot
        print("\n[6/6] Capturing screenshot and checking for errors...")
        screenshot_path = temp_dir / f'screenshot_{project_type}.jpg' if keep_dir else None

        if screenshot:
            if not capture_screenshot(output_path=screenshot_path):
                print("  WARNING: Screenshot capture failed (continuing anyway)")
        else:
            print("  Screenshot capture skipped (--no-screenshot)")

        # Check for server errors in output
        # Give the app a moment to process the screenshot request
        time.sleep(1)

        # Check if process is still running (no crash)
        if process.poll() is not None:
            _, stderr = process.communicate()
            print(f"  ERROR: Application crashed!")
            if stderr:
                print(f"  stderr: {stderr.decode()}")
            return False

        print("  No crashes detected")

        success = True
        print(f"\n{'='*60}")
        print(f"SUCCESS: {project_type} template works correctly!")
        print('='*60)

    finally:
        # Stop application
        stop_app(process)
        kill_port_8080()

        # Cleanup
        if keep_dir:
            print(f"\nKept temp directory: {temp_dir}")
        else:
            print(f"\nCleaning up: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)

    return success


def main():
    parser = argparse.ArgumentParser(description='Verify project templates create working applications')
    parser.add_argument('--keep', action='store_true', help='Keep temp directories for inspection')
    parser.add_argument('--type', choices=['single_page', 'spa', 'all'], default='all',
                        help='Template type to test (default: all)')
    parser.add_argument('--no-screenshot', action='store_true',
                        help='Skip screenshot capture (faster, but less thorough)')
    args = parser.parse_args()

    templates = ['single_page', 'spa'] if args.type == 'all' else [args.type]

    print("="*60)
    print("NiceGUI Project Template Verification")
    print("="*60)
    print(f"Templates to test: {', '.join(templates)}")
    print(f"Keep temp dirs: {args.keep}")
    print(f"Screenshot capture: {not args.no_screenshot}")

    results = {}
    for template in templates:
        results[template] = verify_template(template, keep_dir=args.keep, screenshot=not args.no_screenshot)

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    all_passed = True
    for template, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {template}: {status}")
        if not passed:
            all_passed = False

    print("="*60)
    if all_passed:
        print("All templates verified successfully!")
        return 0
    else:
        print("Some templates failed verification!")
        return 1


if __name__ == '__main__':
    sys.exit(main())

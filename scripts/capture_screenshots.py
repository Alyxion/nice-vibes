#!/usr/bin/env python3
"""
Capture screenshots of sample applications for README documentation.

Usage:
    poetry run python scripts/capture_screenshots.py [sample_name]
    
Examples:
    poetry run python scripts/capture_screenshots.py                    # All samples
    poetry run python scripts/capture_screenshots.py multi_dashboard    # Single sample
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image


# Configuration
SAMPLES_DIR = Path(__file__).parent.parent / 'samples'
SCREENSHOT_WIDTH = 1480  # Extra width to avoid horizontal scrollbars
SCREENSHOT_HEIGHT = 1100  # 4:3 aspect ratio
OUTPUT_WIDTH = 800  # README-friendly size
WAIT_SECONDS = 3
MIN_WAIT_SECONDS = 2
QUALITY = 85  # JPEG quality
PORT = 8080


def get_samples() -> list[Path]:
    """Get all sample directories with main.py."""
    samples = []
    for item in SAMPLES_DIR.iterdir():
        if item.is_dir() and (item / 'main.py').exists():
            samples.append(item)
    return sorted(samples)


def kill_port(port: int) -> None:
    """Kill any process using the specified port."""
    try:
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True,
        )
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)
            time.sleep(1)
    except Exception:
        pass


def start_server(sample_dir: Path) -> subprocess.Popen:
    """Start the sample application server."""
    process = subprocess.Popen(
        [sys.executable, 'main.py'],
        cwd=sample_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wait for server to start
    time.sleep(2)
    return process


def capture_screenshot(url: str, output_path: Path, wait_seconds: int, output_width: int) -> None:
    """Capture a screenshot using Selenium."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--window-size={SCREENSHOT_WIDTH},{SCREENSHOT_HEIGHT}')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(wait_seconds)
        
        # Capture as PNG first (lossless)
        png_path = output_path.with_suffix('.png')
        driver.save_screenshot(str(png_path))
        
        # Convert to resized JPEG
        with Image.open(png_path) as img:
            # Calculate new height maintaining aspect ratio
            ratio = output_width / img.width
            new_height = int(img.height * ratio)
            
            # Resize with high-quality resampling
            resized = img.resize((output_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB (JPEG doesn't support alpha)
            if resized.mode in ('RGBA', 'P'):
                resized = resized.convert('RGB')
            
            # Save as JPEG
            resized.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
        
        # Remove temporary PNG
        png_path.unlink()
        
        print(f'  Saved: {output_path}')
        
    finally:
        driver.quit()


def capture_sample(sample_dir: Path, wait_seconds: int, output_width: int) -> bool:
    """Capture screenshot for a single sample."""
    sample_name = sample_dir.name
    output_path = sample_dir / 'screenshot.jpg'
    
    print(f'Capturing {sample_name}...')
    
    # Start server
    process = start_server(sample_dir)
    
    try:
        # Check if server started
        if process.poll() is not None:
            print(f'  Error: Server failed to start')
            return False
        
        # Capture screenshot
        capture_screenshot('http://localhost:8080', output_path, wait_seconds, output_width)
        return True
        
    except Exception as e:
        print(f'  Error: {e}')
        return False
        
    finally:
        # Stop server
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def main():
    parser = argparse.ArgumentParser(description='Capture screenshots of sample applications.')
    parser.add_argument(
        'sample',
        nargs='?',
        help='Sample name to capture (default: all samples)'
    )
    parser.add_argument(
        '--wait',
        type=int,
        default=WAIT_SECONDS,
        help=f'Seconds to wait after page load (default: {WAIT_SECONDS})'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=OUTPUT_WIDTH,
        help=f'Output image width (default: {OUTPUT_WIDTH})'
    )
    args = parser.parse_args()
    
    wait_seconds = max(args.wait, MIN_WAIT_SECONDS)
    output_width = args.width
    
    if args.sample:
        # Single sample
        sample_dir = SAMPLES_DIR / args.sample
        if not sample_dir.exists():
            print(f'Error: Sample "{args.sample}" not found')
            sys.exit(1)
        samples = [sample_dir]
    else:
        # All samples
        samples = get_samples()
    
    # Kill any existing process on port 8080
    kill_port(PORT)
    
    print(f'Capturing {len(samples)} sample(s) at {SCREENSHOT_WIDTH}x{SCREENSHOT_HEIGHT}')
    print(f'Output: {output_width}px wide JPEG, {wait_seconds}s wait\n')
    
    success = 0
    for sample in samples:
        if capture_sample(sample, wait_seconds, output_width):
            success += 1
        print()
    
    print(f'Done: {success}/{len(samples)} screenshots captured')


if __name__ == '__main__':
    main()

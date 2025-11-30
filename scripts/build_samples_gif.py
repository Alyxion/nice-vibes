#!/usr/bin/env python3
"""
Build an animated GIF showcasing all sample screenshots.

Samples with an `animated` marker in their README will be recorded live.
Order is determined by docs/prompt_config.yaml samples section.

Usage:
    poetry run python scripts/build_samples_gif.py
"""
import subprocess
import sys
import time
from pathlib import Path

import yaml
from PIL import Image

SCRIPTS_DIR = Path(__file__).parent
SAMPLES_DIR = SCRIPTS_DIR.parent / 'samples'
CONFIG_FILE = SCRIPTS_DIR.parent / 'docs' / 'prompt_config.yaml'
OUTPUT_FILE = SAMPLES_DIR / 'showcase.gif'

# GIF settings
STATIC_DURATION_MS = 2500  # 2.5 seconds for static screenshots
ANIMATED_DURATION_S = 3  # 3 seconds recording for animated samples
ANIMATED_FPS = 20  # Frames per second for animated samples
MAX_WIDTH = 600  # Compress to this width
GALLERY_WIDTH = 280  # Width for gallery thumbnails
MAX_COLORS = 128  # Color palette size
PORT = 8080


def get_sample_order() -> list[str]:
    """Get sample order from config file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f)
        samples = config.get('samples', [])
        return [s['name'] for s in samples if 'name' in s]
    return []


def is_animated(sample_dir: Path) -> bool:
    """Check if sample should be recorded as animation."""
    readme = sample_dir / 'README.md'
    if readme.exists():
        content = readme.read_text().lower()
        # Look for <!-- animated --> marker in README
        return '<!-- animated -->' in content
    return False


def kill_port(port: int) -> None:
    """Kill any process on the given port."""
    try:
        result = subprocess.run(['lsof', '-ti', f':{port}'], capture_output=True, text=True)
        if result.stdout.strip():
            for pid in result.stdout.strip().split('\n'):
                subprocess.run(['kill', '-9', pid], capture_output=True)
            time.sleep(0.5)
    except Exception:
        pass


def capture_animated_frames(sample_dir: Path) -> list[Image.Image]:
    """Capture frames from a running sample for animation."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    frames = []
    process = None
    
    try:
        # Kill any existing process on port
        kill_port(PORT)
        
        # Start the sample server
        process = subprocess.Popen(
            [sys.executable, 'main.py'],
            cwd=sample_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(2)  # Wait for server to start
        
        # Setup headless browser
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1480,1100')
        
        driver = webdriver.Chrome(options=options)
        driver.get(f'http://localhost:{PORT}')
        time.sleep(1)  # Initial load
        
        # Capture frames
        frame_count = ANIMATED_DURATION_S * ANIMATED_FPS
        frame_interval = 1.0 / ANIMATED_FPS
        
        for i in range(frame_count):
            # Capture screenshot
            png_data = driver.get_screenshot_as_png()
            img = Image.open(__import__('io').BytesIO(png_data))
            
            # Resize
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
            
            frames.append(img)
            time.sleep(frame_interval)
        
        driver.quit()
        print(f'  Captured {len(frames)} frames')
        
    except Exception as e:
        print(f'  Error capturing animation: {e}')
    finally:
        if process:
            process.terminate()
            process.wait()
        kill_port(PORT)
    
    return frames


def load_static_frame(screenshot_path: Path, width: int = MAX_WIDTH) -> Image.Image:
    """Load and resize a static screenshot."""
    img = Image.open(screenshot_path)
    ratio = width / img.width
    new_height = int(img.height * ratio)
    return img.resize((width, new_height), Image.Resampling.LANCZOS)


def save_sample_gif(sample_dir: Path, frames: list[Image.Image]) -> None:
    """Save an animated GIF for a single sample (for gallery use)."""
    if not frames:
        return
    
    output_path = sample_dir / 'animated.gif'
    
    # Resize frames to gallery width
    gallery_frames = []
    for img in frames:
        ratio = GALLERY_WIDTH / img.width
        new_height = int(img.height * ratio)
        resized = img.resize((GALLERY_WIDTH, new_height), Image.Resampling.LANCZOS)
        gallery_frames.append(resized.convert('P', palette=Image.ADAPTIVE, colors=MAX_COLORS))
    
    gallery_frames[0].save(
        output_path,
        save_all=True,
        append_images=gallery_frames[1:],
        duration=int(1000 / ANIMATED_FPS),
        loop=0,
        optimize=True,
    )
    
    size_kb = output_path.stat().st_size / 1024
    print(f'  Saved gallery GIF: {output_path.name} ({size_kb:.0f} KB)')


def build_gif() -> None:
    """Build animated GIF from sample screenshots."""
    print('Building samples showcase GIF...')
    
    all_frames = []
    all_durations = []
    
    # Get samples in order from config (others follow alphabetically)
    sample_order = get_sample_order()
    sample_dirs = [d for d in SAMPLES_DIR.iterdir() if d.is_dir()]
    def sort_key(d):
        try:
            return sample_order.index(d.name)
        except ValueError:
            return len(sample_order) + ord(d.name[0])
    sample_dirs.sort(key=sort_key)
    
    for sample_dir in sample_dirs:
        if not sample_dir.is_dir():
            continue
        
        screenshot = sample_dir / 'screenshot.jpg'
        main_py = sample_dir / 'main.py'
        
        if not screenshot.exists() or not main_py.exists():
            continue
        
        name = sample_dir.name
        
        if is_animated(sample_dir):
            print(f'  Recording: {name} (animated)...')
            frames = capture_animated_frames(sample_dir)
            if frames:
                # Save individual gallery GIF
                save_sample_gif(sample_dir, frames)
                # Add to showcase
                all_frames.extend(frames)
                all_durations.extend([int(1000 / ANIMATED_FPS)] * len(frames))
            else:
                # Fallback to static
                all_frames.append(load_static_frame(screenshot))
                all_durations.append(STATIC_DURATION_MS)
        else:
            print(f'  Adding: {name} (static)')
            all_frames.append(load_static_frame(screenshot))
            all_durations.append(STATIC_DURATION_MS)
    
    if not all_frames:
        print('  No frames to save')
        return
    
    # Convert all frames to palette mode
    palette_frames = []
    for img in all_frames:
        palette_frames.append(img.convert('P', palette=Image.ADAPTIVE, colors=MAX_COLORS))
    
    # Save as animated GIF
    palette_frames[0].save(
        OUTPUT_FILE,
        save_all=True,
        append_images=palette_frames[1:],
        duration=all_durations,
        loop=0,
        optimize=True,
    )
    
    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f'  Saved: {OUTPUT_FILE} ({size_kb:.0f} KB, {len(all_frames)} frames)')


if __name__ == '__main__':
    build_gif()

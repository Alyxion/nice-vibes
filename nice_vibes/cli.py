"""Command-line interface for nice-vibes.

Usage:
    nice-vibes                   # Interactive sample selection
    nice-vibes list              # List available samples
    nice-vibes run <sample>      # Run a sample application
    nice-vibes copy <sample>     # Copy sample source to current directory
    nice-vibes copy <sample> -o <dir>  # Copy to specific directory
    nice-vibes mcp-config        # Print MCP server configuration
"""

import argparse
import json
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

import yaml

# Check if we have interactive terminal support
try:
    import curses
    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False

# Paths - resolve to absolute paths to work regardless of CWD
PACKAGE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = PACKAGE_DIR / 'samples'
CONFIG_FILE = PACKAGE_DIR / 'docs' / 'prompt_config.yaml'


def load_samples() -> dict[str, str]:
    """Load samples from prompt_config.yaml.
    
    Returns dict mapping sample name to first line of summary.
    """
    if not CONFIG_FILE.exists():
        return {}
    
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f)
    
    samples = {}
    for sample in config.get('samples', []):
        name = sample.get('name', '')
        summary = sample.get('summary', '').strip()
        # Use first line of summary as description
        description = summary.split('\n')[0] if summary else ''
        if name:
            samples[name] = description
    
    return samples


# Load samples at module import
SAMPLES = load_samples()


def list_samples() -> None:
    """Print available samples."""
    print('\nAvailable samples:\n')
    for name, description in SAMPLES.items():
        print(f'  {name:24} {description}')
    print('\nRun with: nice-vibes run <sample_name>')
    print('Example:  nice-vibes run dashboard\n')


def interactive_select() -> tuple[str, str] | None:
    """Show interactive sample selection using curses.
    
    Returns tuple of (action, sample_name) or None if cancelled.
    Action is 'run' or 'copy'.
    """
    if not HAS_CURSES:
        print("Interactive selection not available (curses not installed)")
        list_samples()
        return None
    
    sample_list = list(SAMPLES.items())
    
    def run_selector(stdscr):
        curses.curs_set(0)  # Hide cursor
        curses.use_default_colors()
        
        # Initialize colors
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected
        curses.init_pair(2, curses.COLOR_CYAN, -1)  # Title
        curses.init_pair(3, curses.COLOR_GREEN, -1)  # Hint
        
        selected = 0
        
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            # Title
            title = "Nice Vibes - Select a sample"
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 2, title)
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
            
            stdscr.addstr(2, 2, "↑/↓ navigate  ")
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr("Enter=Run  c=Copy source  ")
            stdscr.attroff(curses.color_pair(3))
            stdscr.addstr("q=Quit")
            stdscr.addstr(3, 2, "─" * min(60, width - 4))
            
            # Sample list
            for idx, (name, description) in enumerate(sample_list):
                y = 5 + idx
                if y >= height - 1:
                    break
                
                if idx == selected:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, 2, f" ▶ {name:22} {description[:width-30]}")
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, 2, f"   {name:22} {description[:width-30]}")
            
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(sample_list) - 1:
                selected += 1
            elif key in (curses.KEY_ENTER, 10, 13):  # Enter = Run
                return ('run', sample_list[selected][0])
            elif key in (ord('c'), ord('C')):  # c = Copy
                return ('copy', sample_list[selected][0])
            elif key in (ord('q'), ord('Q'), 27):  # q or Escape
                return None
    
    try:
        return curses.wrapper(run_selector)
    except Exception:
        # Fallback if curses fails
        list_samples()
        return None


def open_browser_delayed(url: str, delay: float = 2.0) -> None:
    """Open browser after a delay to let the server start."""
    time.sleep(delay)
    webbrowser.open(url)


def run_sample(sample_name: str, extra_args: list[str]) -> int:
    """Run a sample application.
    
    :param sample_name: Name of the sample to run
    :param extra_args: Additional arguments to pass to the sample
    :return: Exit code
    """
    if sample_name not in SAMPLES:
        print(f"Error: Unknown sample '{sample_name}'")
        print(f"Available samples: {', '.join(SAMPLES.keys())}")
        return 1
    
    sample_dir = SAMPLES_DIR / sample_name
    main_file = sample_dir / 'main.py'
    
    if not main_file.exists():
        print(f"Error: Sample main.py not found at {main_file}")
        return 1
    
    print(f"Starting {sample_name}...")
    print(f"Location: {sample_dir}")
    print("Opening browser at http://localhost:8080 ...\n")
    
    # Open browser after delay (in background thread)
    browser_thread = threading.Thread(
        target=open_browser_delayed,
        args=('http://localhost:8080',),
        daemon=True,
    )
    browser_thread.start()
    
    # Run the sample with Python, passing extra args
    try:
        result = subprocess.run(
            [sys.executable, str(main_file)] + extra_args,
            cwd=str(sample_dir),
        )
        return result.returncode
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


def print_mcp_config() -> int:
    """Print MCP server configuration for use with AI tools."""
    # Get the Python executable path
    python_path = sys.executable
    
    config = {
        "mcpServers": {
            "nice-vibes": {
                "command": python_path,
                "args": ["-m", "nice_vibes.mcp"]
            }
        }
    }
    
    print("# NiceVibes MCP Server Configuration")
    print("#")
    print("# Add this to your MCP client config (e.g., Windsurf, Claude Desktop):")
    print("#")
    print(json.dumps(config, indent=2))
    print()
    print("# For Windsurf: Add to ~/.codeium/windsurf/mcp_config.json")
    print("# For Claude Desktop: Add to ~/Library/Application Support/Claude/claude_desktop_config.json")
    
    return 0


def copy_sample(sample_name: str, output_dir: str | None = None) -> int:
    """Copy sample source code to a directory.
    
    :param sample_name: Name of the sample to copy
    :param output_dir: Target directory (default: ./<sample_name>)
    :return: Exit code
    """
    if sample_name not in SAMPLES:
        print(f"Error: Unknown sample '{sample_name}'")
        print(f"Available samples: {', '.join(SAMPLES.keys())}")
        return 1
    
    sample_dir = SAMPLES_DIR / sample_name
    
    if not sample_dir.exists():
        print(f"Error: Sample directory not found at {sample_dir}")
        return 1
    
    # Determine target directory
    if output_dir:
        target = Path(output_dir)
    else:
        target = Path.cwd() / sample_name
    
    if target.exists():
        print(f"Error: Target directory already exists: {target}")
        print("Use -o to specify a different output directory")
        return 1
    
    # Copy the sample directory
    print(f"Copying {sample_name} to {target}...")
    
    # Copy files, excluding __pycache__ and other artifacts
    def ignore_patterns(directory, files):
        return [f for f in files if f in ('__pycache__', '.DS_Store', '*.pyc')]
    
    shutil.copytree(sample_dir, target, ignore=ignore_patterns)
    
    # Count files
    file_count = sum(1 for _ in target.rglob('*') if _.is_file())
    
    print(f"\n✓ Copied {file_count} files to {target}")
    print(f"\nTo run the sample:")
    print(f"  cd {target}")
    print(f"  python main.py")
    
    return 0


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog='nice-vibes',
        description='Nice Vibes - Run NiceGUI sample applications',
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    subparsers.add_parser('list', help='List available samples')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run a sample application')
    run_parser.add_argument('sample', help='Sample name to run')
    run_parser.add_argument(
        'args',
        nargs='*',
        help='Additional arguments to pass to the sample',
    )
    
    # Copy command
    copy_parser = subparsers.add_parser('copy', help='Copy sample source code')
    copy_parser.add_argument('sample', help='Sample name to copy')
    copy_parser.add_argument(
        '-o', '--output',
        help='Output directory (default: ./<sample_name>)',
    )
    
    # MCP config command
    subparsers.add_parser('mcp-config', help='Print MCP server configuration')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_samples()
        return 0
    elif args.command == 'run':
        return run_sample(args.sample, args.args)
    elif args.command == 'copy':
        return copy_sample(args.sample, args.output)
    elif args.command == 'mcp-config':
        return print_mcp_config()
    else:
        # No command - show interactive selector
        result = interactive_select()
        if result:
            action, sample = result
            if action == 'run':
                return run_sample(sample, [])
            elif action == 'copy':
                return copy_sample(sample, None)
        return 0


if __name__ == '__main__':
    sys.exit(main())

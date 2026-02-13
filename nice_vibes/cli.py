"""Command-line interface for nice-vibes.

Usage:
    nice-vibes                   # Interactive samples menu
    nice-vibes samples           # Interactive samples menu
    nice-vibes samples list      # List available samples
    nice-vibes samples run <sample>      # Run a sample application
    nice-vibes samples copy <sample>     # Copy sample source to current directory
    nice-vibes samples copy <sample> -o <dir>  # Copy to specific directory
    nice-vibes list              # Alias: nice-vibes samples list
    nice-vibes run <sample>      # Alias: nice-vibes samples run <sample>
    nice-vibes copy <sample>     # Alias: nice-vibes samples copy <sample>
    nice-vibes mcp-config        # Print MCP server configuration
    nice-vibes mcp-test          # Interactive MCP server test client
    nice-vibes debug <app>       # Run any NiceGUI app with debug bridge injected
"""

import argparse
import json
import os
import select
import shutil
import signal
import socket
import subprocess
import sys
import threading
import tty
import time
import termios
import webbrowser
from pathlib import Path
from collections import deque
from queue import Queue, Empty

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


def is_port_free(port: int, host: str = '127.0.0.1') -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
        return True
    except OSError:
        return False


def kill_port_8080() -> bool:
    """Try to kill any process listening on TCP port 8080.

    Returns True if we found at least one PID to kill.
    """
    try:
        result = subprocess.run(
            ['lsof', '-ti', 'tcp:8080', '-sTCP:LISTEN'],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return False

    pids = [p.strip() for p in result.stdout.splitlines() if p.strip()]
    if not pids:
        return False

    for pid_str in pids:
        try:
            os.kill(int(pid_str), signal.SIGKILL)
        except (ValueError, ProcessLookupError, PermissionError):
            continue

    time.sleep(0.25)
    return True


def list_samples() -> None:
    """Print available samples."""
    print('\nAvailable samples:\n')
    for name, description in SAMPLES.items():
        print(f'  {name:24} {description}')
    print('\nRun with: nice-vibes run <sample_name>')
    print('Example:  nice-vibes run dashboard\n')


def interactive_sample_browser() -> tuple[str, str] | None:
    """Show interactive sample browser using curses.

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
            title = "Nice Vibes - Sample Browser"
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 2, title)
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
            
            stdscr.addstr(2, 2, "↑/↓ navigate  ")
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr("Enter=Run  c=Copy source  ")
            stdscr.attroff(curses.color_pair(3))
            stdscr.addstr("b=Back  q=Quit")
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
            elif key in (ord('b'), ord('B')):  # b = Back
                return ('back', '')
            elif key in (ord('q'), ord('Q'), 27):  # q or Escape
                return None
    
    try:
        return curses.wrapper(run_selector)
    except KeyboardInterrupt:
        return None
    except Exception:
        # Fallback if curses fails
        list_samples()
        return None


def interactive_sample_switcher(*, allow_back: bool) -> None:
    if not HAS_CURSES:
        print("Interactive selection not available (curses not installed)")
        list_samples()
        return

    sample_list = list(SAMPLES.items())

    def run_ui(stdscr):
        curses.curs_set(0)
        curses.use_default_colors()
        stdscr.nodelay(True)
        stdscr.timeout(50)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected
        curses.init_pair(2, curses.COLOR_CYAN, -1)  # Title
        curses.init_pair(3, curses.COLOR_GREEN, -1)  # Hint
        curses.init_pair(4, curses.COLOR_YELLOW, -1)  # Status

        selected = 0
        running_sample: str | None = None
        proc: subprocess.Popen[str] | None = None
        log_lines: deque[str] = deque(maxlen=400)
        log_q: Queue[str] = Queue()
        stop_reader = threading.Event()
        reader_thread: threading.Thread | None = None
        browser_opened = False

        def stop_process() -> None:
            nonlocal proc, running_sample
            if proc is None:
                return

            try:
                os.killpg(proc.pid, signal.SIGINT)
            except ProcessLookupError:
                proc = None
                running_sample = None
                return

            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    pass

            proc = None
            running_sample = None
            # Give uvicorn/FastAPI a brief moment to release port 8080.
            time.sleep(0.25)

        def start_process(sample_name: str) -> None:
            nonlocal proc, running_sample, reader_thread, browser_opened

            if not is_port_free(8080):
                log_lines.append("ERROR: [Errno 48] Address already in use")
                log_lines.append("Hint: press 'k' to kill whatever is using port 8080")
                return

            stop_reader.set()
            if reader_thread is not None:
                reader_thread.join(timeout=0.5)
            stop_reader.clear()

            stop_process()
            log_lines.clear()

            sample_dir = SAMPLES_DIR / sample_name
            main_file = sample_dir / 'main.py'
            if not main_file.exists():
                log_lines.append(f"Error: Sample main.py not found at {main_file}")
                return

            running_sample = sample_name
            log_lines.append(f"Starting {sample_name}...")
            log_lines.append(f"Location: {sample_dir}")
            if os.environ.get('NICE_VIBES_NO_BROWSER', '').lower() in {'1', 'true', 'yes'}:
                log_lines.append("Browser auto-open disabled (NICE_VIBES_NO_BROWSER=1).")
            elif not browser_opened:
                log_lines.append("Opening browser at http://localhost:8080 ...")
                threading.Thread(target=open_browser_delayed, args=('http://localhost:8080',), daemon=True).start()
                browser_opened = True
            else:
                log_lines.append("Browser already opened; reusing existing tab.")

            proc = subprocess.Popen(
                [sys.executable, str(main_file)],
                cwd=str(sample_dir),
                start_new_session=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            def reader() -> None:
                if proc is None or proc.stdout is None:
                    return
                while not stop_reader.is_set():
                    line = proc.stdout.readline()
                    if not line:
                        break
                    log_q.put(line.rstrip('\n'))

            reader_thread = threading.Thread(target=reader, daemon=True)
            reader_thread.start()

        def drain_logs() -> None:
            while True:
                try:
                    line = log_q.get_nowait()
                except Empty:
                    break
                log_lines.append(line)

        def draw() -> None:
            stdscr.erase()
            height, width = stdscr.getmaxyx()

            log_h = max(6, height // 3)
            list_h = max(0, height - log_h - 8)

            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 2, "Nice Vibes")
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            stdscr.addstr(2, 2, "↑/↓ navigate  ")
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr("Enter=Switch  c=Copy  k=Kill 8080  ")
            stdscr.attroff(curses.color_pair(3))
            if allow_back:
                stdscr.addstr("b=Back  ")
            stdscr.addstr("q=Quit")

            status = f"Running: {running_sample}" if running_sample else "Running: (none)"
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(3, 2, status[: max(0, width - 4)])
            stdscr.attroff(curses.color_pair(4))
            stdscr.addstr(4, 2, "─" * max(0, width - 4))

            # Samples list (top)
            stdscr.addstr(6, 2, "Samples")
            for idx, (name, desc) in enumerate(sample_list[: max(0, list_h)]):
                y = 7 + idx
                if y >= height - log_h - 1:
                    break
                label = f"{name:18} {desc}"[: max(0, width - 6)]
                if idx == selected:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, 2, f" ▶ {label}".ljust(max(0, width - 4)))
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, 2, f"   {label}".ljust(max(0, width - 4)))

            # Log (bottom)
            log_top = max(7, height - log_h)
            if log_top < height - 1:
                stdscr.addstr(log_top - 1, 2, "─" * max(0, width - 4))
                stdscr.addstr(log_top, 2, "Log")

                log_area_h = max(0, height - log_top - 2)
                tail = list(log_lines)[-log_area_h:]
                for i, line in enumerate(tail):
                    y = log_top + 1 + i
                    if y >= height - 1:
                        break
                    stdscr.addstr(y, 2, line[: max(0, width - 4)])

            stdscr.refresh()

        try:
            while True:
                drain_logs()

                if proc is not None:
                    rc = proc.poll()
                    if rc is not None:
                        log_lines.append(f"Process exited with code {rc}")
                        stop_process()

                draw()
                key = stdscr.getch()
                if key == -1:
                    continue

                if key == curses.KEY_UP and selected > 0:
                    selected -= 1
                elif key == curses.KEY_DOWN and selected < len(sample_list) - 1:
                    selected += 1
                elif key in (curses.KEY_ENTER, 10, 13):
                    start_process(sample_list[selected][0])
                elif key in (ord('k'), ord('K')):
                    killed = kill_port_8080()
                    if killed:
                        log_lines.append("Killed process(es) on port 8080")
                    else:
                        log_lines.append("No process found on port 8080 (or missing lsof)")
                elif key in (ord('c'), ord('C')):
                    # Copy in foreground (outside curses). We mark a log line and do it.
                    sample_name = sample_list[selected][0]
                    stop_reader.set()
                    if reader_thread is not None:
                        reader_thread.join(timeout=0.2)
                    curses.endwin()
                    copy_sample(sample_name, None)
                    time.sleep(0.3)
                    stdscr.refresh()
                elif allow_back and key in (ord('b'), ord('B')):
                    break
                elif key in (ord('q'), ord('Q'), 27):
                    break
        finally:
            stop_reader.set()
            if reader_thread is not None:
                reader_thread.join(timeout=0.5)
            stop_process()

    try:
        curses.wrapper(run_ui)
    except KeyboardInterrupt:
        return


def interactive_main_menu() -> str | None:
    """Show interactive main menu.

    Returns:
        - 'samples'
        - 'mcp_test'
        - None if cancelled
    """
    if not HAS_CURSES:
        print("Interactive selection not available (curses not installed)")
        print("Try: nice-vibes samples")
        return None

    entries: list[tuple[str, str]] = [
        ('samples', 'Browse sample apps'),
        ('mcp_test', 'Interactive MCP server test client'),
    ]

    def run_selector(stdscr):
        curses.curs_set(0)
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected
        curses.init_pair(2, curses.COLOR_CYAN, -1)  # Title
        curses.init_pair(3, curses.COLOR_GREEN, -1)  # Hint

        selected = 0

        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            title = "Nice Vibes"
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 2, title)
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

            stdscr.addstr(2, 2, "↑/↓ navigate  ")
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr("Enter=Select  ")
            stdscr.attroff(curses.color_pair(3))
            stdscr.addstr("k=Kill 8080  q=Quit")
            stdscr.addstr(3, 2, "─" * min(60, width - 4))

            for idx, (kind, description) in enumerate(entries):
                y = 5 + idx
                if y >= height - 1:
                    break

                label = "Samples" if kind == 'samples' else "MCP Test"
                line = f" ▶ {label:12} {description[:width-18]}" if idx == selected else f"   {label:12} {description[:width-18]}"

                if idx == selected:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, 2, line)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, 2, line)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(entries) - 1:
                selected += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                kind, _ = entries[selected]
                return kind
            elif key in (ord('k'), ord('K')):
                killed = kill_port_8080()
                if killed:
                    return None
            elif key in (ord('q'), ord('Q'), 27):
                return None

    try:
        return curses.wrapper(run_selector)
    except KeyboardInterrupt:
        return None
    except Exception:
        return None


def open_browser_delayed(url: str, delay: float = 2.0) -> None:
    """Open browser after a delay to let the server start."""
    time.sleep(delay)
    webbrowser.open(url)


def run_sample(sample_name: str, extra_args: list[str] | None = None) -> int:
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
    if os.environ.get('NICE_VIBES_NO_BROWSER', '').lower() not in {'1', 'true', 'yes'}:
        print("Opening browser at http://localhost:8080 ...\n")
        
        # Open browser after delay (in background thread)
        browser_thread = threading.Thread(
            target=open_browser_delayed,
            args=('http://localhost:8080',),
            daemon=True,
        )
        browser_thread.start()
    else:
        print("Browser auto-open disabled (NICE_VIBES_NO_BROWSER=1).\n")
    
    print("Press 'b' to stop and go back (Ctrl+C also works).")

    # Run the sample with Python, passing extra args.
    # We don't need stdin for NiceGUI apps, so we keep it detached and manage stop from the CLI.
    proc = subprocess.Popen(
        [sys.executable, str(main_file)] + extra_args,
        cwd=str(sample_dir),
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    old_term_settings = None
    stdin_fd = None
    try:
        if sys.stdin.isatty():
            stdin_fd = sys.stdin.fileno()
            old_term_settings = termios.tcgetattr(stdin_fd)
            tty.setcbreak(stdin_fd)

        while True:
            if proc.stdout is None:
                break

            # Stream subprocess output, but don't block forever.
            line = proc.stdout.readline()
            if line:
                print(line, end='')

            rc = proc.poll()
            if rc is not None:
                return rc

            if stdin_fd is not None:
                r, _, _ = select.select([stdin_fd], [], [], 0.05)
                if r:
                    ch = os.read(stdin_fd, 1)
                    if ch in (b'b', b'B'):
                        raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("\nStopping...")
        try:
            os.killpg(proc.pid, signal.SIGINT)
        except ProcessLookupError:
            return 0

        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            print("Force stopping...")
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                return 0
            proc.wait()

        print("Stopped.")
        return 0
    finally:
        if old_term_settings is not None and stdin_fd is not None:
            termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_term_settings)


def run_mcp_test() -> int:
    """Run the interactive MCP server test client."""
    import asyncio
    from nice_vibes.mcp.test_client import interactive_session

    try:
        asyncio.run(interactive_session())
        return 0
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


def run_debug(target: str, extra_args: list[str] | None = None) -> int:
    """Run any NiceGUI app with debug bridge auto-injected.

    :param target: Module name or file path to run
    :param extra_args: Additional arguments to pass to the app
    :return: Exit code
    """
    import runpy

    # Enable debug mode
    os.environ['DEBUG_MODE'] = '1'

    # Patch ui.page BEFORE importing target
    import nice_vibes.debug.auto  # noqa: F401

    print(f"Running {target} with debug bridge enabled...")
    print("Debug viewer: http://localhost:8089")
    print()

    # Adjust sys.argv
    original_argv = sys.argv.copy()
    sys.argv = [target] + (extra_args or [])

    try:
        if target.endswith('.py'):
            # Run as file
            runpy.run_path(target, run_name='__main__')
        else:
            # Run as module
            runpy.run_module(target, run_name='__main__', alter_sys=True)
        return 0
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        sys.argv = original_argv


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
    try:
        parser = argparse.ArgumentParser(
            prog='nice-vibes',
            description='Nice Vibes - Run NiceGUI sample applications',
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')

        samples_parser = subparsers.add_parser('samples', help='Samples submenu')
        samples_subparsers = samples_parser.add_subparsers(dest='samples_command', help='Samples commands')
        samples_subparsers.add_parser('list', help='List available samples')

        samples_run_parser = samples_subparsers.add_parser('run', help='Run a sample application')
        samples_run_parser.add_argument('sample', help='Sample name to run')
        samples_run_parser.add_argument(
            'args',
            nargs='*',
            help='Additional arguments to pass to the sample',
        )

        samples_copy_parser = samples_subparsers.add_parser('copy', help='Copy sample source code')
        samples_copy_parser.add_argument('sample', help='Sample name to copy')
        samples_copy_parser.add_argument(
            '-o', '--output',
            help='Output directory (default: ./<sample_name>)',
        )

        # Backward-compatible aliases
        subparsers.add_parser('list', help='Alias: samples list')
        run_parser = subparsers.add_parser('run', help='Alias: samples run')
        run_parser.add_argument('sample', help='Sample name to run')
        run_parser.add_argument('args', nargs='*', help='Additional arguments to pass to the sample')

        copy_parser = subparsers.add_parser('copy', help='Alias: samples copy')
        copy_parser.add_argument('sample', help='Sample name to copy')
        copy_parser.add_argument('-o', '--output', help='Output directory (default: ./<sample_name>)')

        # MCP config command
        subparsers.add_parser('mcp-config', help='Print MCP server configuration')

        # MCP test command (still available at top-level)
        subparsers.add_parser('mcp-test', help='Interactive MCP server test client')

        # Utility command
        subparsers.add_parser('kill-8080', help='Kill any process listening on TCP port 8080')

        # Debug command
        debug_parser = subparsers.add_parser('debug', help='Run any NiceGUI app with debug bridge injected')
        debug_parser.add_argument('target', help='Module or file to run (e.g., myapp.main or path/to/main.py)')
        debug_parser.add_argument('args', nargs='*', help='Additional arguments to pass to the app')
        
        args = parser.parse_args()
        
        if args.command == 'samples':
            if args.samples_command == 'list':
                list_samples()
                return 0
            elif args.samples_command == 'run':
                return run_sample(args.sample, args.args)
            elif args.samples_command == 'copy':
                return copy_sample(args.sample, args.output)
            else:
                interactive_sample_switcher(allow_back=False)
                return 0
        elif args.command == 'list':
            list_samples()
            return 0
        elif args.command == 'run':
            return run_sample(args.sample, args.args)
        elif args.command == 'copy':
            return copy_sample(args.sample, args.output)
        elif args.command == 'mcp-config':
            return print_mcp_config()
        elif args.command == 'mcp-test':
            return run_mcp_test()
        elif args.command == 'kill-8080':
            killed = kill_port_8080()
            if killed:
                print('Killed process(es) on port 8080')
                return 0
            print('No process found on port 8080 (or missing lsof)')
            return 0
        elif args.command == 'debug':
            return run_debug(args.target, args.args)
        else:
            # No command - show main menu
            while True:
                choice = interactive_main_menu()
                if not choice:
                    return 0

                if choice == 'mcp_test':
                    return run_mcp_test()

                if choice == 'samples':
                    interactive_sample_switcher(allow_back=True)
                    continue

            return 0
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())

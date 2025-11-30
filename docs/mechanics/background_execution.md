# Background Execution in NiceGUI

NiceGUI provides several mechanisms for running code in the background without blocking the UI. This document covers the key patterns and when to use each.

## Overview

| Method | Use Case | Blocks Event Loop | Thread Pool |
|--------|----------|-------------------|-------------|
| `run.io_bound()` | I/O or CPU-intensive sync functions | No | Yes |
| `run.cpu_bound()` | CPU-intensive work (process pool) | No | Process pool |
| `background_tasks.create()` | Fire-and-forget async tasks | No | No |
| `ui.timer()` | Periodic execution | No | No |
| `asyncio.create_task()` | Standard async task | No | No |

## Choosing Between io_bound and cpu_bound

### When to Use `run.io_bound()`

- **C++ Extension Libraries**: Libraries like **OpenCV**, **PIL/Pillow**, **NumPy**, and **pandas** do most of their heavy lifting in C/C++ code that releases the GIL. Using `run.io_bound()` is more efficient because:
  - No process boundary overhead (no pickling/unpickling)
  - Shared memory access (no data copying)
  - Lower latency for frequent calls
  
- **I/O Operations**: File reading, network requests, database queries

- **Example**: Video processing with OpenCV
  ```python
  def process_frame(frame):
      # OpenCV operations release the GIL
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      edges = cv2.Canny(gray, 100, 200)
      return edges
  
  result = await run.io_bound(process_frame, frame)
  ```

### When to Use `run.cpu_bound()`

- **Pure Python Computation**: When the bottleneck is Python code itself (loops, string processing, custom algorithms)
- **Small Data Transfer**: When data passed to/from the process is small (large objects must be pickled, which is slow)
- **Long-running Tasks**: Tasks that run for seconds or longer, where process startup overhead is negligible

- **Example**: Pure Python number crunching
  ```python
  def compute_primes(n):
      # Pure Python loop - holds the GIL
      primes = []
      for num in range(2, n):
          if all(num % p != 0 for p in primes):
              primes.append(num)
      return primes
  
  result = await run.cpu_bound(compute_primes, 100000)
  ```

### Decision Guide

```
Is the heavy work in C/C++ extensions (OpenCV, NumPy, PIL)?
  → Use run.io_bound()

Is it pure Python code AND data is small?
  → Use run.cpu_bound()

Is it I/O (file, network, database)?
  → Use run.io_bound()

Unsure?
  → Start with run.io_bound() (simpler, lower overhead)
```

## run.io_bound

Use `run.io_bound()` to run synchronous blocking functions in a thread pool without blocking the event loop.

### Basic Usage

```python
from nicegui import run

# Blocking function that would freeze the UI
def slow_operation(data: str) -> str:
    time.sleep(2)  # Simulates I/O or CPU work
    return f"Processed: {data}"

# Run in background thread
async def handle_click():
    result = await run.io_bound(slow_operation, "input data")
    ui.notify(result)
```

### Key Points

- **Returns a coroutine**: Must be awaited or wrapped in a task
- **Thread pool**: Uses Python's `ThreadPoolExecutor`
- **Arguments**: Pass function arguments after the function
- **Return value**: Returns whatever the function returns

### Non-blocking Pattern

To start work without waiting for completion:

```python
import asyncio
from nicegui import run

# Start without blocking
task = asyncio.create_task(run.io_bound(slow_function, arg1, arg2))

# Later, check if done
if task.done():
    result = task.result()
```

### With ui.timer for Polling

```python
class Worker:
    def __init__(self):
        self._pending_task = None
        self._timer = ui.timer(0.1, self._check_task)
    
    def start_work(self):
        if self._pending_task is None:
            self._pending_task = asyncio.create_task(
                run.io_bound(self._do_work)
            )
    
    def _check_task(self):
        if self._pending_task and self._pending_task.done():
            try:
                result = self._pending_task.result()
                # Handle result
            finally:
                self._pending_task = None
```

## background_tasks.create

Use `background_tasks.create()` for fire-and-forget async tasks that should run independently.

### Basic Usage

```python
from nicegui import background_tasks

async def long_running_task():
    await asyncio.sleep(10)
    print("Task completed")

# Fire and forget - no await needed
background_tasks.create(long_running_task())
```

### With run.io_bound

Combine for non-blocking background work:

```python
async def start_video_reader():
    await run.io_bound(read_video_loop, state, video_file)

# Start without blocking the page load
background_tasks.create(start_video_reader())
```

### Key Points

- **No await**: The task runs independently
- **Exception handling**: Exceptions are logged but don't crash the app
- **Lifecycle**: Tasks continue even if the creating context ends

## Thread-Safe State Sharing

When background threads need to share state with the UI thread, use locks:

```python
from dataclasses import dataclass, field
import threading

@dataclass
class SharedState:
    data: str | None = None
    is_running: bool = True
    lock: threading.Lock = field(default_factory=threading.Lock)

# Background thread writes
def background_worker(state: SharedState):
    while state.is_running:
        result = compute_something()
        with state.lock:
            state.data = result

# UI thread reads
def get_current_data(state: SharedState) -> str | None:
    with state.lock:
        return state.data
```

## Cleanup on Disconnect

Always clean up background tasks when the client disconnects:

```python
@ui.page('/')
def index():
    state = SharedState()
    state.is_running = True
    
    # Start background work
    background_tasks.create(start_worker(state))
    
    # Cleanup when client disconnects
    async def cleanup():
        state.is_running = False
    
    ui.context.client.on_disconnect(cleanup)
```

## Common Patterns

### Long-Running Video/Stream Processing

```python
def read_stream(state: StreamState):
    """Runs in background thread via run.io_bound."""
    while state.is_running:
        frame = capture_frame()
        with state.lock:
            state.current_frame = frame

@ui.page('/')
def index():
    state = StreamState()
    
    async def start():
        await run.io_bound(read_stream, state)
    
    background_tasks.create(start())
```

### Periodic Data Fetching

```python
async def fetch_data():
    while True:
        data = await run.io_bound(api_call)
        update_ui(data)
        await asyncio.sleep(5)

background_tasks.create(fetch_data())
```

### Request-Response with Timeout

```python
async def fetch_with_timeout():
    try:
        result = await asyncio.wait_for(
            run.io_bound(slow_api_call),
            timeout=10.0
        )
        return result
    except asyncio.TimeoutError:
        return None
```

## Anti-Patterns

### ❌ Blocking the Event Loop

```python
# BAD - blocks the entire UI
def handle_click():
    time.sleep(5)  # UI freezes!
    ui.notify("Done")
```

### ❌ Using asyncio.run() Inside Handlers

```python
# BAD - creates nested event loop
def handle_click():
    asyncio.run(some_coroutine())  # Error!
```

### ❌ Forgetting to Await run.io_bound

```python
# BAD - coroutine never executes
def handle_click():
    run.io_bound(slow_function)  # Returns coroutine, doesn't run!
```

### ❌ Accessing `self` or Instance State from Background Thread

```python
# BAD - race condition! self._value may change during execution
class MyComponent:
    def process(self):
        task = asyncio.create_task(run.io_bound(self._do_work))
    
    def _do_work(self):
        # DANGER: accessing self from background thread
        return self._value * 2  # Race condition!
```

### ✅ Correct Patterns

```python
# GOOD - await the coroutine
async def handle_click():
    result = await run.io_bound(slow_function)

# GOOD - create task for fire-and-forget
def handle_click():
    background_tasks.create(run.io_bound(slow_function))

# GOOD - create task and poll
def handle_click():
    task = asyncio.create_task(run.io_bound(slow_function))

# GOOD - capture values BEFORE entering background thread
class MyComponent:
    def process(self):
        # Capture all needed values on main thread
        value = self._value
        format_type = self._format
        
        # Pass captured values to static method
        task = asyncio.create_task(
            run.io_bound(MyComponent._do_work, value, format_type)
        )
    
    @staticmethod
    def _do_work(value: int, format_type: str) -> int:
        # Safe: no instance access, only uses passed arguments
        return value * 2
```

## Asyncio Context Issues

**Critical**: When using `asyncio.create_task()` directly, the task runs outside of any client's execution context. This means you **cannot access UI elements** from within the task - NiceGUI won't know which client to update.

### ❌ Problem: Lost Client Context

```python
async def fetch_and_update():
    data = await run.io_bound(slow_api_call)
    ui.notify(data)  # ERROR: No client context!

def handle_click():
    asyncio.create_task(fetch_and_update())  # Context lost!
```

### ✅ Solution 1: Use `ui.timer` with `once=True`

For delayed execution that preserves client context, use a one-shot timer:

```python
def handle_click():
    async def delayed_work():
        data = await run.io_bound(slow_api_call)
        ui.notify(data)  # Works! Timer preserves context
    
    # Execute immediately (0 delay) but within client context
    ui.timer(0, delayed_work, once=True)
```

### ✅ Solution 2: Use `background_tasks.create()`

NiceGUI's `background_tasks` preserves the client context:

```python
async def fetch_and_update():
    data = await run.io_bound(slow_api_call)
    ui.notify(data)  # Works! Context preserved

def handle_click():
    background_tasks.create(fetch_and_update())
```

### When to Use Each

| Method | Context Preserved | Use Case |
|--------|-------------------|----------|
| `ui.timer(0, fn, once=True)` | ✅ Yes | Deferred execution, UI updates |
| `background_tasks.create()` | ✅ Yes | Fire-and-forget with UI access |
| `asyncio.create_task()` | ❌ No | Only for non-UI background work |

## Race Conditions in Background Threads

**Critical**: Functions executed via `run.io_bound()` run in a separate thread. Accessing instance attributes (`self.xxx`) from these functions creates race conditions because:

1. The main thread may modify the attribute while the background thread reads it
2. The background thread may read partially-updated state
3. Multiple background tasks may interfere with each other

### Safe Pattern: Capture Before Thread

```python
def start_background_work(self):
    # 1. Capture all needed values on main thread (safe)
    callback = self._callback
    config = self._config
    data = self._data.copy()  # Copy mutable data!
    
    # 2. Pass as arguments to static/module-level function
    task = asyncio.create_task(
        run.io_bound(process_data, callback, config, data)
    )

def process_data(callback, config, data):
    """Static function - no self access, thread-safe."""
    result = callback(data)
    return format_result(result, config)
```

### What Can Be Safely Accessed

| Safe | Unsafe |
|------|--------|
| Function arguments | `self.xxx` attributes |
| Local variables | Global mutable state |
| Immutable data | Shared mutable objects |
| Thread-safe objects | UI elements |

## Performance Considerations

1. **Thread pool size**: Default pool has limited threads; don't saturate it
2. **Lock contention**: Keep critical sections short
3. **Memory**: Large data in shared state consumes memory
4. **Timer frequency**: Don't poll too frequently (5-100ms is usually fine)

## See Also

- [Custom Components](./custom_components.md) - Building JS components that use background execution
- [Three.js Integration](./threejs_integration.md) - Example of background rendering
- Sample: `samples/video_custom_component` - Complete example with video processing

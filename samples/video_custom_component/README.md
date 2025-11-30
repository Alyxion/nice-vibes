# Video Custom Component
<!-- animated -->

![Animation](animated.gif)

A comprehensive sample demonstrating **custom JavaScript components**, **background execution with `run.io_bound`**, and **real-time video processing** with OpenCV filters.

## What This Sample Demonstrates

### 1. Custom JavaScript Component (`AnimatedImage`)

- **Python-JS Communication**: Bidirectional events between Python and Vue.js
- **Pull-based Frame Requests**: JS requests frames, Python responds with base64 images
- **High-FPS Display**: Smooth animation using `requestAnimationFrame`
- **Props and Methods**: Passing configuration from Python to JS

### 2. Background Execution with `run.io_bound`

- **Non-blocking I/O**: Video reading runs in background thread pool
- **`background_tasks.create()`**: Fire-and-forget async task management
- **`ui.timer`**: Polling for async task completion
- **Thread-safe State**: Lock-protected shared data between threads

### 3. Real-time Video Processing

- **16 OpenCV Filters**: Sobel, Canny, Thermal, Blur, Sharpen, Cartoon, etc.
- **Dynamic Filter Selection**: Change filters at runtime via dropdowns
- **Synchronized Multi-view**: 4 views showing same frame with different filters

## Video Source

This sample uses a free video from Pexels:
- **Video**: [Traffic Flow in the Highway](https://www.pexels.com/video/traffic-flow-in-the-highway-2103099/)
- **License**: Free to use (Pexels license)

## Setup

1. Download the video from the link above
2. Save it as `video.mp4` in this directory
3. Run the sample

The video file is gitignored to keep the repository small.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Background Thread (run.io_bound)           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  read_video_loop()                                      │ │
│  │  - OpenCV VideoCapture                                  │ │
│  │  - Resize frames to display size                        │ │
│  │  - Store in VideoState.current_frame                    │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                    Lock-protected access
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              4x AnimatedImage (Custom Component)             │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │   Original   │  │  Sobel Edge  │  ← Filter selectable    │
│  └──────────────┘  └──────────────┘                         │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  Canny Edge  │  │   Thermal    │  ← via dropdown         │
│  └──────────────┘  └──────────────┘                         │
│                                                              │
│  JS requests frame → Python applies filter → encodes JPEG   │
│  → sends base64 → JS displays image                         │
└─────────────────────────────────────────────────────────────┘
```

## Running

```bash
cd samples/video_custom_component
python main.py
```

Then open http://localhost:8080 in your browser.

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Main application, video reading, UI layout |
| `animated_image.py` | Python side of custom component |
| `animated_image.js` | Vue.js component for high-FPS image display |
| `filters.py` | 16 OpenCV filters with configurable parameters |

## Key Patterns

### Custom Component Definition

```python
# animated_image.py
class AnimatedImage(Element, component='animated_image.js'):
    def __init__(self, width, height, ...):
        self._props['width'] = width
        self.on('frame-request', self._handle_frame_request)
```

### Background Task with run.io_bound

```python
async def start_reader():
    await run.io_bound(read_video_loop, state, VIDEO_FILE)

background_tasks.create(start_reader())
```

### Non-blocking Frame Generation

```python
# Start task without blocking
self._pending_task = asyncio.create_task(run.io_bound(callback))

# Timer polls for completion
def _check_pending_frame(self):
    if self._pending_task and self._pending_task.done():
        frame_data = self._pending_task.result()
        self.run_method('updateFrame', base64_data)
```

### Thread-Safe Shared State

```python
@dataclass
class VideoState:
    current_frame: np.ndarray | None = None
    lock: threading.Lock = field(default_factory=threading.Lock)

# Background thread writes
with state.lock:
    state.current_frame = frame

# UI thread reads
with state.lock:
    frame = state.current_frame
```

### Cleanup on Disconnect

```python
async def cleanup():
    state.is_running = False

ui.context.client.on_disconnect(cleanup)
```

## Requirements

- nicegui
- opencv-python
- numpy
- Pillow

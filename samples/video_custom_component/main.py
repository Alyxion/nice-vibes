"""Video Custom Component Sample.

This sample demonstrates three key NiceGUI patterns:

1. **Custom JavaScript Components**:
   - AnimatedImage: Python/Vue.js component for high-FPS image display
   - Bidirectional events (JS requests frames, Python responds)
   - Props passed from Python to JavaScript

2. **Background Execution**:
   - run.io_bound() for non-blocking I/O operations
   - background_tasks.create() for fire-and-forget async tasks
   - ui.timer() for polling async task completion
   - Thread-safe state sharing with locks

3. **Real-time Video Processing**:
   - OpenCV filters applied on-demand
   - 16 selectable filters with configurable parameters
   - Synchronized multi-view display

Video source: https://www.pexels.com/video/traffic-flow-in-the-highway-2103099/
Download the video and save as video.mp4 in this directory.
"""

import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np

from nicegui import app, background_tasks, run, ui

from animated_image import AnimatedImage
from filters import DEFAULT_FILTERS, apply_filter, get_filter_names

# Video file path
VIDEO_DIR = Path(__file__).parent
VIDEO_FILE = VIDEO_DIR / 'video.mp4'

# Display settings
DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540
TARGET_FPS = 30


# --- Video Reader ---

@dataclass
class VideoState:
    """Shared video state for synchronized playback."""
    current_frame: np.ndarray | None = None
    frame_number: int = 0
    is_running: bool = True
    lock: threading.Lock = field(default_factory=threading.Lock)
    
    # Filter selections for each of the 4 views
    selected_filters: list[str] = field(default_factory=lambda: DEFAULT_FILTERS.copy())
    # Custom params per view (index -> param_name -> value)
    filter_params: list[dict] = field(default_factory=lambda: [{}, {}, {}, {}])
    
    @classmethod
    def current(cls) -> 'VideoState':
        """Get or create VideoState for the current user."""
        if 'video_state' not in app.storage.client:
            app.storage.client['video_state'] = cls()
        return app.storage.client['video_state']


def read_video_loop(state: VideoState, video_path: Path) -> None:
    """Read video frames in endless loop.
    
    Runs in background thread. Uses microsleeps with accumulated timing
    to maintain accurate frame rate without drift.
    """
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        return
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_interval = 1.0 / min(fps, TARGET_FPS)
    
    # Accumulated time tracking - never resets, prevents drift
    next_frame_time = time.perf_counter()
    
    while state.is_running:
        ret, frame = cap.read()
        
        if not ret:
            # Loop back to start
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        # Resize for display
        frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        
        with state.lock:
            state.current_frame = frame
            state.frame_number += 1
        
        # Schedule next frame time (accumulates infinitely)
        next_frame_time += frame_interval
        
        # Microsleep until next frame time
        while True:
            remaining = next_frame_time - time.perf_counter()
            if remaining <= 0:
                break
            # Sleep in small increments for responsiveness
            time.sleep(min(remaining, 0.001))  # 1ms max sleep
    
    cap.release()


def get_filtered_frame(
    state: VideoState,
    view_index: int,
    last_frame_number: list[int],  # Mutable container to track last processed frame
) -> np.ndarray | None:
    """Get current frame with filter applied for a specific view.
    
    :param state: Video state with current frame and filter settings
    :param view_index: Index of the view (0-3)
    :param last_frame_number: Single-element list tracking last processed frame number
    :return: BGR numpy array if new frame available, None if frame unchanged.
        Returning None allows AnimatedImage to immediately retry for next frame.
    """
    with state.lock:
        frame = state.current_frame
        frame_number = state.frame_number
        filter_name = state.selected_filters[view_index]
        params = state.filter_params[view_index]
    
    if frame is None:
        return None
    
    # Return None if frame hasn't changed - triggers immediate retry
    if frame_number == last_frame_number[0]:
        return None
    
    # Apply filter to new frame
    try:
        result = apply_filter(frame.copy(), filter_name, params)
        last_frame_number[0] = frame_number
        return result
    except Exception:
        return None


# --- UI ---

# Static files
STATIC_DIR = Path(__file__).parent / 'static'
app.add_static_files('/static', STATIC_DIR)


@ui.page('/')
def index():
    """Main page with 2x2 video filter grid."""
    ui.dark_mode().enable()
    
    # Load external CSS
    ui.add_head_html('<link rel="stylesheet" href="/static/app.css">')
    
    # Check if video exists
    if not VIDEO_FILE.exists():
        with ui.column().classes('w-full min-h-screen items-center justify-center p-8'):
            with ui.card().classes('bg-gray-800 text-white p-6 max-w-xl'):
                ui.label('Video Not Found').classes('text-xl font-bold text-red-400 mb-4')
                ui.markdown('''
**To use this demo, download a video:**

1. Save any MP4 video as `video.mp4` in this directory
2. Refresh this page

See README.md for a recommended free video source.
                ''')
        return
    
    # Get or create video state
    state = VideoState.current()
    state.is_running = True
    
    # Start video reader in background thread
    async def start_reader():
        await run.io_bound(read_video_loop, state, VIDEO_FILE)
    
    background_tasks.create(start_reader())
    
    # Build UI
    with ui.element('div').classes('main-container'):
        # Header bar
        with ui.element('div').classes('header-bar'):
            with ui.column().classes('gap-0'):
                ui.label('Surveillance Monitor').classes('header-title')
                ui.label('Real-time video analysis • 4 channels').classes('header-subtitle')
            with ui.element('div').classes('status-indicator'):
                ui.element('div').classes('status-dot')
                ui.label('LIVE')
        
        # 2x2 Grid
        all_filter_names = get_filter_names()
        camera_names = ['CAM 01', 'CAM 02', 'CAM 03', 'CAM 04']
        
        with ui.element('div').classes('video-grid'):
            for view_index in range(4):
                with ui.element('div').classes('video-cell'):
                    # Track last processed frame number per view
                    last_frame_num = [-1]
                    
                    # Create frame getter for this view index
                    def make_frame_getter(idx: int, frame_num_ref: list):
                        def get_frame() -> np.ndarray | None:
                            return get_filtered_frame(state, idx, frame_num_ref)
                        return get_frame
                    
                    frame_getter = make_frame_getter(view_index, last_frame_num)
                    
                    # Video header with filter selector
                    with ui.element('div').classes('video-header'):
                        ui.label(camera_names[view_index]).classes('camera-label')
                        filter_select = ui.select(
                            options=all_filter_names,
                            value=state.selected_filters[view_index],
                        ).props('dense dark borderless').classes('text-white text-sm')
                        
                        # Update filter when changed
                        def make_filter_change_handler(idx: int, frame_num_ref: list):
                            def on_change(e):
                                state.selected_filters[idx] = e.value
                                state.filter_params[idx] = {}
                                frame_num_ref[0] = -1
                            return on_change
                        
                        filter_select.on_value_change(
                            make_filter_change_handler(view_index, last_frame_num)
                        )
                    
                    # Animated image component
                    AnimatedImage(
                        width=DISPLAY_WIDTH,
                        height=DISPLAY_HEIGHT,
                        show_fps=True,
                        on_frame_request=frame_getter,
                    )
    
    # Cleanup on disconnect
    async def cleanup():
        state.is_running = False
    
    ui.context.client.on_disconnect(cleanup)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        show=False,
        title='Surveillance Monitor',
        reload=True,
        uvicorn_reload_includes='*.py,*.js,*.css',
    )

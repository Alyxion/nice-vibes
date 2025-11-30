"""Animated Image Component - Custom NiceGUI element with JS/Python communication.

This component demonstrates:
- Custom JavaScript/Vue component integration
- High-frequency Python→JS image updates (up to 30 fps)
- JS→Python event-driven frame requests
- Automatic image encoding (PIL Image or numpy array)
- Non-blocking background thread execution with run.io_bound
"""

import asyncio
import base64
from io import BytesIO
from typing import Callable, Union

import numpy as np
from PIL import Image

from nicegui import run, ui
from nicegui.element import Element
from nicegui.events import GenericEventArguments, handle_event

# Type alias for frame callback return types
FrameType = Union[Image.Image, np.ndarray, None]


class AnimatedImage(Element, component='animated_image.js'):
    """A custom component that displays images at high frame rates.
    
    The JavaScript side requests frames via events, and Python responds
    with base64-encoded images. The callback can return:
    - PIL.Image.Image (RGB mode)
    - numpy.ndarray (BGR, RGB, RGBA, or grayscale)
    - None to skip the frame
    
    This pull-based approach ensures:
    - No frame buildup if client is slow
    - Automatic frame rate adaptation
    - Clean separation of concerns
    - Non-blocking frame generation via run.io_bound
    """
    
    def __init__(
        self,
        width: int = 400,
        height: int = 300,
        show_fps: bool = True,
        target_fps: int = 30,
        image_format: str = 'jpeg',
        quality: int = 85,
        on_frame_request: Callable[[], FrameType] | None = None,
    ) -> None:
        """Initialize the animated image component.
        
        :param width: Display width in pixels
        :param height: Display height in pixels
        :param show_fps: Whether to show FPS counter overlay
        :param target_fps: Target frames per second (max 30)
        :param image_format: Image format ('jpeg' or 'png')
        :param quality: JPEG quality (1-100) or PNG compression (0-9)
        :param on_frame_request: Callback returning PIL Image, numpy array, or None
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['showFps'] = show_fps
        self._props['targetFps'] = min(target_fps, 30)
        self._props['imageFormat'] = image_format
        
        self._image_format = image_format
        self._quality = quality
        self._frame_callback = on_frame_request
        self._pending_task: asyncio.Task | None = None  # Track pending io_bound task
        self._ready_to_send = False  # Track if JS is ready for next frame
        
        # Register handler for frame requests from JS
        self.on('frame-request', self._handle_frame_request)
        
        # Timer to check for completed frame generation and send immediately
        self._timer = ui.timer(0.01, self._check_pending_frame)  # 100Hz check for low latency
    
    @staticmethod
    def _encode_frame(frame: FrameType, image_format: str, quality: int) -> bytes | None:
        """Encode a frame to bytes. Thread-safe, no instance access.
        
        :param frame: PIL Image, numpy array (BGR/RGBA/grayscale), or None
        :param image_format: 'jpeg' or 'png'
        :param quality: JPEG quality (1-100) or PNG compression level
        :return: Encoded image bytes, or None if frame is None/invalid
        """
        if frame is None:
            return None
        
        # Convert numpy array to PIL Image
        if isinstance(frame, np.ndarray):
            if frame.ndim == 2:
                # Grayscale
                img = Image.fromarray(frame, mode='L').convert('RGB')
            elif frame.ndim == 3:
                if frame.shape[2] == 3:
                    # Assume BGR (OpenCV default), convert to RGB
                    img = Image.fromarray(frame[:, :, ::-1], mode='RGB')
                elif frame.shape[2] == 4:
                    # BGRA, convert to RGB
                    img = Image.fromarray(frame[:, :, 2::-1], mode='RGB')
                else:
                    return None
            else:
                return None
        elif isinstance(frame, Image.Image):
            img = frame if frame.mode == 'RGB' else frame.convert('RGB')
        else:
            return None
        
        # Encode to bytes
        buffer = BytesIO()
        if image_format == 'jpeg':
            img.save(buffer, format='JPEG', quality=quality)
        else:
            img.save(buffer, format='PNG', compress_level=min(quality // 10, 9))
        return buffer.getvalue()
    
    @staticmethod
    def _generate_and_encode_frame(
        callback: Callable[[], FrameType],
        image_format: str,
        quality: int,
    ) -> str | None:
        """Generate frame and encode to base64 string. Runs in background thread.
        
        This is a staticmethod to avoid accessing instance state from
        a background thread, which would cause race conditions.
        """
        frame = callback()
        if frame is None:
            return None
        
        frame_bytes = AnimatedImage._encode_frame(frame, image_format, quality)
        if frame_bytes is None:
            return None
        
        return base64.b64encode(frame_bytes).decode('ascii')
    
    def _handle_frame_request(self, _e: GenericEventArguments) -> None:
        """Handle frame request from JavaScript.
        
        Marks that JS is ready to receive a frame and immediately tries to
        start frame generation.
        """
        if self._frame_callback is None:
            return
        
        # JS is ready to receive
        self._ready_to_send = True
        
        # Start processing if not already doing so
        self._try_generate_frame()
    
    def _try_generate_frame(self) -> None:
        """Try to start frame generation if conditions are met."""
        # Skip if already processing or JS not ready
        if self._pending_task is not None or not self._ready_to_send:
            return
        
        # Capture all values needed by background thread BEFORE entering it
        # This avoids race conditions from accessing self in the thread
        callback = self._frame_callback
        image_format = self._image_format
        quality = self._quality
        
        if callback is None:
            return
        
        # Start io_bound task - callback + encoding both run in background thread
        self._pending_task = asyncio.create_task(
            run.io_bound(AnimatedImage._generate_and_encode_frame, callback, image_format, quality)
        )
    
    def _check_pending_frame(self) -> None:
        """Timer callback to check if frame generation is complete and send."""
        if self._pending_task is None:
            # No pending task - try to start one if JS is waiting
            if self._ready_to_send:
                self._try_generate_frame()
            return
        
        if not self._pending_task.done():
            return  # Still processing, check again next tick
        
        # Get result and send immediately
        try:
            base64_data = self._pending_task.result()
            
            if base64_data is not None and self._ready_to_send:
                self.run_method('updateFrame', base64_data)
                self._ready_to_send = False  # Wait for next request from JS
            elif base64_data is None and self._ready_to_send:
                # No frame available, try again immediately
                self._pending_task = None
                self._try_generate_frame()
                return
        except Exception:
            pass  # Ignore errors, will retry
        finally:
            self._pending_task = None
    
    def on_frame_request(self, callback: Callable[[], FrameType]) -> 'AnimatedImage':
        """Set the callback for frame requests.
        
        The callback should return a PIL Image, numpy array, or None to skip.
        
        :param callback: Function returning PIL Image, numpy array (BGR/grayscale), or None
        :return: Self for method chaining
        """
        self._frame_callback = callback
        return self
    
    def start(self) -> None:
        """Start the animation."""
        self.run_method('setRunning', True)
    
    def stop(self) -> None:
        """Stop the animation."""
        self.run_method('setRunning', False)
    
    async def get_fps(self) -> float:
        """Get the current frames per second.
        
        Returns:
            Current FPS as measured by the client
        """
        return await self.run_method('getFps')

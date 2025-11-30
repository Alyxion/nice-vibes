"""OpenCV image filters for video processing.

This module provides a collection of popular image filters that can be
applied to video frames in real-time.
"""

from dataclasses import dataclass, field
from typing import Callable

import cv2
import numpy as np


@dataclass
class FilterConfig:
    """Configuration for a filter with adjustable parameters."""
    name: str
    func: Callable[[np.ndarray, dict], np.ndarray]
    params: dict = field(default_factory=dict)
    description: str = ''


# --- Filter Functions ---

def filter_original(frame: np.ndarray, params: dict) -> np.ndarray:
    """No filter - return original frame."""
    return frame


def filter_grayscale(frame: np.ndarray, params: dict) -> np.ndarray:
    """Convert to grayscale."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def filter_sobel(frame: np.ndarray, params: dict) -> np.ndarray:
    """Sobel edge detection filter."""
    ksize = params.get('ksize', 3)
    scale = params.get('scale', 1.0)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    sobel = np.sqrt(sobel_x**2 + sobel_y**2) * scale
    sobel = np.uint8(np.clip(sobel, 0, 255))
    return cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)


def filter_canny(frame: np.ndarray, params: dict) -> np.ndarray:
    """Canny edge detection filter."""
    threshold1 = params.get('threshold1', 100)
    threshold2 = params.get('threshold2', 200)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1, threshold2)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def filter_thermal(frame: np.ndarray, params: dict) -> np.ndarray:
    """Thermal/heat map effect."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.applyColorMap(gray, cv2.COLORMAP_JET)


def filter_blur(frame: np.ndarray, params: dict) -> np.ndarray:
    """Gaussian blur filter."""
    ksize = params.get('ksize', 15)
    # Ensure ksize is odd
    ksize = ksize if ksize % 2 == 1 else ksize + 1
    return cv2.GaussianBlur(frame, (ksize, ksize), 0)


def filter_sharpen(frame: np.ndarray, params: dict) -> np.ndarray:
    """Sharpen filter using unsharp masking."""
    strength = params.get('strength', 1.5)
    blurred = cv2.GaussianBlur(frame, (0, 0), 3)
    return cv2.addWeighted(frame, 1 + strength, blurred, -strength, 0)


def filter_emboss(frame: np.ndarray, params: dict) -> np.ndarray:
    """Emboss effect."""
    strength = params.get('strength', 1.0)
    kernel = np.array([[-2, -1, 0],
                       [-1, 1, 1],
                       [0, 1, 2]]) * strength
    embossed = cv2.filter2D(frame, -1, kernel)
    return embossed


def filter_sepia(frame: np.ndarray, params: dict) -> np.ndarray:
    """Sepia tone effect."""
    intensity = params.get('intensity', 1.0)
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia = cv2.transform(frame, kernel)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    return cv2.addWeighted(frame, 1 - intensity, sepia, intensity, 0)


def filter_negative(frame: np.ndarray, params: dict) -> np.ndarray:
    """Negative/invert colors."""
    return cv2.bitwise_not(frame)


def filter_posterize(frame: np.ndarray, params: dict) -> np.ndarray:
    """Posterize effect - reduce color levels."""
    levels = params.get('levels', 4)
    levels = max(2, min(levels, 16))
    divisor = 256 // levels
    return (frame // divisor) * divisor


def filter_cartoon(frame: np.ndarray, params: dict) -> np.ndarray:
    """Cartoon effect using bilateral filter and edge detection."""
    line_size = params.get('line_size', 7)
    blur_value = params.get('blur_value', 7)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value if blur_value % 2 == 1 else blur_value + 1)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, line_size if line_size % 2 == 1 else line_size + 1, 5)
    
    color = cv2.bilateralFilter(frame, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon


def filter_sketch(frame: np.ndarray, params: dict) -> np.ndarray:
    """Pencil sketch effect."""
    blur_strength = params.get('blur_strength', 21)
    blur_strength = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    inv_gray = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv_gray, (blur_strength, blur_strength), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


def filter_hdr(frame: np.ndarray, params: dict) -> np.ndarray:
    """HDR-like effect using CLAHE."""
    clip_limit = params.get('clip_limit', 3.0)
    
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def filter_vignette(frame: np.ndarray, params: dict) -> np.ndarray:
    """Vignette effect - darken edges."""
    strength = params.get('strength', 0.5)
    
    rows, cols = frame.shape[:2]
    X = cv2.getGaussianKernel(cols, cols * 0.5)
    Y = cv2.getGaussianKernel(rows, rows * 0.5)
    kernel = Y * X.T
    mask = kernel / kernel.max()
    mask = mask * strength + (1 - strength)
    
    result = frame.copy().astype(np.float32)
    for i in range(3):
        result[:, :, i] = result[:, :, i] * mask
    return np.clip(result, 0, 255).astype(np.uint8)


def filter_cool(frame: np.ndarray, params: dict) -> np.ndarray:
    """Cool color temperature."""
    intensity = params.get('intensity', 30)
    result = frame.copy()
    result[:, :, 0] = np.clip(result[:, :, 0].astype(np.int16) + intensity, 0, 255)  # Blue
    result[:, :, 2] = np.clip(result[:, :, 2].astype(np.int16) - intensity, 0, 255)  # Red
    return result.astype(np.uint8)


def filter_warm(frame: np.ndarray, params: dict) -> np.ndarray:
    """Warm color temperature."""
    intensity = params.get('intensity', 30)
    result = frame.copy()
    result[:, :, 0] = np.clip(result[:, :, 0].astype(np.int16) - intensity, 0, 255)  # Blue
    result[:, :, 2] = np.clip(result[:, :, 2].astype(np.int16) + intensity, 0, 255)  # Red
    return result.astype(np.uint8)


# --- Filter Registry ---

AVAILABLE_FILTERS: dict[str, FilterConfig] = {
    'Original': FilterConfig(
        name='Original',
        func=filter_original,
        description='No filter applied'
    ),
    'Grayscale': FilterConfig(
        name='Grayscale',
        func=filter_grayscale,
        description='Convert to black and white'
    ),
    'Sobel Edge': FilterConfig(
        name='Sobel Edge',
        func=filter_sobel,
        params={'ksize': 3, 'scale': 1.0},
        description='Sobel edge detection'
    ),
    'Canny Edge': FilterConfig(
        name='Canny Edge',
        func=filter_canny,
        params={'threshold1': 100, 'threshold2': 200},
        description='Canny edge detection'
    ),
    'Thermal': FilterConfig(
        name='Thermal',
        func=filter_thermal,
        description='Heat map colorization'
    ),
    'Blur': FilterConfig(
        name='Blur',
        func=filter_blur,
        params={'ksize': 15},
        description='Gaussian blur'
    ),
    'Sharpen': FilterConfig(
        name='Sharpen',
        func=filter_sharpen,
        params={'strength': 1.5},
        description='Sharpen edges'
    ),
    'Emboss': FilterConfig(
        name='Emboss',
        func=filter_emboss,
        params={'strength': 1.0},
        description='Emboss/relief effect'
    ),
    'Sepia': FilterConfig(
        name='Sepia',
        func=filter_sepia,
        params={'intensity': 1.0},
        description='Vintage sepia tone'
    ),
    'Negative': FilterConfig(
        name='Negative',
        func=filter_negative,
        description='Invert colors'
    ),
    'Posterize': FilterConfig(
        name='Posterize',
        func=filter_posterize,
        params={'levels': 4},
        description='Reduce color levels'
    ),
    'Cartoon': FilterConfig(
        name='Cartoon',
        func=filter_cartoon,
        params={'line_size': 7, 'blur_value': 7},
        description='Cartoon effect'
    ),
    'Sketch': FilterConfig(
        name='Sketch',
        func=filter_sketch,
        params={'blur_strength': 21},
        description='Pencil sketch effect'
    ),
    'HDR': FilterConfig(
        name='HDR',
        func=filter_hdr,
        params={'clip_limit': 3.0},
        description='HDR-like enhancement'
    ),
    'Vignette': FilterConfig(
        name='Vignette',
        func=filter_vignette,
        params={'strength': 0.5},
        description='Darken edges'
    ),
    'Cool': FilterConfig(
        name='Cool',
        func=filter_cool,
        params={'intensity': 30},
        description='Cool color temperature'
    ),
    'Warm': FilterConfig(
        name='Warm',
        func=filter_warm,
        params={'intensity': 30},
        description='Warm color temperature'
    ),
}

# Default filters shown in the 2x2 grid
DEFAULT_FILTERS = ['Original', 'Sobel Edge', 'Canny Edge', 'Thermal']


def get_filter_names() -> list[str]:
    """Get list of all available filter names."""
    return list(AVAILABLE_FILTERS.keys())


def get_filter(name: str) -> FilterConfig:
    """Get filter configuration by name."""
    return AVAILABLE_FILTERS.get(name, AVAILABLE_FILTERS['Original'])


def apply_filter(frame: np.ndarray, name: str, params: dict | None = None) -> np.ndarray:
    """Apply a filter to a frame.
    
    :param frame: Input BGR frame
    :param name: Filter name
    :param params: Optional parameter overrides
    :return: Filtered BGR frame
    """
    config = get_filter(name)
    merged_params = {**config.params, **(params or {})}
    return config.func(frame, merged_params)

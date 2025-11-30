"""Three.js Scene Component - Custom NiceGUI element for advanced 3D.

This component demonstrates:
- Loading Three.js from CDN
- Custom particle system with shaders
- Real-time parameter updates from Python
- OrbitControls for camera interaction
"""

from typing import Any

from nicegui.element import Element


class ThreeJSScene(Element, component='threejs_scene.js'):
    """A custom Three.js scene with tornado particle effect.
    
    This bypasses NiceGUI's basic ui.scene to allow full Three.js control,
    including custom shaders, particle systems, and post-processing.
    """
    
    def __init__(
        self,
        particle_count: int = 5000,
        rotation_speed: float = 2.0,
        height: float = 8.0,
        radius: float = 3.0,
        color_intensity: float = 1.0,
        wind_strength: float = 1.0,
    ) -> None:
        """Initialize the Three.js tornado scene.
        
        :param particle_count: Number of particles in the tornado
        :param rotation_speed: Angular velocity of rotation
        :param height: Tornado height
        :param radius: Base radius of the tornado
        :param color_intensity: Brightness of the glow effect
        :param wind_strength: Turbulence/chaos in particle movement
        """
        super().__init__()
        self._props['particleCount'] = particle_count
        self._props['rotationSpeed'] = rotation_speed
        self._props['height'] = height
        self._props['radius'] = radius
        self._props['colorIntensity'] = color_intensity
        self._props['windStrength'] = wind_strength
    
    def update_settings(self, settings: dict[str, Any]) -> None:
        """Update tornado settings in real-time.
        
        :param settings: Dictionary of setting names to values
        """
        self.run_method('updateSettings', settings)
    
    def reset_camera(self) -> None:
        """Reset camera to default position."""
        self.run_method('resetCamera')
    
    def set_paused(self, paused: bool) -> None:
        """Pause or resume the animation."""
        self.run_method('setPaused', paused)

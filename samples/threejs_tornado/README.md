# Three.js Tornado Visualization
<!-- animated -->

![Animation](animated.gif)

A stunning 3D tornado particle system demonstrating advanced Three.js integration with NiceGUI.

## Features

- **5000+ Animated Particles** - GPU-accelerated particle system
- **Custom GLSL Shaders** - Vertex and fragment shaders for glow effects
- **Real-time Controls** - Adjust speed, size, intensity on the fly
- **Orbit Camera** - Drag to rotate, scroll to zoom
- **Additive Blending** - Fire-like glow effect

## Three.js Integration

This sample bypasses NiceGUI's basic `ui.scene` to demonstrate full Three.js control:

```python
class ThreeJSScene(Element, component='threejs_scene.js', 
                   libraries=['https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js']):
    """Custom Three.js component with full shader access."""
    
    def update_settings(self, settings: dict) -> None:
        self.run_method('updateSettings', settings)
```

## Shader Highlights

The tornado uses custom GLSL shaders for:

- **Spiral Motion** - Particles rotate faster at the top
- **Funnel Shape** - Radius increases with height
- **Turbulence** - Wind-like chaos using sine waves
- **Glow Effect** - Additive blending with color intensity

## Controls

| Control | Effect |
|---------|--------|
| **Particles** | Number of particles (1K-20K) |
| **Rotation Speed** | Angular velocity |
| **Height** | Tornado height |
| **Radius** | Base width |
| **Glow Intensity** | Brightness of fire effect |
| **Wind Turbulence** | Chaos/randomness |

## Patterns Demonstrated

- **Custom Element with JS** - `Element` subclass with `component=` parameter
- **CDN Libraries** - Loading Three.js from CDN via `libraries=` parameter
- **Python→JS Methods** - `run_method()` for real-time updates
- **GLSL Shaders** - Custom vertex/fragment shaders in JavaScript
- **OrbitControls** - Camera interaction from Three.js examples

## Running

```bash
cd samples/threejs_tornado
poetry run python main.py
```

Then open http://localhost:8080

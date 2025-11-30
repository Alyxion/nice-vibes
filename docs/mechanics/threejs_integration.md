# Three.js Integration

NiceGUI includes a bundled Three.js library (`nicegui-scene`) that you can use for custom 3D visualizations beyond the basic `ui.scene` component.

## Basic Setup

Create a custom element that imports from `nicegui-scene`:

```python
# threejs_scene.py
from nicegui.element import Element

class ThreeJSScene(Element, component='threejs_scene.js'):
    """Custom Three.js scene component."""
    
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            self._props[key] = value
    
    def update_settings(self, settings: dict) -> None:
        """Send settings to JavaScript."""
        self.run_method('updateSettings', settings)
```

## JavaScript Component

Import Three.js from NiceGUI's bundled module:

```javascript
// threejs_scene.js
import SceneLib from "nicegui-scene";
const { THREE, OrbitControls } = SceneLib;

export default {
  template: `<div ref="container" style="width: 100%; height: 100%;"></div>`,
  
  props: {
    // Define your props here
  },
  
  mounted() {
    this.initScene();
    this.animate();
  },
  
  methods: {
    initScene() {
      // Setup Three.js scene, camera, renderer
    },
    animate() {
      requestAnimationFrame(() => this.animate());
      // Render loop
    }
  }
};
```

## Critical: Vue Reactivity Conflict

**Problem**: Vue wraps objects in reactive proxies, but Three.js objects have non-configurable properties that break when proxied.

**Error message**:
```
TypeError: 'get' on proxy: property 'modelViewMatrix' is a read-only 
and non-configurable data property on the proxy target but the proxy 
did not return its actual value
```

**Solution**: Store Three.js objects outside Vue's reactivity system using a `WeakMap`:

```javascript
import SceneLib from "nicegui-scene";
const { THREE, OrbitControls } = SceneLib;

// Store Three.js objects outside Vue reactivity
const threeState = new WeakMap();

export default {
  data() {
    return {
      // Only store simple values here, NOT Three.js objects
      isPaused: false,
      settings: {},
    };
  },

  mounted() {
    // Initialize non-reactive Three.js state
    threeState.set(this, {
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      clock: null,
    });
    
    this.$nextTick(() => {
      this.initScene();
      this.animate();
    });
  },

  methods: {
    // Helper to access Three.js state
    getState() {
      return threeState.get(this);
    },
    
    initScene() {
      const state = this.getState();
      const container = this.$refs.container;
      
      state.scene = new THREE.Scene();
      state.camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
      state.renderer = new THREE.WebGLRenderer({ antialias: true });
      state.renderer.setSize(container.clientWidth, container.clientHeight);
      container.appendChild(state.renderer.domElement);
      
      state.controls = new OrbitControls(state.camera, state.renderer.domElement);
      state.clock = new THREE.Clock();
    },
    
    animate() {
      requestAnimationFrame(() => this.animate());
      const state = this.getState();
      if (!state || !state.renderer) return;
      
      state.controls.update();
      state.renderer.render(state.scene, state.camera);
    }
  }
};
```

## Custom Shaders

Three.js ShaderMaterial works with the bundled version:

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color(0xff6600) },
  },
  vertexShader: `
    varying vec3 vPosition;
    void main() {
      vPosition = position;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform vec3 uColor;
    varying vec3 vPosition;
    void main() {
      gl_FragColor = vec4(uColor, 1.0);
    }
  `,
  transparent: true,
  blending: THREE.AdditiveBlending,
});
```

**Note**: When using `vertexColors: true`, do NOT declare `attribute vec3 color` in your shader - Three.js adds it automatically. Declaring it causes:
```
ERROR: 0:72: 'color' : redefinition
```

## Full-Screen Layout

To prevent scrollbars in full-screen 3D scenes:

```python
ui.add_head_html('''<style>
    html, body { 
        margin: 0; 
        padding: 0; 
        overflow: hidden;
        background-color: #000 !important; 
    }
    .nicegui-content { 
        padding: 0 !important;
        overflow: hidden;
    }
    .q-page { padding: 0 !important; }
</style>''')

with ui.element('div').classes('w-full h-screen relative'):
    scene = ThreeJSScene().classes('absolute inset-0')
```

## Python → JavaScript Communication

Use `run_method` to call JavaScript methods:

```python
class ThreeJSScene(Element, component='threejs_scene.js'):
    def update_settings(self, settings: dict) -> None:
        self.run_method('updateSettings', settings)
    
    def reset_camera(self) -> None:
        self.run_method('resetCamera')
```

```javascript
methods: {
  updateSettings(settings) {
    const state = this.getState();
    // Update uniforms, recreate geometry, etc.
  },
  
  resetCamera() {
    const state = this.getState();
    state.camera.position.set(0, 5, 15);
    state.controls.target.set(0, 0, 0);
  }
}
```

## Available Three.js Exports

The `nicegui-scene` module exports:

```javascript
import SceneLib from "nicegui-scene";
const {
  THREE,           // Full Three.js library
  OrbitControls,   // Camera controls
  DragControls,    // Object dragging
  CSS2DRenderer,   // 2D labels
  CSS3DRenderer,   // 3D CSS elements
  GLTFLoader,      // GLTF model loader
  STLLoader,       // STL model loader
  TWEEN,           // Animation tweening
  Stats,           // Performance stats
} = SceneLib;
```

## Common Pitfalls

1. **Don't use external CDN imports** - Use the bundled `nicegui-scene` module
2. **Don't store Three.js objects in Vue `data()`** - Use WeakMap pattern
3. **Don't redeclare `color` attribute** with `vertexColors: true`
4. **Wait for `$nextTick`** before accessing `$refs.container` dimensions
5. **Check for null state** in animate loop (component may unmount)

## Example: Particle System

See `samples/threejs_tornado/` for a complete example with:
- 15,000+ animated particles
- Custom GLSL vertex/fragment shaders
- Real-time parameter controls
- Additive blending for glow effects
- OrbitControls for camera interaction

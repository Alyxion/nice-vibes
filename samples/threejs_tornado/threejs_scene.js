// threejs_scene.js - Three.js tornado particle system
// Uses NiceGUI's bundled Three.js (nicegui-scene module)

import SceneLib from "nicegui-scene";
const { THREE, OrbitControls } = SceneLib;

// Store Three.js objects outside Vue reactivity to avoid proxy conflicts
const threeState = new WeakMap();

export default {
  template: `<div ref="container" class="threejs-container" style="width: 100%; height: 100%; min-height: 400px;"></div>`,

  props: {
    particleCount: { type: Number, default: 15000 },
    rotationSpeed: { type: Number, default: 1.5 },
    height: { type: Number, default: 10.0 },
    radius: { type: Number, default: 2.5 },
    colorIntensity: { type: Number, default: 1.2 },
    windStrength: { type: Number, default: 0.8 },
  },

  data() {
    return {
      animationId: null,
      isPaused: false,
      settings: {},
    };
  },

  mounted() {
    console.log('ThreeJS Scene mounting...');
    
    // Initialize non-reactive Three.js state
    threeState.set(this, {
      scene: null,
      camera: null,
      renderer: null,
      particles: null,
      clock: null,
      controls: null,
      groundRing: null,
      ambientParticles: null,
    });
    
    this.settings = {
      particleCount: this.particleCount,
      rotationSpeed: this.rotationSpeed,
      height: this.height,
      radius: this.radius,
      colorIntensity: this.colorIntensity,
      windStrength: this.windStrength,
    };
    
    this.$nextTick(() => {
      this.initScene();
      this.createTornado();
      this.animate();
      
      // Handle resize
      window.addEventListener('resize', this.onResize);
      
      console.log('ThreeJS Scene initialized');
    });
  },

  unmounted() {
    window.removeEventListener('resize', this.onResize);
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    const state = this.getState();
    if (state && state.renderer) {
      state.renderer.dispose();
    }
  },

  methods: {
    // Helper to get Three.js state without Vue reactivity
    getState() {
      return threeState.get(this);
    },
    
    initScene() {
      const state = this.getState();
      const container = this.$refs.container;
      const width = container.clientWidth || 800;
      const height = container.clientHeight || 600;
      
      console.log('Container size:', width, 'x', height);

      // Scene
      state.scene = new THREE.Scene();
      state.scene.background = new THREE.Color(0x000000);
      state.scene.fog = new THREE.FogExp2(0x000000, 0.02);

      // Camera
      state.camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
      state.camera.position.set(0, 5, 15);
      state.camera.lookAt(0, 4, 0);

      // Renderer
      state.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      state.renderer.setSize(width, height);
      state.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      container.appendChild(state.renderer.domElement);

      // Controls
      state.controls = new OrbitControls(state.camera, state.renderer.domElement);
      state.controls.enableDamping = true;
      state.controls.dampingFactor = 0.05;
      state.controls.target.set(0, 4, 0);
      state.controls.update();

      // Clock
      state.clock = new THREE.Clock();

      // Add ground plane with glow
      this.addGround();
      
      // Add ambient particles
      this.addAmbientParticles();
    },

    addGround() {
      // No ground ring - just particles
    },

    addAmbientParticles() {
      const state = this.getState();
      const count = 500;
      
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(count * 3);
      
      for (let i = 0; i < count; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 40;
        positions[i * 3 + 1] = Math.random() * 20;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 40;
      }
      
      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      
      const material = new THREE.PointsMaterial({
        color: 0xff6600,
        size: 0.05,
        transparent: true,
        opacity: 0.5,
      });
      
      state.ambientParticles = new THREE.Points(geometry, material);
      state.scene.add(state.ambientParticles);
    },

    createTornado() {
      const state = this.getState();
      const count = this.settings.particleCount;

      // Particle geometry
      const geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(count * 3);
      const colors = new Float32Array(count * 3);
      const sizes = new Float32Array(count);
      const randoms = new Float32Array(count * 4); // For animation variation

      for (let i = 0; i < count; i++) {
        // Distribute more particles at the base, fewer at top (funnel shape)
        const t = Math.pow(Math.random(), 0.7); // Bias towards bottom
        const angle = Math.random() * Math.PI * 2;
        
        // Funnel shape: narrow at bottom, wider at top
        const radiusAtHeight = this.settings.radius * (0.1 + t * 0.9);
        // Add some thickness variation
        const thickness = 0.3 + Math.random() * 0.4;
        const r = radiusAtHeight * thickness;
        
        positions[i * 3] = Math.cos(angle) * r;
        positions[i * 3 + 1] = t * this.settings.height;
        positions[i * 3 + 2] = Math.sin(angle) * r;

        // Color gradient: deep orange/red at bottom, bright yellow/white at top
        const colorT = t;
        colors[i * 3] = 1.0; // R
        colors[i * 3 + 1] = 0.2 + colorT * 0.6; // G - more orange at bottom
        colors[i * 3 + 2] = colorT * colorT * 0.4; // B - slight blue at very top

        // Size variation - larger at top for glow effect
        sizes[i] = 0.3 + Math.random() * 0.5 + t * 0.5;

        // Random factors for animation
        randoms[i * 4] = Math.random();
        randoms[i * 4 + 1] = Math.random();
        randoms[i * 4 + 2] = Math.random();
        randoms[i * 4 + 3] = Math.random();
      }

      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
      geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
      geometry.setAttribute('aRandom', new THREE.BufferAttribute(randoms, 4));

      // Custom shader material for glow effect
      const material = new THREE.ShaderMaterial({
        uniforms: {
          uTime: { value: 0 },
          uRotationSpeed: { value: this.settings.rotationSpeed },
          uHeight: { value: this.settings.height },
          uRadius: { value: this.settings.radius },
          uColorIntensity: { value: this.settings.colorIntensity },
          uWindStrength: { value: this.settings.windStrength },
          uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) },
        },
        vertexShader: `
          attribute float size;
          attribute vec4 aRandom;
          
          uniform float uTime;
          uniform float uRotationSpeed;
          uniform float uHeight;
          uniform float uRadius;
          uniform float uWindStrength;
          uniform float uPixelRatio;
          
          varying vec3 vColor;
          varying float vAlpha;
          
          void main() {
            // 'color' attribute is auto-defined by Three.js with vertexColors
            vColor = color;
            
            // Get base position
            vec3 pos = position;
            
            // Height factor (0 at bottom, 1 at top)
            float heightFactor = pos.y / uHeight;
            
            // Spiral motion
            float angle = atan(pos.z, pos.x);
            
            // Rotate based on time and height
            float rotationOffset = uTime * uRotationSpeed * (1.0 + heightFactor * 0.5);
            rotationOffset += aRandom.x * 6.28; // Individual offset
            
            // Add wind turbulence
            float turbulence = sin(uTime * 2.0 + aRandom.y * 10.0) * uWindStrength * 0.3;
            turbulence += cos(uTime * 1.5 + aRandom.z * 8.0) * uWindStrength * 0.2;
            
            // Funnel shape: wider at top
            float funnelRadius = uRadius * (0.2 + heightFactor * 0.8);
            funnelRadius += turbulence * heightFactor;
            
            // Apply rotation
            float newAngle = angle + rotationOffset;
            pos.x = cos(newAngle) * funnelRadius;
            pos.z = sin(newAngle) * funnelRadius;
            
            // Vertical movement
            pos.y = mod(pos.y + uTime * 0.5 * (1.0 + aRandom.w), uHeight);
            
            // Add some chaos
            pos.x += sin(uTime * 3.0 + aRandom.x * 20.0) * 0.1 * uWindStrength;
            pos.z += cos(uTime * 2.5 + aRandom.y * 15.0) * 0.1 * uWindStrength;
            
            vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
            gl_Position = projectionMatrix * mvPosition;
            
            // Size attenuation - visible particles
            gl_PointSize = size * 50.0 * uPixelRatio / -mvPosition.z;
            gl_PointSize = clamp(gl_PointSize, 2.0, 40.0);
            
            // Alpha based on height - brighter overall
            vAlpha = 0.6 + heightFactor * 0.4;
            vAlpha *= smoothstep(0.0, 0.05, heightFactor); // Fade at bottom
            vAlpha *= smoothstep(1.0, 0.95, heightFactor); // Fade at top
          }
        `,
        fragmentShader: `
          varying vec3 vColor;
          varying float vAlpha;
          
          uniform float uColorIntensity;
          
          void main() {
            // Circular point with soft edge
            vec2 center = gl_PointCoord - vec2(0.5);
            float dist = length(center);
            if (dist > 0.5) discard;
            
            // Soft glow falloff
            float alpha = 1.0 - smoothstep(0.0, 0.5, dist);
            alpha = pow(alpha, 1.5); // Sharper falloff
            alpha *= vAlpha;
            
            // Glow effect with color - brighter
            vec3 color = vColor * uColorIntensity * 1.5;
            
            gl_FragColor = vec4(color, alpha);
          }
        `,
        transparent: true,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
        vertexColors: true,
      });

      state.particles = new THREE.Points(geometry, material);
      state.scene.add(state.particles);
    },

    animate() {
      this.animationId = requestAnimationFrame(() => this.animate());

      if (this.isPaused) return;

      const state = this.getState();
      if (!state || !state.clock) return;
      
      const elapsed = state.clock.getElapsedTime();

      // Update particle shader uniforms
      if (state.particles) {
        state.particles.material.uniforms.uTime.value = elapsed;
      }

      // Animate ambient particles
      if (state.ambientParticles) {
        state.ambientParticles.rotation.y = elapsed * 0.1;
      }

      state.controls.update();
      state.renderer.render(state.scene, state.camera);
    },

    onResize() {
      const container = this.$refs.container;
      if (!container) return;
      
      const state = this.getState();
      if (!state || !state.camera) return;
      
      const width = container.clientWidth;
      const height = container.clientHeight;

      state.camera.aspect = width / height;
      state.camera.updateProjectionMatrix();
      state.renderer.setSize(width, height);
    },

    // Methods callable from Python
    updateSettings(settings) {
      Object.assign(this.settings, settings);
      
      const state = this.getState();
      if (state && state.particles) {
        const uniforms = state.particles.material.uniforms;
        if (settings.rotationSpeed !== undefined) uniforms.uRotationSpeed.value = settings.rotationSpeed;
        if (settings.height !== undefined) uniforms.uHeight.value = settings.height;
        if (settings.radius !== undefined) uniforms.uRadius.value = settings.radius;
        if (settings.colorIntensity !== undefined) uniforms.uColorIntensity.value = settings.colorIntensity;
        if (settings.windStrength !== undefined) uniforms.uWindStrength.value = settings.windStrength;
      }
      
      // Recreate particles if count changed
      if (settings.particleCount !== undefined && settings.particleCount !== this.particleCount) {
        if (state && state.scene && state.particles) {
          state.scene.remove(state.particles);
        }
        this.createTornado();
      }
    },

    resetCamera() {
      const state = this.getState();
      if (!state) return;
      state.camera.position.set(0, 5, 15);
      state.controls.target.set(0, 4, 0);
      state.controls.update();
    },

    setPaused(paused) {
      this.isPaused = paused;
    },
  },
};

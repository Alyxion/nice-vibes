// animated_image.js - Vue component for high-fps image display
// Requests frames from Python and displays them as fast as possible (up to 30 fps)

export default {
  template: `
    <div class="animated-image-container" :style="containerStyle">
      <img 
        ref="img" 
        :src="currentSrc" 
        :style="imgStyle"
        @load="onImageLoaded"
      />
      <div v-if="showFps" class="fps-counter">{{ displayFps.toFixed(1) }} FPS</div>
    </div>
  `,

  props: {
    width: { type: Number, default: 400 },
    height: { type: Number, default: 300 },
    showFps: { type: Boolean, default: true },
    targetFps: { type: Number, default: 30 },
    imageFormat: { type: String, default: 'jpeg' },
  },

  data() {
    return {
      currentSrc: '',
      displayFps: 0,
      frameCount: 0,
      lastFpsUpdate: 0,
      isRunning: false,
    };
  },

  computed: {
    containerStyle() {
      return {
        width: `${this.width}px`,
        height: `${this.height}px`,
        position: 'relative',
        overflow: 'hidden',
        backgroundColor: '#000',
      };
    },
    imgStyle() {
      return {
        width: '100%',
        height: '100%',
        objectFit: 'contain',
      };
    },
  },

  mounted() {
    this.lastFpsUpdate = performance.now();
    this.start();
  },

  unmounted() {
    this.stop();
  },

  methods: {
    start() {
      if (this.isRunning) return;
      this.isRunning = true;
      this.requestNextFrame();
    },

    stop() {
      this.isRunning = false;
    },

    requestNextFrame() {
      if (!this.isRunning) return;
      // Emit event to Python to request a new frame
      this.$emit('frame-request');
    },

    // Called from Python with base64 image data
    updateFrame(base64Data) {
      if (!this.isRunning) return;
      const mimeType = this.imageFormat === 'png' ? 'image/png' : 'image/jpeg';
      const newSrc = `data:${mimeType};base64,${base64Data}`;
      
      // Only update if different to ensure onload fires
      if (this.currentSrc !== newSrc) {
        this.currentSrc = newSrc;
      } else {
        // Same frame, request next immediately
        requestAnimationFrame(() => this.requestNextFrame());
      }
    },

    onImageLoaded() {
      this.frameCount++;

      // Update FPS counter every second
      const now = performance.now();
      const elapsed = now - this.lastFpsUpdate;
      if (elapsed >= 1000) {
        this.displayFps = (this.frameCount * 1000) / elapsed;
        this.frameCount = 0;
        this.lastFpsUpdate = now;
      }

      // Request next frame immediately after current one is displayed
      if (this.isRunning) {
        // Use requestAnimationFrame for smooth timing
        requestAnimationFrame(() => this.requestNextFrame());
      }
    },

    // Methods callable from Python
    setRunning(running) {
      if (running) {
        this.start();
      } else {
        this.stop();
      }
    },

    getFps() {
      return this.displayFps;
    },
  },
};

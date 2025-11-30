"""Three.js Tornado Visualization Sample.

This sample demonstrates:
- Custom Three.js integration beyond NiceGUI's basic ui.scene
- Particle system with thousands of animated particles
- Custom shaders for glow/fire effects
- Real-time parameter controls
- Full-screen immersive 3D experience
"""

from dataclasses import dataclass, field

from nicegui import app, ui

from threejs_scene import ThreeJSScene


@dataclass
class TornadoSettings:
    """Per-user tornado settings."""
    particle_count: int = 15000
    rotation_speed: float = 1.5
    height: float = 10.0
    radius: float = 2.5
    color_intensity: float = 1.2
    wind_strength: float = 0.8
    
    @classmethod
    def current(cls) -> 'TornadoSettings':
        if 'tornado_settings' not in app.storage.client:
            app.storage.client['tornado_settings'] = cls()
        return app.storage.client['tornado_settings']


class TornadoApp:
    """Main tornado visualization application."""
    
    def __init__(self):
        self.settings = TornadoSettings.current()
        self.scene: ThreeJSScene | None = None
    
    @classmethod
    def current(cls) -> 'TornadoApp':
        if 'tornado_app' not in app.storage.client:
            app.storage.client['tornado_app'] = cls()
        return app.storage.client['tornado_app']
    
    def update_scene(self) -> None:
        """Send updated settings to the Three.js scene."""
        if self.scene:
            self.scene.update_settings({
                'particleCount': self.settings.particle_count,
                'rotationSpeed': self.settings.rotation_speed,
                'height': self.settings.height,
                'radius': self.settings.radius,
                'colorIntensity': self.settings.color_intensity,
                'windStrength': self.settings.wind_strength,
            })
    
    def build(self) -> None:
        """Build the tornado visualization UI."""
        ui.dark_mode().enable()
        
        # Dark background styling - prevent scrollbars
        ui.add_head_html('''<style>
            html, body { 
                margin: 0; 
                padding: 0; 
                overflow: hidden;
                background-color: #000 !important; 
            }
            .nicegui-content { 
                background-color: #000 !important; 
                padding: 0 !important;
                overflow: hidden;
            }
            .q-page { padding: 0 !important; }
            .q-card { background-color: rgba(30, 30, 30, 0.9) !important; border: 1px solid #333; }
            .q-expansion-item, .q-expansion-item__container, .q-item,
            .q-expansion-item__content, .q-item__section {
                background: transparent !important;
                background-color: transparent !important;
            }
        </style>''')
        
        # Use fixed height container
        with ui.element('div').classes('w-full h-screen relative'):
            # Three.js scene (full screen)
            self.scene = ThreeJSScene(
                particle_count=self.settings.particle_count,
                rotation_speed=self.settings.rotation_speed,
                height=self.settings.height,
                radius=self.settings.radius,
                color_intensity=self.settings.color_intensity,
                wind_strength=self.settings.wind_strength,
            ).classes('absolute inset-0')
            
            # Header overlay
            with ui.row().classes('absolute top-0 left-0 right-0 z-10 p-4 justify-between items-center'):
                with ui.column().classes('gap-0'):
                    ui.label('Three.js + NiceGUI').classes('text-white text-2xl font-bold')
                    ui.label('Tornado Particle System').classes('text-gray-400 text-sm')
            
            # Bottom control panel
            with ui.column().classes('absolute bottom-4 left-1/2 z-10 transform -translate-x-1/2'):
                self._build_control_panel()
    
    def _build_control_panel(self) -> None:
        """Build the collapsible control panel at bottom center."""
        # Container with transparency
        with ui.element('div').classes('w-96 rounded-lg overflow-hidden').style(
            'background: rgba(0,0,0,0.25); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.15);'
        ):
            # Collapsible state
            expanded = {'value': True}
            
            def toggle():
                expanded['value'] = not expanded['value']
                content.set_visibility(expanded['value'])
                icon.props(f'name={"expand_less" if expanded["value"] else "expand_more"}')
            
            # Header row - always visible, clickable
            with ui.row().classes('w-full items-center justify-between p-3 cursor-pointer').on('click', toggle):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('tune').classes('text-orange-400')
                    ui.label('Controls').classes('text-white font-medium')
                with ui.row().classes('items-center gap-3'):
                    ui.label('Drag to rotate • Scroll to zoom').classes('text-gray-400 text-xs')
                    icon = ui.icon('expand_less').classes('text-gray-400')
            
            # Collapsible content
            with ui.column().classes('w-full gap-3 px-3 pb-3') as content:
                # Row 1: Particles and Rotation
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Particles').classes('text-gray-300 text-xs')
                        ui.slider(min=1000, max=30000, step=1000, value=self.settings.particle_count).on_value_change(
                            lambda e: self._update('particle_count', int(e.value))
                        ).props('dense dark color=orange')
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Rotation').classes('text-gray-300 text-xs')
                        ui.slider(min=0.5, max=5.0, step=0.1, value=self.settings.rotation_speed).on_value_change(
                            lambda e: self._update('rotation_speed', e.value)
                        ).props('dense dark color=orange')
                
                # Row 2: Height and Radius
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Height').classes('text-gray-300 text-xs')
                        ui.slider(min=4.0, max=15.0, step=0.5, value=self.settings.height).on_value_change(
                            lambda e: self._update('height', e.value)
                        ).props('dense dark color=orange')
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Radius').classes('text-gray-300 text-xs')
                        ui.slider(min=1.0, max=6.0, step=0.5, value=self.settings.radius).on_value_change(
                            lambda e: self._update('radius', e.value)
                        ).props('dense dark color=orange')
                
                # Row 3: Glow and Wind
                with ui.row().classes('w-full gap-4'):
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Glow').classes('text-gray-300 text-xs')
                        ui.slider(min=0.2, max=2.5, step=0.1, value=self.settings.color_intensity).on_value_change(
                            lambda e: self._update('color_intensity', e.value)
                        ).props('dense dark color=orange')
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label('Turbulence').classes('text-gray-300 text-xs')
                        ui.slider(min=0.0, max=3.0, step=0.1, value=self.settings.wind_strength).on_value_change(
                            lambda e: self._update('wind_strength', e.value)
                        ).props('dense dark color=orange')
                
                # Reset button
                with ui.row().classes('w-full justify-center'):
                    ui.button('Reset', on_click=self._reset_settings).props('flat dense size=sm color=orange')
    
    def _update(self, key: str, value: float) -> None:
        """Update a setting and sync to scene."""
        setattr(self.settings, key, value)
        self.update_scene()
    
    def _reset_settings(self) -> None:
        """Reset all settings to defaults."""
        self.settings.particle_count = 15000
        self.settings.rotation_speed = 1.5
        self.settings.height = 10.0
        self.settings.radius = 2.5
        self.settings.color_intensity = 1.2
        self.settings.wind_strength = 0.8
        self.update_scene()
        ui.notify('Settings reset')


@ui.page('/')
def index():
    TornadoApp.current().build()


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        show=False,
        title='Three.js + NiceGUI',
        reload=True,
        uvicorn_reload_includes='*.py,*.js,*.css',
    )

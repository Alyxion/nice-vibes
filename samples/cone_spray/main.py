"""Hollow Cone Nozzle Spray Visualization - Main Application.

Demonstrates:
- Custom Three.js component with particle physics
- Hollow cone spray pattern with adjustable geometry
- Real-time parameter controls via sliders
- Canvas texture for round particles
- Emission accumulator for frame-rate-independent emission
- WeakMap pattern for Vue/Three.js integration
"""

from nicegui import ui

from cone_spray_scene import ConeSprayScene


def create_app() -> None:
    """Create the main application UI."""
    
    # Add custom CSS for full-screen layout
    ui.add_head_html('''
    <style>
        html, body {
            margin: 0;0
            padding: 0;
            overflow: hidden;
            background-color: #1a1a2e !important;
        }
        .nicegui-content {
            padding: 0 !important;
        }
        .q-page {
            padding: 0 !important;
        }
        .control-panel {
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(79, 195, 247, 0.3);
        }
        .control-section {
            border-bottom: 1px solid rgba(79, 195, 247, 0.2);
            padding-bottom: 1rem;
            margin-bottom: 1rem;
        }
        .control-section:last-child {
            border-bottom: none;
        }
        .slider-label {
            color: #b0b0c0;
            font-size: 0.85rem;
        }
        .value-display {
            color: #4fc3f7;
            font-weight: 600;
            min-width: 60px;
            text-align: right;
        }
    </style>
    ''')

    # Main layout
    with ui.row().classes('w-full h-screen'):
        # Control Panel (Left Side)
        with ui.column().classes('control-panel w-80 h-full p-4 gap-2'):
            ui.label('Jasmins Hollow Cone').classes('text-xl font-bold text-cyan-400 mb-2')
            ui.label('Interactive 3D Visualization').classes('text-sm text-gray-400 mb-4')
            
            # Create the scene reference (will be set later)
            scene_ref = {'scene': None}
            
            # Cone Geometry Section
            with ui.column().classes('control-section w-full gap-3'):
                ui.label('Cone Geometry 123').classes('text-md font-semibold text-cyan-300')
                
                # Inner Angle
                with ui.row().classes('w-full items-center'):
                    ui.label('Inner Angle').classes('slider-label flex-grow')
                    inner_value = ui.label('25°').classes('value-display')
                inner_slider = ui.slider(min=5, max=45, value=25, step=1).classes('w-full')
                inner_slider.on_value_change(lambda e: (
                    inner_value.set_text(f'{e.value}°'),
                    scene_ref['scene'].set_inner_angle(e.value) if scene_ref['scene'] else None
                ))
                
                # Outer Angle
                with ui.row().classes('w-full items-center'):
                    ui.label('Outer Angle').classes('slider-label flex-grow')
                    outer_value = ui.label('35°').classes('value-display')
                outer_slider = ui.slider(min=10, max=60, value=35, step=1).classes('w-full')
                outer_slider.on_value_change(lambda e: (
                    outer_value.set_text(f'{e.value}°'),
                    scene_ref['scene'].set_outer_angle(e.value) if scene_ref['scene'] else None
                ))

            # Flow Parameters Section
            with ui.column().classes('control-section w-full gap-3'):
                ui.label('Flow Parameters').classes('text-md font-semibold text-cyan-300')
                
                # Flow Rate
                with ui.row().classes('w-full items-center'):
                    ui.label('Flow Rate').classes('slider-label flex-grow')
                    flow_value = ui.label('500/s').classes('value-display')
                flow_slider = ui.slider(min=100, max=2000, value=500, step=50).classes('w-full')
                flow_slider.on_value_change(lambda e: (
                    flow_value.set_text(f'{int(e.value)}/s'),
                    scene_ref['scene'].set_flow_rate(int(e.value)) if scene_ref['scene'] else None
                ))
                
                # Initial Velocity
                with ui.row().classes('w-full items-center'):
                    ui.label('Velocity').classes('slider-label flex-grow')
                    vel_value = ui.label('8.0 m/s').classes('value-display')
                vel_slider = ui.slider(min=2, max=20, value=8, step=0.5).classes('w-full')
                vel_slider.on_value_change(lambda e: (
                    vel_value.set_text(f'{e.value:.1f} m/s'),
                    scene_ref['scene'].set_initial_velocity(e.value) if scene_ref['scene'] else None
                ))

            # Particle Properties Section
            with ui.column().classes('control-section w-full gap-3'):
                ui.label('Particle Properties').classes('text-md font-semibold text-cyan-300')
                
                # Particle Size
                with ui.row().classes('w-full items-center'):
                    ui.label('Droplet Size').classes('slider-label flex-grow')
                    size_value = ui.label('0.020').classes('value-display')
                size_slider = ui.slider(min=0.005, max=0.05, value=0.02, step=0.005).classes('w-full')
                size_slider.on_value_change(lambda e: (
                    size_value.set_text(f'{e.value:.3f}'),
                    scene_ref['scene'].set_particle_size(e.value) if scene_ref['scene'] else None
                ))
                
                # Spread Randomness
                with ui.row().classes('w-full items-center'):
                    ui.label('Spread').classes('slider-label flex-grow')
                    spread_value = ui.label('15%').classes('value-display')
                spread_slider = ui.slider(min=0, max=0.5, value=0.15, step=0.05).classes('w-full')
                spread_slider.on_value_change(lambda e: (
                    spread_value.set_text(f'{int(e.value * 100)}%'),
                    scene_ref['scene'].set_spread_randomness(e.value) if scene_ref['scene'] else None
                ))

            # Physics Section
            with ui.column().classes('control-section w-full gap-3'):
                ui.label('Physics').classes('text-md font-semibold text-cyan-300')
                
                # Gravity
                with ui.row().classes('w-full items-center'):
                    ui.label('Gravity').classes('slider-label flex-grow')
                    grav_value = ui.label('9.81 m/s²').classes('value-display')
                grav_slider = ui.slider(min=0, max=20, value=9.81, step=0.5).classes('w-full')
                grav_slider.on_value_change(lambda e: (
                    grav_value.set_text(f'{e.value:.2f} m/s²'),
                    scene_ref['scene'].set_gravity(e.value) if scene_ref['scene'] else None
                ))
                
                # Air Resistance
                with ui.row().classes('w-full items-center'):
                    ui.label('Air Resistance').classes('slider-label flex-grow')
                    air_value = ui.label('0.50').classes('value-display')
                air_slider = ui.slider(min=0, max=2, value=0.5, step=0.1).classes('w-full')
                air_slider.on_value_change(lambda e: (
                    air_value.set_text(f'{e.value:.2f}'),
                    scene_ref['scene'].set_air_resistance(e.value) if scene_ref['scene'] else None
                ))

            # Control Buttons
            with ui.row().classes('w-full gap-2 mt-4'):
                ui.button('Reset View', icon='videocam', on_click=lambda: scene_ref['scene'].reset_camera() if scene_ref['scene'] else None).props('outline').classes('flex-grow')
                ui.button('Pause', icon='pause', on_click=lambda: scene_ref['scene'].toggle_pause() if scene_ref['scene'] else None).props('outline').classes('flex-grow')
            
            with ui.row().classes('w-full gap-2'):
                ui.button('Clear', icon='delete', on_click=lambda: scene_ref['scene'].clear_particles() if scene_ref['scene'] else None).props('outline color=negative').classes('flex-grow')

            # Info
            ui.space()
            with ui.column().classes('w-full gap-1'):
                ui.label('Controls:').classes('text-xs text-gray-500 font-semibold')
                ui.label('Left-click + drag: Rotate').classes('text-xs text-gray-600')
                ui.label('Right-click + drag: Pan').classes('text-xs text-gray-600')
                ui.label('Scroll: Zoom').classes('text-xs text-gray-600')

        # 3D Scene (Right Side - fills remaining space)
        with ui.column().classes('flex-grow h-full'):
            scene = ConeSprayScene(
                inner_angle=25,
                outer_angle=35,
                flow_rate=500,
                particle_size=0.02,
                initial_velocity=8.0,
                gravity=9.81,
                air_resistance=0.5,
                spread_randomness=0.15,
            ).classes('w-full h-full')
            scene_ref['scene'] = scene


# Create the application
create_app()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Hollow Cone Nozzle Spray',
        port=8080,
        reload=True,
        show=False,
        dark=True,
        uvicorn_reload_includes='*.py,*.js,*.css',
    )

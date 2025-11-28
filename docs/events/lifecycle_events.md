# Lifecycle Events

Application and client lifecycle hooks.

## Application Lifecycle

### on_startup
Called once when the app starts:

```python
from nicegui import app, ui

@app.on_startup
async def startup():
    print('App starting...')
    # Initialize database, load config, etc.
```

### on_shutdown
Called once when the app stops:

```python
@app.on_shutdown
async def shutdown():
    print('App shutting down...')
    # Close connections, save state, etc.
```

## Client Lifecycle

### on_connect
Called when a client connects (including reconnects):

```python
@app.on_connect
async def connect():
    print('Client connected')
    # Initialize client-specific state
```

### on_disconnect
Called when a client disconnects:

```python
@app.on_disconnect
async def disconnect():
    print('Client disconnected')
    # Cleanup client resources
```

### on_delete
Called when a client is deleted (no reconnect expected):

```python
@app.on_delete
async def delete():
    print('Client deleted')
    # Final cleanup
```

## Exception Handlers

### on_exception
Called on any exception:

```python
@app.on_exception
async def handle_exception(e):
    print(f'Exception: {e}')
    # Log error, notify admin, etc.
```

### on_page_exception
Called when exception occurs during page build:

```python
@app.on_page_exception
async def handle_page_exception(e):
    ui.label(f'Error: {e}').classes('text-red-500')
```

## Timer Events

Periodic or delayed execution:

```python
from nicegui import ui

# Periodic timer
def update():
    label.text = str(datetime.now())

label = ui.label()
timer = ui.timer(1.0, update)  # Every 1 second

# One-shot timer
ui.timer(5.0, lambda: ui.notify('5 seconds passed'), once=True)

# Control timer
timer.active = False  # Pause
timer.active = True   # Resume
timer.cancel()        # Stop permanently
```

## Page Load Events

```python
@ui.page('/')
async def index():
    # This runs when page is requested
    ui.label('Loading...')
    
    # Use timer for post-load actions
    async def on_load():
        data = await fetch_data()
        container.clear()
        with container:
            ui.label(f'Data: {data}')
    
    container = ui.column()
    ui.timer(0.1, on_load, once=True)
```

## Documentation

- [Lifecycle](https://nicegui.io/documentation/section_configuration_deployment)
- [Timer](https://nicegui.io/documentation/timer)

# NiceGUI App & Configuration

App-level configuration, storage, and lifecycle management.

## App Namespace: `app`

### Storage

| Property | Scope | Persistence |
|----------|-------|-------------|
| `app.storage.tab` | Per browser tab | Server memory |
| `app.storage.client` | Per client connection | Server memory |
| `app.storage.user` | Per user (browser) | Server file |
| `app.storage.general` | App-wide shared | Server file |
| `app.storage.browser` | Per browser | Browser localStorage |

### Lifecycle Hooks

| Method | When Called |
|--------|-------------|
| `app.on_connect()` | Client connects (including reconnect) |
| `app.on_disconnect()` | Client disconnects |
| `app.on_delete()` | Client deleted (no reconnect) |
| `app.on_startup()` | App starts |
| `app.on_shutdown()` | App shuts down |
| `app.on_exception()` | Exception occurs |
| `app.on_page_exception()` | Exception during page build |

### Static Files

| Method | Description |
|--------|-------------|
| `app.add_static_files(url_path, local_path)` | Serve directory |
| `app.add_static_file(url_path, local_path)` | Serve single file |
| `app.add_media_files(url_path, local_path)` | Serve media (streaming) |
| `app.add_media_file(url_path, local_path)` | Serve single media file |

### Other

| Property/Method | Description |
|-----------------|-------------|
| `app.native` | Native mode configuration |
| `app.shutdown()` | Shut down the app |

## Examples

### Storage
```python
from nicegui import app, ui

# Per-user storage (persists across sessions)
app.storage.user['theme'] = 'dark'
theme = app.storage.user.get('theme', 'light')

# Per-tab storage
app.storage.tab['counter'] = 0

# App-wide storage
app.storage.general['total_visits'] = 0
```

### Lifecycle Hooks
```python
from nicegui import app, ui

@app.on_startup
async def startup():
    print('App starting...')

@app.on_shutdown
async def shutdown():
    print('App shutting down...')

@app.on_connect
async def connect():
    print('Client connected')

@app.on_disconnect
async def disconnect():
    print('Client disconnected')
```

### Static Files
```python
from nicegui import app

app.add_static_files('/static', 'static')
app.add_media_files('/media', 'media')
```

### Native Mode
```python
from nicegui import ui

ui.run(native=True, window_size=(800, 600))

# Or configure via app.native
app.native.window_args['size'] = (800, 600)
```

---

## UI Functions

### Page & Navigation

| Function | Description |
|----------|-------------|
| `ui.page(path)` | Decorator to define a page route |
| `ui.navigate.to(url)` | Navigate to URL |
| `ui.navigate.back()` | Go back in history |
| `ui.navigate.forward()` | Go forward in history |
| `ui.navigate.reload()` | Reload page |
| `ui.page_title(title)` | Change page title |

### Styling & Appearance

| Function | Description |
|----------|-------------|
| `ui.colors(primary=..., ...)` | Set color theme |
| `ui.dark_mode(value)` | Set dark mode |
| `ui.dark_mode.enable()` | Enable dark mode |
| `ui.dark_mode.disable()` | Disable dark mode |
| `ui.dark_mode.toggle()` | Toggle dark mode |
| `ui.query(selector)` | Query HTML elements |
| `ui.add_css(css)` | Add CSS to page |
| `ui.add_head_html(html)` | Add HTML to `<head>` |
| `ui.add_body_html(html)` | Add HTML to `<body>` |

### Interaction

| Function | Description |
|----------|-------------|
| `ui.notify(message)` | Show notification toast |
| `ui.download(data, filename)` | Trigger file download |
| `ui.clipboard.write(text)` | Write to clipboard |
| `ui.clipboard.read()` | Read from clipboard |
| `ui.keyboard(on_key=...)` | Keyboard event handler |
| `ui.timer(interval, callback)` | Periodic function calls |
| `ui.on(event, handler)` | Register event handler |

### Execution

| Function | Description |
|----------|-------------|
| `ui.run(...)` | Start NiceGUI server |
| `ui.run_with(app)` | Attach to FastAPI app |
| `ui.run_javascript(code)` | Execute JS on client |
| `ui.update(*elements)` | Send updates to client |

## Examples

### Page Definition
```python
from nicegui import ui

@ui.page('/')
def index():
    ui.label('Home')

@ui.page('/user/{user_id}')
def user_page(user_id: str):
    ui.label(f'User: {user_id}')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
```

### Navigation
```python
ui.button('Go Home', on_click=lambda: ui.navigate.to('/'))
ui.button('Back', on_click=ui.navigate.back)
```

### Notifications
```python
ui.notify('Success!', type='positive')
ui.notify('Warning!', type='warning')
ui.notify('Error!', type='negative')
ui.notify('Info', position='top', close_button=True)
```

### Timer
```python
def update():
    label.text = str(datetime.now())

label = ui.label()
ui.timer(1.0, update)  # Update every second
```

### Dark Mode
```python
ui.dark_mode(True)  # Enable
ui.switch('Dark mode', on_change=lambda e: ui.dark_mode(e.value))
```

### Run Options
```python
ui.run(
    host='0.0.0.0',
    port=8080,
    title='My App',
    dark=True,
    reload=False,
    show=True,  # Open browser
)
```

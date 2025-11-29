# Configuration & Deployment

## ui.run() Parameters

The `ui.run()` function starts the NiceGUI server with various configuration options:

```python
from nicegui import ui

ui.label('Hello World')

ui.run(
    host='0.0.0.0',
    port=8080,
    title='My App',
    reload=True,
)
```

### Core Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `host` | `'127.0.0.1'` | Host to bind to (`'0.0.0.0'` for all interfaces) |
| `port` | `8080` | Port to bind to |
| `title` | `'NiceGUI'` | Page title shown in browser tab |
| `favicon` | `None` | Path to favicon, emoji, SVG, or base64 image |
| `dark` | `None` | Dark mode (`True`, `False`, or `None` for auto) |
| `language` | `'en-US'` | Quasar language pack |
| `show` | `True` | Open browser automatically on startup |

### Development Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `reload` | `True` | Auto-reload on Python file changes |
| `uvicorn_reload_dirs` | cwd | Comma-separated directories to watch |
| `uvicorn_reload_includes` | `'*.py'` | Glob patterns that trigger reload |
| `uvicorn_reload_excludes` | `'.*, .py[cod], .sw.*, ~*'` | Glob patterns to ignore |
| `uvicorn_logging_level` | `'warning'` | Uvicorn log level |

**Tip:** For custom component development, include JS/CSS/HTML files:

```python
ui.run(reload=True, uvicorn_reload_includes='*.py,*.js,*.css,*.html')
```

### Storage & Security

| Parameter | Default | Description |
|-----------|---------|-------------|
| `storage_secret` | `None` | Secret for browser storage (required for `ui.storage.browser`) |
| `session_middleware_kwargs` | `{}` | Additional SessionMiddleware options |

### Connection Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `binding_refresh_interval` | `0.1` | Seconds between binding updates |
| `reconnect_timeout` | `3.0` | Max seconds to wait for browser reconnect |
| `message_history_length` | `1000` | Messages stored for reconnection (0 to disable) |

### Native Window Mode

| Parameter | Default | Description |
|-----------|---------|-------------|
| `native` | `False` | Open in native window instead of browser |
| `window_size` | `None` | Native window size, e.g., `(1024, 768)` |
| `fullscreen` | `False` | Open in fullscreen native window |
| `frameless` | `False` | Remove window frame |

```python
# Native desktop app
ui.run(native=True, window_size=(1200, 800))
```

### SSL/HTTPS

```python
ui.run(
    port=443,
    ssl_certfile='/path/to/cert.pem',
    ssl_keyfile='/path/to/key.pem',
)
```

### Other Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `tailwind` | `True` | Enable Tailwind CSS |
| `prod_js` | `True` | Use production Vue/Quasar builds |
| `on_air` | `False` | Enable NiceGUI On Air remote access |
| `show_welcome_message` | `True` | Show startup message |
| `fastapi_docs` | `False` | Enable FastAPI Swagger/ReDoc |
| `endpoint_documentation` | `'none'` | OpenAPI docs (`'none'`, `'internal'`, `'page'`, `'all'`) |
| `cache_control_directives` | long cache | Cache headers for static files |

## Favicon Options

### Emoji Favicon

```python
ui.run(favicon='🚀')
```

### SVG Favicon

```python
smiley = '''
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <circle cx="100" cy="100" r="78" fill="#ffde34"/>
</svg>
'''
ui.run(favicon=smiley)
```

### Base64 Favicon

```python
icon = 'data:image/png;base64,iVBORw0KGgo...'
ui.run(favicon=icon)
```

## Server Hosting

### Direct Deployment

```python
# Production settings
ui.run(
    host='0.0.0.0',
    port=80,
    reload=False,
    show=False,
)
```

### Docker Deployment

Use the official NiceGUI Docker image:

```bash
docker run -it --restart always \
    -p 80:8080 \
    -e PUID=$(id -u) \
    -e PGID=$(id -g) \
    -v $(pwd)/:/app/ \
    zauberzeug/nicegui:latest
```

Or with docker-compose:

```yaml
app:
    image: zauberzeug/nicegui:latest
    restart: always
    ports:
        - 80:8080
    environment:
        - PUID=1000
        - PGID=1000
    volumes:
        - ./:/app/
```

### Reverse Proxy (NGINX)

For production, use a reverse proxy like NGINX or Traefik to handle SSL termination.

## Packaging with PyInstaller

Bundle your app as a standalone executable:

```python
# main.py
from nicegui import native, ui

def root():
    ui.label('Hello from PyInstaller')

ui.run(root, reload=False, port=native.find_open_port())
```

```bash
nicegui-pack --onefile --name "myapp" main.py
```

### Packaging Options

| Option | Description |
|--------|-------------|
| `--onefile` | Single executable (slower startup) |
| `--onedir` | Directory with executable (faster startup) |
| `--windowed` | No console window (use with `native=True`) |

### macOS Packaging

Add at the top of your main file:

```python
from multiprocessing import freeze_support  # noqa
freeze_support()  # noqa

# rest of your code
```

## NiceGUI On Air

Share your local app over the internet:

```python
# Random URL (1 hour)
ui.run(on_air=True)

# Fixed URL with token from https://on-air.nicegui.io
ui.run(on_air='<your-token>')
```

## Custom Startup Handler

```python
from nicegui import app, ui

ui.label('My App')

app.on_startup(lambda: print('URLs:', app.urls))

ui.run(show_welcome_message=False)
```

## Environment-Based Configuration

```python
import os
from nicegui import ui

ui.run(
    host=os.getenv('HOST', '127.0.0.1'),
    port=int(os.getenv('PORT', 8080)),
    reload=os.getenv('ENV') == 'development',
    storage_secret=os.getenv('STORAGE_SECRET'),
)
```

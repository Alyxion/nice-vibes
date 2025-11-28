# Upload Events

File upload handling.

## on_upload Event

Fires when a file is uploaded:

```python
from nicegui import ui

def handle_upload(e):
    ui.notify(f'Uploaded: {e.name}')
    content = e.content.read()  # File bytes
    # Process file...

# Constructor style
ui.upload(on_upload=handle_upload)

# Method style (post-constructor)
upload = ui.upload()
upload.on_upload(handle_upload)
```

## Upload Event Properties

```python
def handler(e):
    e.name      # Original filename
    e.type      # MIME type (e.g., 'image/png')
    e.content   # SpooledTemporaryFile (file-like object)
    e.sender    # The upload element
```

## Multiple Files

```python
def handle_uploads(e):
    ui.notify(f'Uploaded: {e.name}')

ui.upload(multiple=True, on_upload=handle_uploads)
# on_upload fires once per file
```

## Auto Upload

Upload immediately when file is selected:

```python
ui.upload(auto_upload=True, on_upload=handler)
```

## File Type Restrictions

```python
# Accept only images
ui.upload(on_upload=handler).props('accept=".jpg,.png,.gif,image/*"')

# Accept only PDFs
ui.upload(on_upload=handler).props('accept=".pdf,application/pdf"')
```

## Max File Size

```python
# Limit to 5MB
ui.upload(on_upload=handler, max_file_size=5_000_000)
```

## Upload Progress

```python
upload = ui.upload(on_upload=handler)

# Show progress
progress = ui.linear_progress(value=0)

def update_progress(e):
    progress.value = e.progress

upload.on('progress', update_progress)
```

## Rejected Files

```python
def on_rejected(e):
    ui.notify(f'Rejected: {e.name} - {e.reason}', type='warning')

ui.upload(
    on_upload=handler,
    on_rejected=on_rejected,
    max_file_size=1_000_000,
)
```

## Common Patterns

### Image Preview
```python
import base64

def show_preview(e):
    content = e.content.read()
    b64 = base64.b64encode(content).decode()
    image.source = f'data:{e.type};base64,{b64}'

image = ui.image().classes('w-64')
ui.upload(on_upload=show_preview).props('accept="image/*"')
```

### Save to Disk
```python
from pathlib import Path

UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(e):
    path = UPLOAD_DIR / e.name
    path.write_bytes(e.content.read())
    ui.notify(f'Saved: {path}')

ui.upload(on_upload=save_file)
```

## Documentation

- [Upload](https://nicegui.io/documentation/upload)

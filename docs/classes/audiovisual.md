# NiceGUI Audiovisual Elements

Elements for displaying images, audio, video, and icons.

## Classes

| Class | Description |
|-------|-------------|
| `ui.image` | Display image |
| `ui.interactive_image` | Image with SVG overlays |
| `ui.audio` | Audio player |
| `ui.video` | Video player |
| `ui.icon` | Icon display |
| `ui.avatar` | Avatar/profile image |

## Examples

### Image
```python
ui.image('https://example.com/image.png')
ui.image('/static/logo.png').classes('w-32')
ui.image('data:image/png;base64,...')  # Base64
```

### Interactive Image
```python
with ui.interactive_image('image.png') as img:
    img.svg_content = '<circle cx="100" cy="100" r="50" fill="red"/>'
```

### Audio
```python
audio = ui.audio('https://example.com/sound.mp3')
audio.play()
audio.pause()
```

### Video
```python
video = ui.video('https://example.com/video.mp4')
video.play()
ui.video('video.mp4', autoplay=True, muted=True, loop=True)
```

### Icon
```python
ui.icon('home')
ui.icon('favorite', color='red')
ui.icon('star', size='xl')
# Material Icons: https://fonts.google.com/icons
```

### Avatar
```python
ui.avatar('A')  # Letter avatar
ui.avatar(icon='person')
ui.avatar('https://example.com/photo.jpg')
```

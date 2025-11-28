# NiceGUI Text Elements

Elements for displaying text and formatted content.

## Classes

| Class | Description |
|-------|-------------|
| `ui.label` | Display text |
| `ui.link` | Hyperlink element |
| `ui.link_target` | Anchor target for navigation |
| `ui.chat_message` | Chat-style message bubble |
| `ui.element` | Generic HTML element |
| `ui.markdown` | Render Markdown content |
| `ui.restructured_text` | Render reStructuredText |
| `ui.mermaid` | Render Mermaid diagrams |
| `ui.html` | Raw HTML content |

## Examples

### Label
```python
ui.label('Hello World')
ui.label('Styled').classes('text-2xl text-blue-500')
```

### Link
```python
ui.link('Go to NiceGUI', 'https://nicegui.io')
ui.link('Internal', '/about')
```

### Markdown
```python
ui.markdown('# Heading\n\nSome **bold** text')
ui.markdown('''
    ## Code Example
    ```python
    print("Hello")
    ```
''')
```

### Chat Message
```python
ui.chat_message('Hello!', name='User', sent=True)
ui.chat_message('Hi there!', name='Bot', avatar='🤖')
```

### HTML
```python
ui.html('<strong>Bold</strong> and <em>italic</em>')
```

### Mermaid Diagrams
```python
ui.mermaid('''
    graph TD
    A[Start] --> B[Process]
    B --> C[End]
''')
```

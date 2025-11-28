# Styling in NiceGUI

NiceGUI provides multiple ways to style elements: Tailwind CSS classes, inline styles, Quasar props, and custom CSS.

## .classes() - Tailwind CSS

Apply Tailwind CSS utility classes to any element:

```python
from nicegui import ui

# Text styling
ui.label('Title').classes('text-2xl font-bold text-blue-600')

# Spacing and layout
ui.card().classes('p-4 m-2 w-full max-w-md')

# Flexbox
ui.row().classes('gap-4 justify-between items-center')

# Background and borders
ui.label('Alert').classes('bg-red-100 border border-red-400 rounded p-2')

# Responsive design
ui.label('Responsive').classes('text-sm md:text-base lg:text-xl')
```

### Common Tailwind Classes

| Category | Examples |
|----------|----------|
| **Text** | `text-xl`, `font-bold`, `text-gray-500`, `text-center` |
| **Spacing** | `p-4`, `m-2`, `px-6`, `mt-4`, `gap-2` |
| **Width/Height** | `w-full`, `w-80`, `max-w-md`, `h-screen` |
| **Flexbox** | `flex`, `justify-between`, `items-center`, `gap-4` |
| **Background** | `bg-white`, `bg-gray-100`, `bg-blue-500` |
| **Border** | `border`, `rounded`, `rounded-lg`, `border-gray-300` |

## .style() - Inline CSS

Apply inline CSS for specific styling needs:

```python
from nicegui import ui

# Direct CSS properties
ui.label('Custom').style('color: red; font-size: 24px')

# Complex styling
ui.label('Gradient').style('''
    background: linear-gradient(90deg, #ff0000, #0000ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
''')

# Dynamic styling
size = 20
ui.label('Dynamic').style(f'font-size: {size}px')
```

### When to Use .style()

- CSS properties not available in Tailwind
- Gradients, transforms, animations
- Dynamic values computed at runtime
- Vendor-specific prefixes

## .props() - Quasar Properties

NiceGUI uses Quasar components. Use `.props()` for Quasar-specific styling:

```python
from nicegui import ui

# Button variants
ui.button('Outlined').props('outlined')
ui.button('Flat').props('flat')
ui.button('Round').props('round')

# Input styling
ui.input('Dense').props('dense filled')
ui.input('Outlined').props('outlined')

# Colors (Quasar color palette)
ui.button('Primary').props('color=primary')
ui.button('Negative').props('color=negative')

# Icons
ui.button(icon='home').props('flat round')
```

## ui.add_head_html() - Custom CSS

Add custom CSS rules to the page `<head>`:

```python
from nicegui import ui

# Add custom CSS
ui.add_head_html('''
<style>
    .my-custom-class {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .highlight:hover {
        transform: scale(1.05);
        transition: transform 0.2s;
    }
</style>
''')

# Use the custom class
ui.label('Custom Styled').classes('my-custom-class')
ui.card().classes('highlight')
```

### Global Styles

```python
from nicegui import ui

ui.add_head_html('''
<style>
    /* Override default styles */
    body {
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
</style>
''')
```

### Loading External Fonts

```python
from nicegui import ui

ui.add_head_html('''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    body { font-family: 'Inter', sans-serif; }
</style>
''')
```

## ui.add_css() - Simpler CSS Addition

For just CSS (no full HTML), use `ui.add_css()`:

```python
from nicegui import ui

ui.add_css('''
    .card-hover:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
''')
```

## Combining Approaches

```python
from nicegui import ui

# Custom CSS for complex effects
ui.add_head_html('''
<style>
    .gradient-border {
        border: 3px solid transparent;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #667eea, #764ba2) border-box;
    }
</style>
''')

# Combine Tailwind + custom class + inline style
ui.card().classes('p-4 rounded-lg gradient-border').style('min-width: 300px')
```

## Dark Mode

```python
from nicegui import ui

# Enable dark mode
ui.dark_mode().enable()

# Or toggle
dark = ui.dark_mode()
ui.button('Toggle Dark', on_click=dark.toggle)

# Tailwind dark: prefix works automatically
ui.label('Adaptive').classes('text-black dark:text-white bg-white dark:bg-gray-800')
```

## Summary

| Method | Use Case |
|--------|----------|
| `.classes()` | Tailwind utilities, most common styling |
| `.style()` | Inline CSS, dynamic values, complex CSS |
| `.props()` | Quasar component properties |
| `ui.add_head_html()` | Custom CSS rules, fonts, global styles |
| `ui.add_css()` | Simple CSS additions |

## Documentation

- [Styling & Appearance](https://nicegui.io/documentation/section_styling_appearance)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Quasar Components](https://quasar.dev/vue-components)

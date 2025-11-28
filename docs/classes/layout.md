# NiceGUI Layout Elements

Elements for structuring and organizing the UI.

## Container Classes

| Class | Description |
|-------|-------------|
| `ui.card` | Card container |
| `ui.card_section` | Section within card |
| `ui.card_actions` | Actions area in card |
| `ui.column` | Vertical flex container |
| `ui.row` | Horizontal flex container |
| `ui.grid` | CSS grid container |
| `ui.list` | List container |
| `ui.item` | List item |
| `ui.item_section` | Section within list item |
| `ui.item_label` | Label within list item |
| `ui.expansion` | Expandable/collapsible panel |
| `ui.scroll_area` | Scrollable container |
| `ui.splitter` | Resizable split panels |

## Navigation Classes

| Class | Description |
|-------|-------------|
| `ui.tabs` | Tab container |
| `ui.tab` | Individual tab |
| `ui.tab_panels` | Tab panel container |
| `ui.tab_panel` | Individual tab panel |
| `ui.stepper` | Step wizard |
| `ui.step` | Individual step |
| `ui.stepper_navigation` | Stepper navigation buttons |
| `ui.carousel` | Image/content carousel |
| `ui.carousel_slide` | Carousel slide |
| `ui.pagination` | Pagination control |
| `ui.menu` | Dropdown menu |
| `ui.menu_item` | Menu item |
| `ui.context_menu` | Right-click context menu |

## Page Layout Classes

| Class | Description |
|-------|-------------|
| `ui.header` | Page header |
| `ui.footer` | Page footer |
| `ui.drawer` | Side drawer |
| `ui.left_drawer` | Left side drawer |
| `ui.right_drawer` | Right side drawer |
| `ui.page_sticky` | Sticky positioned element |
| `ui.page_scroller` | Page scroll button |

## Utility Classes

| Class | Description |
|-------|-------------|
| `ui.separator` | Visual separator line |
| `ui.space` | Flexible spacer |
| `ui.skeleton` | Loading skeleton placeholder |
| `ui.slide_item` | Swipeable list item |
| `ui.fullscreen` | Fullscreen control |
| `ui.teleport` | Move element in DOM |
| `ui.timeline` | Timeline display |
| `ui.timeline_entry` | Timeline entry |
| `ui.tooltip` | Tooltip popup |
| `ui.dialog` | Modal dialog |
| `ui.notification` | Notification element |

## Examples

### Basic Containers
```python
with ui.row():
    ui.label('Left')
    ui.label('Right')

with ui.column():
    ui.label('Top')
    ui.label('Bottom')

with ui.grid(columns=3):
    for i in range(9):
        ui.label(f'Cell {i}')
```

### Card
```python
with ui.card():
    ui.label('Card Title').classes('text-xl')
    ui.label('Card content')
    with ui.card_actions():
        ui.button('Action')
```

### Page Layout
```python
with ui.header():
    ui.label('My App').classes('text-xl')

with ui.left_drawer():
    ui.link('Home', '/')
    ui.link('About', '/about')

with ui.footer():
    ui.label('© 2024')
```

### Tabs
```python
with ui.tabs() as tabs:
    tab1 = ui.tab('Tab 1')
    tab2 = ui.tab('Tab 2')

with ui.tab_panels(tabs, value=tab1):
    with ui.tab_panel(tab1):
        ui.label('Content 1')
    with ui.tab_panel(tab2):
        ui.label('Content 2')
```

### Stepper
```python
with ui.stepper() as stepper:
    with ui.step('Step 1'):
        ui.label('First step')
        with ui.stepper_navigation():
            ui.button('Next', on_click=stepper.next)
    with ui.step('Step 2'):
        ui.label('Second step')
        with ui.stepper_navigation():
            ui.button('Back', on_click=stepper.previous)
            ui.button('Done')
```

### Dialog
```python
with ui.dialog() as dialog:
    with ui.card():
        ui.label('Dialog content')
        ui.button('Close', on_click=dialog.close)

ui.button('Open', on_click=dialog.open)
```

### Expansion
```python
with ui.expansion('Click to expand'):
    ui.label('Hidden content')
```

### Splitter
```python
with ui.splitter() as splitter:
    with splitter.before:
        ui.label('Left panel')
    with splitter.after:
        ui.label('Right panel')
```

### Menu
```python
with ui.button('Menu'):
    with ui.menu():
        ui.menu_item('Item 1', on_click=lambda: print('1'))
        ui.menu_item('Item 2', on_click=lambda: print('2'))
```

### Context Menu
```python
with ui.label('Right-click me'):
    with ui.context_menu():
        ui.menu_item('Copy')
        ui.menu_item('Paste')
```

### Tooltip
```python
ui.button('Hover me').tooltip('This is a tooltip')
```

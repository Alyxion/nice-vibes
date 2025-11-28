# NiceGUI Data Elements

Elements for displaying data, charts, and visualizations.

## Classes

| Class | Description |
|-------|-------------|
| `ui.table` | Data table |
| `ui.aggrid` | AG Grid data table |
| `ui.highchart` | Highcharts chart |
| `ui.echart` | Apache ECharts |
| `ui.pyplot` | Matplotlib pyplot context |
| `ui.matplotlib` | Matplotlib figure |
| `ui.line_plot` | Simple line plot |
| `ui.plotly` | Plotly chart |
| `ui.linear_progress` | Linear progress bar |
| `ui.circular_progress` | Circular progress indicator |
| `ui.spinner` | Loading spinner |
| `ui.scene` | 3D scene (Three.js) |
| `ui.scene_view` | Additional view of 3D scene |
| `ui.leaflet` | Leaflet map |
| `ui.tree` | Tree view |
| `ui.log` | Log viewer |
| `ui.editor` | WYSIWYG editor |
| `ui.code` | Code display with syntax highlighting |
| `ui.json_editor` | JSON editor |

## Examples

### Table
```python
columns = [
    {'name': 'name', 'label': 'Name', 'field': 'name'},
    {'name': 'age', 'label': 'Age', 'field': 'age'},
]
rows = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
]
ui.table(columns=columns, rows=rows)
```

### AG Grid
```python
ui.aggrid({
    'columnDefs': [{'field': 'name'}, {'field': 'age'}],
    'rowData': [{'name': 'Alice', 'age': 30}],
})
```

### EChart
```python
ui.echart({
    'xAxis': {'type': 'category', 'data': ['A', 'B', 'C']},
    'yAxis': {'type': 'value'},
    'series': [{'type': 'bar', 'data': [10, 20, 30]}],
})
```

### Plotly
```python
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(x=['A', 'B'], y=[10, 20]))
ui.plotly(fig)
```

### Progress
```python
ui.linear_progress(value=0.7)
ui.circular_progress(value=0.5)
ui.spinner()
ui.spinner('dots')
```

### 3D Scene
```python
with ui.scene() as scene:
    scene.box()
    scene.sphere().move(2, 0, 0)
```

### Leaflet Map
```python
m = ui.leaflet(center=(51.5, -0.1), zoom=10)
m.marker(latlng=(51.5, -0.1))
```

### Tree
```python
ui.tree([
    {'id': '1', 'label': 'Root', 'children': [
        {'id': '2', 'label': 'Child 1'},
        {'id': '3', 'label': 'Child 2'},
    ]}
], label_key='label')
```

### Log
```python
log = ui.log(max_lines=100)
log.push('Log message')
```

### Code Display
```python
ui.code('print("Hello")', language='python')
```

### JSON Editor
```python
ui.json_editor({'key': 'value', 'list': [1, 2, 3]})
```

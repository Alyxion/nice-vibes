# Dashboard Sample

A simple sales dashboard demonstrating NiceGUI best practices.

## Patterns Demonstrated

### Data Modeling
- **Dataclass** for structured user data (`data.py`)
- **`get_current()` class method** for per-user storage
- **No global variables** - all state in `app.storage.client`
- **Computed fields** with `recompute()` method

### Event Handling
- **Constructor style**: `on_click=handler` for buttons
- **Method style**: `.on_value_change()` for inputs triggering recomputation

### Data Binding
- **`.bind_value()`** for two-way binding between inputs and data model
- **`.bind_text_from()`** for automatic display updates when data changes

### Container Updates
- **`.clear()` + `with`** pattern for rebuilding order history list

### Application Structure
- **Main guard**: `if __name__ in {'__main__', '__mp_main__'}:`
- **`storage_secret`** required for `app.storage.client`

## Running

```bash
cd samples/dashboard
poetry run python main.py
```

Then open http://localhost:8080

## File Structure

```
dashboard/
├── main.py     # Single-file app with data model and UI
└── README.md   # This file
```

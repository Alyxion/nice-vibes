# Data Modeling in NiceGUI

Best practices for managing user data in NiceGUI applications.

## Core Principles

1. **Use dataclasses or Pydantic** for data structures
2. **Never use global variables** - NiceGUI serves concurrent users
3. **Group user data in a class** instead of scattered variables
4. **Store per-user data in `app.storage.client`**

## User Data Class Pattern

```python
from dataclasses import dataclass, field
from nicegui import app, ui


@dataclass
class UserData:
    """Per-user application state."""
    name: str = ''
    email: str = ''
    items: list[str] = field(default_factory=list)
    
    @classmethod
    def get_current(cls) -> 'UserData':
        """Get or create UserData for the current user."""
        if 'user_data' not in app.storage.client:
            app.storage.client['user_data'] = cls()
        return app.storage.client['user_data']
```

## Usage in Pages

```python
@ui.page('/')
def index():
    data = UserData.get_current()
    
    ui.input('Name').bind_value(data, 'name')
    ui.input('Email').bind_value(data, 'email')
```

## With Pydantic

```python
from pydantic import BaseModel, Field
from nicegui import app, ui


class UserData(BaseModel):
    """Per-user application state with validation."""
    name: str = ''
    email: str = ''
    age: int = 0
    
    class Config:
        # Allow mutation for binding
        frozen = False
    
    @classmethod
    def get_current(cls) -> 'UserData':
        """Get or create UserData for the current user."""
        if 'user_data' not in app.storage.client:
            app.storage.client['user_data'] = cls()
        return app.storage.client['user_data']
```

## Dashboard with Computed Values

For dashboards where inputs affect computed results:

```python
from dataclasses import dataclass
from nicegui import app, ui


@dataclass
class DashboardData:
    quantity: int = 0
    unit_price: float = 0.0
    total: float = 0.0  # Computed field
    
    def compute_total(self):
        """Recompute derived values."""
        self.total = self.quantity * self.unit_price
    
    @classmethod
    def get_current(cls) -> 'DashboardData':
        if 'dashboard' not in app.storage.client:
            app.storage.client['dashboard'] = cls()
        return app.storage.client['dashboard']


@ui.page('/dashboard')
def dashboard():
    data = DashboardData.get_current()
    
    def on_input_change(e):
        data.compute_total()
    
    # Inputs bound to data, trigger recomputation on change
    ui.number('Quantity', min=0).bind_value(data, 'quantity').on_value_change(on_input_change)
    ui.number('Unit Price', min=0, format='%.2f').bind_value(data, 'unit_price').on_value_change(on_input_change)
    
    # Result automatically updates via bind_text_from
    ui.label().bind_text_from(data, 'total', lambda t: f'Total: ${t:.2f}')
```

## Why Not Global Variables?

```python
# BAD: Global state shared between all users!
user_name = ''
user_items = []

@ui.page('/')
def index():
    global user_name  # All users see/modify the same data!
    ui.input('Name').bind_value(globals(), 'user_name')


# GOOD: Per-user state via app.storage.client
@ui.page('/')
def index():
    data = UserData.get_current()  # Each user gets their own instance
    ui.input('Name').bind_value(data, 'name')
```

## Storage Scopes

| Storage | Scope | Use Case |
|---------|-------|----------|
| `app.storage.client` | Per browser tab | User session data |
| `app.storage.user` | Per authenticated user | Persistent user preferences |
| `app.storage.general` | Shared across all users | App-wide settings |

## Complete Example

```python
from dataclasses import dataclass, field
from nicegui import app, ui


@dataclass
class OrderData:
    customer_name: str = ''
    items: list[dict] = field(default_factory=list)
    discount_percent: float = 0.0
    subtotal: float = 0.0
    total: float = 0.0
    
    def add_item(self, name: str, price: float):
        self.items.append({'name': name, 'price': price})
        self.recompute()
    
    def recompute(self):
        self.subtotal = sum(item['price'] for item in self.items)
        self.total = self.subtotal * (1 - self.discount_percent / 100)
    
    @classmethod
    def get_current(cls) -> 'OrderData':
        if 'order' not in app.storage.client:
            app.storage.client['order'] = cls()
        return app.storage.client['order']


@ui.page('/')
def index():
    order = OrderData.get_current()
    
    ui.input('Customer').bind_value(order, 'customer_name')
    
    ui.number('Discount %', min=0, max=100).bind_value(
        order, 'discount_percent'
    ).on_value_change(lambda: order.recompute())
    
    ui.label().bind_text_from(order, 'subtotal', lambda v: f'Subtotal: ${v:.2f}')
    ui.label().bind_text_from(order, 'total', lambda v: f'Total: ${v:.2f}')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='your-secret-key')  # Required for storage
```

## Documentation

- [Storage](https://nicegui.io/documentation/storage)
- [Data Binding](https://nicegui.io/documentation/section_binding_properties)

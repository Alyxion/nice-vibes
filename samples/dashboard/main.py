"""Sample NiceGUI Dashboard Application.

This sample demonstrates all documented patterns:
- Main guard with __mp_main__
- Dataclass for user data with get_current() pattern
- Per-user storage via app.storage.client
- Data binding with bind_value() and bind_text_from()
- Computed values with on_value_change()
- Page routing with @ui.page
- Container updates with clear() + with
"""

from dataclasses import dataclass, field

from nicegui import app, ui


# --- Data Model ---

@dataclass
class DashboardData:
    """Per-user dashboard state.
    
    All user data is stored in this single class rather than
    scattered across multiple variables. This ensures:
    - Clean data organization
    - Per-user isolation via app.storage.client
    - Easy binding to UI elements
    """
    
    # Input fields
    quantity: int = 5
    unit_price: float = 29.99
    discount_percent: float = 10.0
    
    # Computed fields
    subtotal: float = 0.0
    discount_amount: float = 0.0
    total: float = 0.0
    
    # History
    order_history: list = field(default_factory=list)
    
    def recompute(self) -> None:
        """Recompute derived values from inputs.
        
        Called via on_value_change() when any input changes.
        Results are automatically displayed via bind_text_from().
        """
        self.subtotal = self.quantity * self.unit_price
        self.discount_amount = self.subtotal * (self.discount_percent / 100)
        self.total = self.subtotal - self.discount_amount
    
    
    @classmethod
    def get_current(cls) -> 'DashboardData':
        """Get or create DashboardData for the current user.
        
        Uses app.storage.client which is unique per browser tab.
        This ensures each user has their own isolated data.
        """
        if 'dashboard_data' not in app.storage.client:
            app.storage.client['dashboard_data'] = cls()
        return app.storage.client['dashboard_data']


# --- UI ---


@ui.page('/')
def index():
    """Main dashboard page."""
    data = DashboardData.get_current()
    data.recompute()  # Compute initial values
    
    # Header
    with ui.header().classes('bg-blue-600 text-white'):
        ui.label('Sales Dashboard').classes('text-xl font-bold')
    
    # Main content with padding
    with ui.column().classes('p-8'):
        with ui.row().classes('gap-8'):
            # Left side: Order Calculator
            with ui.card().classes('w-80'):
                ui.label('Order Calculator').classes('text-lg font-semibold')
                
                ui.number('Quantity', min=1, max=100).bind_value(data, 'quantity').on_value_change(lambda: data.recompute())
                ui.number('Unit Price ($)', min=0.01, step=0.01, format='%.2f').bind_value(data, 'unit_price').on_value_change(lambda: data.recompute())
                
                ui.label().bind_text_from(data, 'discount_percent', lambda v: f'Discount: {v:.0f}%')
                ui.slider(min=0, max=50).bind_value(data, 'discount_percent').on_value_change(lambda: data.recompute())
                
                ui.separator()
                
                with ui.row().classes('w-full justify-between'):
                    ui.label('Subtotal:')
                    ui.label().bind_text_from(data, 'subtotal', lambda v: f'${v:.2f}')
                with ui.row().classes('w-full justify-between'):
                    ui.label('Discount:')
                    ui.label().bind_text_from(data, 'discount_amount', lambda v: f'-${v:.2f}')
                with ui.row().classes('w-full justify-between font-bold text-lg'):
                    ui.label('Total:')
                    ui.label().bind_text_from(data, 'total', lambda v: f'${v:.2f}')
                
                ui.button('Add to History', on_click=lambda: add_order()).props('color=primary').classes('w-full mt-4')
            
            # Right side: Order History
            with ui.card().classes('w-80'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('Order History').classes('text-lg font-semibold')
                    ui.button(icon='delete', on_click=lambda: clear_history()).props('flat round size=sm')
                
                empty_label = ui.label('No orders yet').classes('text-gray-500')
                history_container = ui.column().classes('w-full gap-2')
    
    # Footer
    with ui.footer().classes('bg-gray-100'):
        ui.label('NiceGUI Dashboard Sample').classes('text-gray-500 text-sm')
    
    def add_order():
        """Add current order to history by appending to container (no clear)."""
        if data.quantity > 0:
            # Hide "No orders yet" label on first order
            if not data.order_history:
                empty_label.set_visibility(False)
            
            order = {
                'quantity': data.quantity,
                'unit_price': data.unit_price,
                'total': data.total,
            }
            data.order_history.append(order)
            # Append to container without clearing - just enter context and add
            with history_container:
                with ui.card().classes('w-full'):
                    ui.label(f'Order #{len(data.order_history)}')
                    ui.label(f'{order["quantity"]} × ${order["unit_price"]:.2f} = ${order["total"]:.2f}')
    
    def clear_history():
        """Clear all orders - uses clear() + with pattern."""
        data.order_history.clear()
        history_container.clear()
        empty_label.set_visibility(True)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False, title='Sales Dashboard')

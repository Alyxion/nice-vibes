"""Simple calculator app demonstrating NiceGUI best practices.

This is the minimal recommended structure for any NiceGUI application:
- Dataclass for state management
- Data binding instead of manual updates
- Proper page decorator
- Header with app title
- Main guard with title and show=False
"""

from dataclasses import dataclass, field

from nicegui import ui


@dataclass
class CalculatorState:
    principal: float = 1000.0
    rate: float = 5.0
    years: float = 10.0
    result: str = field(default='')

    def calculate(self):
        amount = self.principal * (1 + self.rate / 100) ** self.years
        self.result = f'Final amount: ${amount:,.2f}'


@ui.page('/')
def index():
    state = CalculatorState()

    with ui.header().classes('bg-primary'):
        ui.label('My Calculator App').classes('text-xl font-bold')

    with ui.card().classes('max-w-md mx-auto mt-8 p-6'):
        ui.number('Principal ($)').bind_value(state, 'principal')
        ui.number('Annual Rate (%)').bind_value(state, 'rate')
        ui.number('Years').bind_value(state, 'years')
        ui.button('Calculate', on_click=state.calculate)
        ui.label().bind_text(state, 'result').classes('text-lg font-bold mt-4')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='My Calculator App', show=False)

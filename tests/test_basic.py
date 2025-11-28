"""Basic NiceGUI unit tests demonstrating the User fixture.

These tests use NiceGUI's simulated User fixture which doesn't require a browser.
Each test defines its own page using @ui.page decorator.
"""

import pytest
from nicegui import ui
from nicegui.testing import User


@pytest.fixture
def setup_page():
    """Clear any existing pages before each test."""
    # Pages are registered globally, so we need fresh ones per test
    pass


async def test_label_displays_text(user: User) -> None:
    """Test that a label displays its text."""
    @ui.page('/test')
    def page():
        ui.label('Hello World')
    
    await user.open('/test')
    await user.should_see('Hello World')


async def test_button_click_shows_notification(user: User) -> None:
    """Test that clicking a button shows a notification."""
    @ui.page('/test_button')
    def page():
        ui.button('Click me', on_click=lambda: ui.notify('Button clicked!'))
    
    await user.open('/test_button')
    user.find('Click me').click()
    await user.should_see('Button clicked!')


async def test_input_value_binding(user: User) -> None:
    """Test that input value can be read and modified."""
    @ui.page('/test_input')
    def page():
        input_field = ui.input('Name', value='')
        ui.label().bind_text_from(input_field, 'value', lambda v: f'Hello, {v}!')
    
    await user.open('/test_input')
    user.find('Name').type('Alice')
    await user.should_see('Hello, Alice!')


async def test_checkbox_toggle(user: User) -> None:
    """Test checkbox toggling."""
    @ui.page('/test_checkbox')
    def page():
        checkbox = ui.checkbox('Accept terms')
        ui.label().bind_text_from(checkbox, 'value', lambda v: 'Accepted' if v else 'Not accepted')
    
    await user.open('/test_checkbox')
    await user.should_see('Not accepted')
    user.find('Accept terms').click()
    await user.should_see('Accepted')


async def test_counter_increment(user: User) -> None:
    """Test a simple counter that increments on button click."""
    @ui.page('/test_counter')
    def page():
        counter = {'value': 0}
        label = ui.label('Count: 0')
        
        def increment():
            counter['value'] += 1
            label.text = f'Count: {counter["value"]}'
        
        ui.button('Increment', on_click=increment)
    
    await user.open('/test_counter')
    await user.should_see('Count: 0')
    user.find('Increment').click()
    await user.should_see('Count: 1')
    user.find('Increment').click()
    await user.should_see('Count: 2')

# NiceGUI Testing Guide

This repository uses **pytest** and NiceGUI’s built-in **testing utilities** to test UI logic without needing a real browser.

## Recommended stack

- **pytest** for the test runner
- **pytest-asyncio** for `async def` tests
- **nicegui.testing.User** for simulated UI interaction
- **nicegui.testing.user_plugin** pytest plugin to provide the `user` fixture

In this repo, the plugin is enabled in `tests/conftest.py`:

```python
pytest_plugins = ['nicegui.testing.user_plugin']
```

## Writing a basic unit test

NiceGUI tests typically:

1. Define a test page with `@ui.page('/some_route')`
2. Use the `user` fixture to open the route
3. Interact with elements and assert visible text

Example:

```python
import pytest
from nicegui import ui
from nicegui.testing import User


@pytest.mark.asyncio
async def test_button_click(user: User) -> None:
    @ui.page('/test_button')
    def page():
        ui.button('Click me', on_click=lambda: ui.notify('Clicked'))

    await user.open('/test_button')
    user.find('Click me').click()
    await user.should_see('Clicked')
```

## How the `User` fixture works

- `User` simulates a client session.
- `await user.open('/path')` renders the page.
- `user.find('text')` finds an element by visible text.
- `await user.should_see('text')` waits until the UI shows the text.

This style is ideal for testing:

- **binding logic** (e.g. `bind_text_from`, `bind_value`)
- **event handlers** (`on_click`, `on_change`)
- **simple state updates**

## Important gotcha: `@ui.page` registrations are global

`@ui.page(...)` registrations are global within the Python process.

That means:

- Defining the *same route* in multiple tests can cause conflicts.
- Tests can influence each other if pages share routes.

Recommended patterns:

- **Use unique routes per test**, e.g. `/test_counter`, `/test_checkbox`.
- If you use parametrized tests, ensure each parameter uses a unique route.

## Testing state updates

A good pattern is to store state in a local object and update a bound label:

```python
import pytest
from nicegui import ui
from nicegui.testing import User


@pytest.mark.asyncio
async def test_counter_increment(user: User) -> None:
    @ui.page('/test_counter')
    def page():
        counter = {'value': 0}
        label = ui.label('Count: 0')

        def inc():
            counter['value'] += 1
            label.text = f"Count: {counter['value']}"

        ui.button('Increment', on_click=inc)

    await user.open('/test_counter')
    await user.should_see('Count: 0')
    user.find('Increment').click()
    await user.should_see('Count: 1')
```

## Async handlers

If your UI handler is async, you can define it normally:

```python
@ui.page('/test_async')
def page():
    async def load():
        ui.notify('loaded')

    ui.button('Load', on_click=load)
```

Then test it the same way.

## What not to test with `User`

The `User` fixture is great for unit-style tests but not ideal for:

- pixel-perfect layout assertions
- real browser behavior and client-side rendering details
- complex JS/WebGL behavior (e.g. Three.js scenes)

For those, prefer a separate **integration/E2E** approach (e.g. Playwright/Selenium) and keep it opt-in because it requires more dependencies.

## Running tests

From the repo root:

```bash
poetry run pytest
```

If you’re only working on UI unit tests:

```bash
poetry run pytest -q tests/test_basic.py
```

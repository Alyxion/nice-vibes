# NiceGUI Coding Style Guide

This document describes the coding conventions used in the NiceGUI codebase. Follow these patterns when writing NiceGUI applications and custom components.

## Line Length and Formatting

- **Max line length**: ~120 characters (flexible, readability over strict limits)
- **Imports**: One import per line for `from` imports, grouped by stdlib → third-party → local
- **String quotes**: Single quotes `'` for strings (not double quotes `"`)
- **Trailing commas**: Used in multi-line collections and function signatures

## Type Hints

NiceGUI uses comprehensive type hints throughout:

```python
from typing import Any, Callable, Optional, Union
from typing_extensions import Self

def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
    """Add a callback to be invoked when the button is clicked."""
    ...
    return self
```

### Common Patterns

- `Optional[X]` for nullable parameters
- `Self` for method chaining return types
- `TypeVar` for generic functions
- `ClassVar` for class-level attributes
- `TYPE_CHECKING` block for import-only types (avoids circular imports)

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
    from .element import Element
```

## Docstrings

**Sphinx-style with `:param:` syntax**:

```python
def __init__(self,
             label: Optional[str] = None, *,
             placeholder: Optional[str] = None,
             value: str = '',
             on_change: Optional[Handler[ValueChangeEventArguments]] = None,
             ) -> None:
    """Text Input

    This element is based on Quasar's `QInput <https://quasar.dev/vue-components/input>`_ component.
    The `on_change` event is called on every keystroke and the value updates accordingly.

    :param label: displayed label for the text input
    :param placeholder: text to show if no value is entered
    :param value: the current value of the text input
    :param on_change: callback to execute when the value changes
    """
```

### Docstring Guidelines

- First line: Brief description of the class/method
- Reference Quasar docs with RST link syntax: `` `QBtn <url>`_ ``
- Document all parameters with `:param name: description`
- Note version additions: `(*added in version 2.9.0*)`

## Class Structure

### Mixin-Based Composition

```python
class Button(IconElement, TextElement, DisableableElement, BackgroundColorElement):
    pass

class Input(LabelElement, ValidationElement, DisableableElement, component='input.js'):
    VALUE_PROP: str = 'value'
    LOOPBACK = False
```

### Class Variables

```python
class Element:
    component: Component | None = None
    exposed_libraries: ClassVar[list[Library]] = []
    _default_props: ClassVar[dict[str, Any]] = {}
    _default_classes: ClassVar[list[str]] = []
```

- Use `ClassVar` for class-level attributes
- Prefix private attributes with `_`
- Use UPPER_CASE for class constants

## Method Signatures

### Keyword-Only Arguments After `*`

```python
def __init__(self,
             text: str = '', *,
             on_click: Optional[Handler[ClickEventArguments]] = None,
             color: Optional[str] = 'primary',
             icon: Optional[str] = None,
             ) -> None:
```

- Positional args before `*`
- Keyword-only args after `*`
- Trailing comma on last parameter

### Method Chaining with `Self`

```python
def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
    """Add a callback..."""
    self.on('click', lambda _: handle_event(callback, ...), [])
    return self
```

## Dataclasses

Use `@dataclass` with `**KWONLY_SLOTS` for event arguments:

```python
from dataclasses import dataclass
from .dataclasses import KWONLY_SLOTS

@dataclass(**KWONLY_SLOTS)
class ClickEventArguments(UiEventArguments):
    pass

@dataclass(**KWONLY_SLOTS)
class ValueChangeEventArguments(UiEventArguments):
    value: Any
```

## WeakRef for Circular References

```python
self._client = weakref.ref(client)
self._parent_slot: weakref.ref[Slot] | None = None

@property
def client(self) -> Client:
    client = self._client()
    if client is None:
        raise RuntimeError('The client has been deleted.')
    return client
```

## Linter Directives

When necessary, use inline comments for linter suppression:

```python
global process_pool  # pylint: disable=global-statement # noqa: PLW0603
cast(Self, sender)._handle_value_change(value)  # pylint: disable=protected-access
```

## Import Organization

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import asyncio
from typing import Any, Optional

# 3. Third-party
from typing_extensions import Self

# 4. Local imports (relative)
from . import core, helpers
from .element import Element
from .events import Handler, ClickEventArguments
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `ValueElement`, `ClickEventArguments` |
| Functions/Methods | snake_case | `on_value_change`, `handle_event` |
| Constants | UPPER_SNAKE | `VALUE_PROP`, `LOOPBACK` |
| Private | `_` prefix | `_props`, `_handle_change` |
| Module-private | `_` prefix | `_running_tasks` |

## Error Handling

```python
@property
def client(self) -> Client:
    client = self._client()
    if client is None:
        raise RuntimeError('The client this element belongs to has been deleted.')
    return client
```

- Use `RuntimeError` for programming errors
- Provide descriptive error messages
- Check for None/deleted references before use

## Async Patterns

```python
async def _invoke_callback(self) -> None:
    try:
        result = self.callback()
        if isinstance(result, Awaitable) and not isinstance(result, AwaitableResponse):
            await result
    except Exception as e:
        core.app.handle_exception(e)
```

- Check if result is `Awaitable` before awaiting
- Forward exceptions to central handler
- Use `asyncio.create_task()` for fire-and-forget (but prefer `background_tasks.create()`)

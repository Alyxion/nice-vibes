# Poetry Setup

We recommend [Poetry](https://python-poetry.org/) for dependency management.

## Project Structure

A valid Poetry package requires:

```
my_app/
├── pyproject.toml    # Dependencies and project config
├── poetry.lock       # Locked versions (commit this)
├── README.md         # Required for valid package
├── my_app/           # Package folder (matches project name)
│   ├── __init__.py
│   └── main.py
└── tests/            # Optional test folder
    └── test_app.py
```

## pyproject.toml

```toml
[tool.poetry]
name = "my-app"
version = "0.1.0"
description = "My NiceGUI application"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "my_app"}]

[tool.poetry.dependencies]
python = "^3.12"
nicegui = "*"  # prefer `poetry add nicegui` to track the latest release; do not hand-edit

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Commands

```bash
# Install dependencies
poetry install

# Run application
poetry run python my_app/main.py

# Add a dependency
poetry add httpx

# Add dev dependency
poetry add --group dev pytest

# Update dependencies
poetry update

# Show installed packages
poetry show

# Lock and install in one command (useful after pyproject.toml changes)
poetry lock && poetry install
```

## Running Scripts

Always use `poetry run` to ensure the virtual environment is active:

```bash
# Run main application
poetry run python my_app/main.py

# Run tests
poetry run pytest

# Run any script
poetry run python scripts/my_script.py
```

## Storage Secret

For `app.storage.client` to work, set a storage secret:

```python
ui.run(storage_secret='your-secret-key')
```

Generate a secure secret:

```bash
poetry run python -c "import secrets; print(secrets.token_hex(32))"
```

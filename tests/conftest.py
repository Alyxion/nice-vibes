"""Pytest configuration for NiceGUI tests.

NiceGUI provides a User fixture for simulated testing without a browser.
The user fixture requires either:
1. A main_file in pytest.ini pointing to your app
2. Or defining pages directly in tests using @ui.page decorator
"""

pytest_plugins = ['nicegui.testing.user_plugin']

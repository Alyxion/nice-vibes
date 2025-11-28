# Stock Peer Analysis Dashboard

Compare multiple stocks against their peer group average.

## Features

- **Stock Selection** - Toggle stocks with chips
- **Time Horizon** - 1 month to 5 years
- **Best/Worst Performers** - Highlights top and bottom stocks
- **Normalized Chart** - Compare prices starting at 100
- **Individual Charts** - Each stock vs peer average with shaded difference

## Patterns Demonstrated

- **Dark Mode** - `ui.dark_mode().enable()` and custom CSS
- **Async Data Loading** - `run.io_bound()` for API calls
- **ECharts** - `ui.echart()` for interactive charts
- **Chips** - Selectable `ui.chip()` for toggles
- **Timer** - `ui.timer()` for initial data load
- **Custom CSS** - `ui.add_head_html()` for dark theme

## Running

```bash
cd samples/stock_peers
poetry run python main.py
```

Then open http://localhost:8080

## Dependencies

- `yfinance` - Yahoo Finance API for stock data

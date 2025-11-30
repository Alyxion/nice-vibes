"""Stock Peer Analysis Dashboard.

Compare multiple stocks against their peer group average.
Demonstrates: dark mode, charts, toggles, data binding, async loading.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta

import yfinance as yf
from nicegui import app, ui


# --- Data Model ---

@dataclass
class StockData:
    """Per-user stock analysis state."""
    
    available_tickers: list[str] = field(default_factory=lambda: [
        'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'AMZN', 'TSLA', 'META'
    ])
    selected_tickers: list[str] = field(default_factory=lambda: [
        'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'AMZN', 'TSLA', 'META'
    ])
    time_horizon: str = '1y'
    prices: dict = field(default_factory=dict)
    normalized: dict = field(default_factory=dict)
    returns: dict = field(default_factory=dict)
    dates: list[str] = field(default_factory=list)
    loading: bool = False
    
    @classmethod
    def current(cls) -> 'StockData':
        """Get or create StockData for the current user."""
        if 'stock_data' not in app.storage.client:
            app.storage.client['stock_data'] = cls()
        return app.storage.client['stock_data']


TIME_HORIZONS = {
    '1d': ('1 Day', 1),
    '1w': ('1 Week', 7),
    '1mo': ('1 Month', 30),
    '3mo': ('3 Months', 90),
    '6mo': ('6 Months', 180),
    '1y': ('1 Year', 365),
    '2y': ('2 Years', 730),
    '5y': ('5 Years', 1825),
}


def fetch_stock_data(tickers: list[str], days: int) -> tuple[dict, list[str]]:
    """Fetch historical stock data. Returns (prices, dates)."""
    end = datetime.now()
    start = end - timedelta(days=max(days, 2))  # At least 2 days for yfinance
    
    # Choose interval based on time horizon
    if days <= 1:
        interval = '5m'
    elif days <= 7:
        interval = '1h'
    else:
        interval = '1d'
    
    data = {}
    dates = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start, end=end, interval=interval)
            if not hist.empty:
                data[ticker] = hist['Close'].tolist()
                if not dates:  # Get dates from first ticker
                    if days <= 1:
                        dates = [d.strftime('%H:%M') for d in hist.index]
                    elif days <= 7:
                        dates = [d.strftime('%a %H:%M') for d in hist.index]
                    elif days <= 90:
                        dates = [d.strftime('%b %d') for d in hist.index]
                    else:
                        dates = [d.strftime('%b %Y') for d in hist.index]
        except Exception:
            pass
    return data, dates


def normalize_prices(prices: dict) -> dict:
    """Normalize prices to start at 100 for comparison."""
    normalized = {}
    for ticker, values in prices.items():
        if values and values[0] > 0:
            base = values[0]
            normalized[ticker] = [v / base * 100 for v in values]
    return normalized


def calculate_returns(prices: dict) -> dict:
    """Calculate total return for each stock."""
    returns = {}
    for ticker, values in prices.items():
        if values and len(values) > 1 and values[0] > 0:
            returns[ticker] = ((values[-1] - values[0]) / values[0]) * 100
    return returns


# --- UI ---

@ui.page('/')
def index():
    """Main dashboard page."""
    # Dark mode
    ui.dark_mode().enable()
    
    data = StockData.current()
    
    # Custom dark theme CSS
    ui.add_head_html('''
    <style>
        body { background: #0e1117; }
        .q-card { background: #1a1d24 !important; border: 1px solid #2d3139; }
        .main-container { max-width: 1920px; margin: 0 auto; }
    </style>
    ''')
    
    # Header
    with ui.header().classes('bg-gradient-to-r from-blue-900 to-purple-900'):
        with ui.row().classes('w-full max-w-6xl mx-auto items-center gap-3'):
            ui.icon('analytics').classes('text-2xl text-blue-300')
            ui.label('Stock Peer Analysis').classes('text-xl font-bold')
            ui.label('Compare stocks against their peer group').classes('text-gray-300 text-sm ml-4')
    
    # Main container with max width
    with ui.column().classes('w-full main-container p-8 gap-8'):
        # Controls card
        with ui.card().classes('w-full'):
            with ui.row().classes('w-full gap-8 items-start p-2'):
                # Stock selection
                with ui.column().classes('gap-2'):
                    ui.label('Stock tickers').classes('text-gray-400 text-sm font-medium')
                    with ui.row().classes('gap-2 flex-wrap'):
                        for ticker in data.available_tickers:
                            ui.chip(
                                ticker,
                                selectable=True,
                                selected=ticker in data.selected_tickers,
                                on_click=lambda e, t=ticker: toggle_ticker(t)
                            ).props('color=primary')
                
                # Time horizon
                with ui.column().classes('gap-2'):
                    ui.label('Time horizon').classes('text-gray-400 text-sm font-medium')
                    horizon_toggle = ui.toggle(
                        {k: v[0] for k, v in TIME_HORIZONS.items()},
                        value=data.time_horizon,
                        on_change=lambda e: set_horizon(e.value)
                    )
        
        # Performers row
        performers_row = ui.row().classes('gap-8')
        
        # Main chart card
        with ui.card().classes('w-full'):
            ui.label('Normalized Price Comparison').classes('text-lg font-semibold')
            ui.label('All stocks normalized to 100 at start date for easy comparison').classes('text-gray-500 text-sm mb-2')
            main_chart = ui.echart({}).classes('w-full h-96')
        
        # Individual charts section
        with ui.card().classes('w-full'):
            ui.label('Individual Stocks vs Peer Average').classes('text-lg font-semibold')
            ui.label('The shaded area shows the difference between each stock and the peer group average.').classes('text-gray-500 text-sm mb-4')
            individual_charts = ui.row().classes('w-full gap-4 flex-wrap justify-center')
    
    async def load_data():
        """Load stock data asynchronously."""
        if not data.selected_tickers:
            return
        
        data.loading = True
        ui.notify('Loading stock data...', type='info')
        
        _, days = TIME_HORIZONS[data.time_horizon]
        
        # Fetch data (blocking call wrapped)
        from nicegui import run
        result = await run.io_bound(fetch_stock_data, data.selected_tickers, days)
        prices, dates = result
        
        data.prices = prices
        data.dates = dates
        data.normalized = normalize_prices(prices)
        data.returns = calculate_returns(prices)
        data.loading = False
        
        update_charts()
    
    def update_charts():
        """Update all charts with current data."""
        if not data.normalized:
            return
        
        # Update performers
        performers_row.clear()
        with performers_row:
            if data.returns:
                sorted_returns = sorted(data.returns.items(), key=lambda x: x[1], reverse=True)
                best = sorted_returns[0]
                worst = sorted_returns[-1]
                
                with ui.column().classes('gap-1'):
                    ui.label('Best performer').classes('text-gray-400 text-sm')
                    ui.label(best[0]).classes('text-xl font-bold')
                    ui.label(f'+{best[1]:.1f}%').classes('text-green-400')
                
                with ui.column().classes('gap-1'):
                    ui.label('Worst performer').classes('text-gray-400 text-sm')
                    ui.label(worst[0]).classes('text-xl font-bold')
                    color = 'text-green-400' if worst[1] >= 0 else 'text-red-400'
                    sign = '+' if worst[1] >= 0 else ''
                    ui.label(f'{sign}{worst[1]:.1f}%').classes(color)
        
        # Main comparison chart
        series = []
        colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#fc8452', '#9a60b4']
        
        for i, (ticker, values) in enumerate(data.normalized.items()):
            series.append({
                'name': ticker,
                'type': 'line',
                'data': values,
                'smooth': True,
                'showSymbol': False,
                'lineStyle': {'width': 2},
            })
        
        main_chart.options['backgroundColor'] = 'transparent'
        main_chart.options['color'] = colors
        main_chart.options['tooltip'] = {'trigger': 'axis'}
        main_chart.options['legend'] = {
            'data': list(data.normalized.keys()),
            'textStyle': {'color': '#999'},
            'top': 0,
            'left': 'center',
            'orient': 'horizontal',
        }
        main_chart.options['grid'] = {'left': 50, 'right': 20, 'top': 40, 'bottom': 60}
        # Show ~10 labels max
        label_interval = max(1, len(data.dates) // 10)
        main_chart.options['xAxis'] = {
            'type': 'category',
            'data': data.dates,
            'axisLine': {'lineStyle': {'color': '#333'}},
            'axisLabel': {'color': '#999', 'interval': label_interval, 'rotate': 45},
        }
        main_chart.options['yAxis'] = {
            'type': 'value',
            'axisLine': {'lineStyle': {'color': '#333'}},
            'axisLabel': {'color': '#999'},
            'splitLine': {'lineStyle': {'color': '#222'}},
        }
        main_chart.options['series'] = series
        main_chart.update()
        
        # Individual charts vs peer average
        individual_charts.clear()
        
        if len(data.normalized) > 1:
            # Calculate peer average
            all_values = list(data.normalized.values())
            min_len = min(len(v) for v in all_values)
            peer_avg = []
            for i in range(min_len):
                avg = sum(v[i] for v in all_values) / len(all_values)
                peer_avg.append(avg)
            
            with individual_charts:
                for ticker, values in list(data.normalized.items())[:4]:  # Show first 4
                    with ui.card().classes('w-60'):
                        ui.label(f'{ticker} vs peer average').classes('text-sm font-semibold')
                        
                        # Calculate difference
                        diff = [values[i] - peer_avg[i] for i in range(min(len(values), len(peer_avg)))]
                        
                        chart = ui.echart({
                            'backgroundColor': 'transparent',
                            'grid': {'left': 30, 'right': 10, 'top': 20, 'bottom': 20},
                            'xAxis': {'type': 'category', 'show': False, 'data': list(range(len(diff)))},
                            'yAxis': {'type': 'value', 'axisLabel': {'color': '#666', 'fontSize': 10}, 'splitLine': {'lineStyle': {'color': '#222'}}},
                            'series': [{
                                'type': 'line',
                                'data': diff,
                                'smooth': True,
                                'showSymbol': False,
                                'lineStyle': {'color': '#5470c6'},
                                'areaStyle': {
                                    'color': {
                                        'type': 'linear',
                                        'x': 0, 'y': 0, 'x2': 0, 'y2': 1,
                                        'colorStops': [
                                            {'offset': 0, 'color': 'rgba(84, 112, 198, 0.5)'},
                                            {'offset': 1, 'color': 'rgba(84, 112, 198, 0.1)'},
                                        ]
                                    }
                                },
                            }]
                        }).classes('w-full h-32')
    
    async def toggle_ticker(ticker: str):
        """Toggle a ticker selection and reload data."""
        if ticker in data.selected_tickers:
            if len(data.selected_tickers) > 1:  # Keep at least one
                data.selected_tickers.remove(ticker)
        else:
            data.selected_tickers.append(ticker)
        await load_data()
    
    async def set_horizon(horizon: str):
        """Set time horizon and reload data."""
        data.time_horizon = horizon
        await load_data()
    
    # Initial load
    ui.timer(0.5, load_data, once=True)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(show=False, title='Stock Peer Analysis', dark=True)

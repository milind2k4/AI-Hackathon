# API Integration Guide

This guide explains how to modify the `Market` class to use real-time or historical market data instead of the synthetic random walk.

## Prerequisites

You will need a library to fetch market data. We recommend `yfinance` for free historical data.

```bash
pip install yfinance
```

## Modifying market.py

1.  **Import the library**:

    ```python
    import yfinance as yf
    ```

2.  **Create a RealMarket Class**:
    Replace or extend the existing `Market` class.

    ```python
    class RealMarket:
        def __init__(self, symbol="AAPL", start_date="2023-01-01", end_date="2023-12-31"):
            self.symbol = symbol
            # Fetch data once
            self.data = yf.download(symbol, start=start_date, end=end_date)
            self.prices = self.data['Close'].values
            self.current_step = 0
            self.price = self.prices[0]
            self.price_history = [self.price]

        def update_price(self):
            """
            Advances to the next historical price point.
            """
            self.current_step += 1
            if self.current_step < len(self.prices):
                self.price = self.prices[self.current_step]
            else:
                # Loop back or stay at last price
                self.price = self.prices[-1]

            self.price_history.append(self.price)
            return self.price

        def get_price(self):
            return self.price

        def calculate_cost(self, volume, is_buy):
            # Same slippage logic as before
            if volume <= 0:
                return self.price

            penalty_factor = 0.0001
            impact = penalty_factor * volume

            if is_buy:
                return self.price * (1 + impact)
            else:
                return self.price * (1 - impact)
    ```

3.  **Update simulation.py**:
    Change the instantiation in `run_simulation`:

    ```python
    # from market import Market
    from market import RealMarket # Assuming you added it to market.py

    def run_simulation(steps=1000):
        # market = Market(initial_price=100.0)
        market = RealMarket(symbol="BTC-USD", start_date="2023-01-01")

        # ... rest of the code
    ```

## Using Alpha Vantage (Real-Time)

For real-time data, you would need an API key.

```python
import requests

class LiveMarket:
    def __init__(self, api_key, symbol="IBM"):
        self.api_key = api_key
        self.symbol = symbol
        self.price = 100.0 # Fallback
        self.price_history = []

    def update_price(self):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={self.symbol}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        try:
            self.price = float(data['Global Quote']['05. price'])
        except:
            print("Error fetching price, using last known")

        self.price_history.append(self.price)
        return self.price
```

> [!NOTE]
> Real-time APIs often have rate limits. For a simulation loop that runs thousands of steps quickly, **Historical Data** is much better.

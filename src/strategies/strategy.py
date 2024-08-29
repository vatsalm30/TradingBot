import collections.abc as c
import pandas as pd
from dataclasses import dataclass

class Strategy:
    def __init__(self, symbol: str, buy: c.Callable, sell: c.Callable):
        """
        Initialize the breakout strategy with the trading symbol, data, and parameters.
        :param symbol: The trading symbol (e.g., 'BTC/USDT')
        :param buy: Function to use when buying
        :param sell: Function to use when selling
        """
        self.trades_queue: Trade = []
        self.symbol = symbol
        self.buy = buy
        self.sell = sell

    
    def generate_signals(self, data: pd.DataFrame):
        """
        Generate buy/sell signals based on the strategy.
        Should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def execute_trade(self, signal, amount, leverage = 1, trailing_loss = 0, stop_loss = 0, take_profit = 0):
        """
        Execute trade based on the signal generated.
        :param signal: The trading signal (0=buy, 1=sell, 2=none)
        """
        if signal == 0:
            print(f"Buying {self.symbol}")
        elif signal == 1:
            print(f"Selling {self.symbol}")
        else:
            print("No action taken")
            
@dataclass
class Trade:
    symbol: str
    amount: float
    order_type: str
    price: float
    market: bool = True
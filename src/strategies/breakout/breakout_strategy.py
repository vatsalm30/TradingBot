from typing import Dict
import pandas as pd
import collections.abc as c

from strategies.strategy import Strategy
import utils.indicators.moving_average as moving_average

class BreakoutStrategy(Strategy):
    def __init__(self, symbol: str, buy: c.Callable, sell: c.Callable):
        """
        Initialize the breakout strategy with the trading symbol, data, and parameters.
        :param symbol: The trading symbol (e.g., 'BTC/USDT')
        :param buy: Function to use when buying
        :param sell: Function to use when selling
        """
        super().__init__(symbol, buy, sell)
    
    def generate_signal(self, data: Dict[str, pd.DataFrame]):
        """
        Generate breakout buy/sell signals.
        :return: A list of buy/sell signals
        """
        twenty = moving_average.simple_moving_average(data["4h"], 20)
        fifty = moving_average.simple_moving_average(data["4h"], 50)

        if twenty > fifty:
            return 0
        if fifty > twenty:
            return 1
        return 2
        
from typing import Dict
import pandas as pd
import collections.abc as c
from datetime import datetime

from strategies.strategy import Strategy, Trade
import utils.indicators.moving_average as moving_average
from utils.indicators.average_true_range import average_true_range

class BreakoutStrategy(Strategy):
    def __init__(self, symbol: str, open_trade: c.Callable, close_trade: c.Callable, deployment_limit: float = .25):
        super().__init__(symbol, open_trade, close_trade, deployment_limit)
    
    def generate_trade(self, data: Dict[str, pd.DataFrame]):
        twenty_sma = moving_average.simple_moving_average(data["5m"].tail(20), 20)
        fifty_sma = moving_average.simple_moving_average(data["5m"].tail(50), 50)

        twenty = twenty_sma.iloc[-1]
        fifty = fifty_sma.iloc[-1]

        amount = self.balance * self.deployment_limit / data["5m"]["close"].iloc[-1]

        buy = twenty > fifty
        sell = fifty > twenty

        if self.current_trade is not None:
            if (self.current_trade.order_type == "sell" and buy) or (self.current_trade.order_type == "buy" and sell):
                self.current_trade.active = False
                self.current_trade.exit_timestamp = datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S')
                self.current_trade.close_price = data["5m"]["close"].iloc[-1]
                self.close_trade(self.current_trade)
                self.current_trade = None
                return
        if self.current_trade is None:
            if buy:
                stop_loss = data["30m"]["low"].iloc[-1] - average_true_range(data["30m"].tail(14), 14).iloc[-1] * 2
                take_profit = data["30m"]["high"].iloc[-1] + average_true_range(data["30m"].tail(14), 14).iloc[-1]* 2
                self.current_trade = Trade(amount, "buy", data["5m"]["close"].iloc[-1], None, datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S'), None, active=False, stoploss=0, takeprofit=0, trailing_stoploss=0)
                return

            if sell:
                stop_loss = data["30m"]["high"].iloc[-1] + average_true_range(data["30m"].tail(14), 14).iloc[-1] * 2
                take_profit = data["30m"]["low"].iloc[-1] - average_true_range(data["30m"].tail(14), 14).iloc[-1] * 2
                self.current_trade = Trade(amount, "sell", data["5m"]["close"].iloc[-1], None, datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S'), None, active=False, stoploss=0, takeprofit=0, trailing_stoploss=0)
                return
        
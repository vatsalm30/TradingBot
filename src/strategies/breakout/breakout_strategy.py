from typing import Dict
import pandas as pd
import collections.abc as c
from datetime import datetime

from strategies.strategy import Strategy, Trade
import utils.indicators.moving_average as moving_average
from utils.indicators.average_true_range import average_true_range

class BreakoutStrategy(Strategy):
    def __init__(self, symbol: str, open_trade: c.Callable, close_trade: c.Callable, start_balance: float):
        self.pos_type = ""
        super().__init__(symbol, open_trade, close_trade, start_balance)
    
    def generate_trade(self, data: Dict[str, pd.DataFrame]):

        twenty_sma = moving_average.simple_moving_average(data["5m"].tail(20), 20)
        fifty_sma = moving_average.simple_moving_average(data["5m"].tail(50), 50)

        twenty = twenty_sma.iloc[-1]
        fifty = fifty_sma.iloc[-1]

        if self.current_trade is not None:
            if (self.current_trade.order_type == "sell" and twenty > fifty) or (self.current_trade.order_type == "buy" and fifty > twenty):
                self.current_trade.active = False
                self.close_trade(self.current_trade)
                self.current_trade.exit_timestamp = datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S')
                self.current_trade.close_price = data["5m"]["close"].iloc[-1]
                self.current_trade = None
                return
        if self.current_trade is None:
            if twenty > fifty:
                stop_loss = data["5m"]["low"].iloc[-1] - average_true_range(data["5m"].tail(14), 14).iloc[-1] * 2
                take_profit = data["5m"]["high"].iloc[-1] + average_true_range(data["5m"].tail(14), 14).iloc[-1]* 2
                self.current_trade = Trade(1, "buy", data["5m"]["close"].iloc[-1], None, datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S'), None, active=False, stoploss=stop_loss, takeprofit=take_profit)
                return

            if fifty > twenty:
                stop_loss = data["5m"]["high"].iloc[-1] + average_true_range(data["5m"].tail(14), 14).iloc[-1] * 2
                take_profit = data["5m"]["low"].iloc[-1] - average_true_range(data["5m"].tail(14), 14).iloc[-1] * 2
                self.current_trade = Trade(1, "sell", data["5m"]["close"].iloc[-1], None, datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S'), None, active=False, stoploss=stop_loss, takeprofit=take_profit)
                return
        
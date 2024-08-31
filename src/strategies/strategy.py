import collections.abc as c
from datetime import datetime
from typing import Dict
import pandas as pd
from dataclasses import dataclass

class Strategy:
    def __init__(self, symbol: str, open_trade: c.Callable, close_trade: c.Callable, start_balance: float):
        self.symbol = symbol
        self.open_trade = open_trade
        self.close_trade = close_trade
        self.start_balance = start_balance
        self.current_trade = None

    
    def generate_trade(self, data: Dict[str, pd.DataFrame]):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def execute_trade(self, data: Dict[str, pd.DataFrame]):
        if self.current_trade is None:
            return
        if self.current_trade.active == False:
            self.current_trade.active = True
            self.open_trade(self.current_trade)
            return
        if self.current_trade.trailing_stoploss > 0:
            # Trailing stoploss not implemented yet
            pass
        if self.current_trade.stoploss > 0:
            if self.current_trade.order_type == "buy":
                if data["5m"]["low"].iloc[-1] < self.current_trade.stoploss:
                    self.current_trade.active = False
                    self.current_trade.exit_timestamp = datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S')
                    self.current_trade.close_price = self.current_trade.stoploss
                    self.close_trade(self.current_trade)
                    self.current_trade = None
                    return
                    
            if self.current_trade.order_type == "sell":
                if data["5m"]["high"].iloc[-1] > self.current_trade.stoploss:
                    self.current_trade.active = False
                    self.current_trade.exit_timestamp = datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S')
                    self.current_trade.close_price = self.current_trade.stoploss
                    self.close_trade(self.current_trade)
                    self.current_trade = None
                    return

        if self.current_trade.takeprofit > 0:
            if self.current_trade.order_type == "buy":
                if data["5m"]["high"].iloc[-1] > self.current_trade.takeprofit:
                    self.current_trade.active = False
                    self.current_trade.exit_timestamp = datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S')
                    self.current_trade.close_price = self.current_trade.takeprofit
                    self.close_trade(self.current_trade)
                    self.current_trade = None
                    return

            if self.current_trade.order_type == "sell":
                if data["5m"]["low"].iloc[-1] < self.current_trade.takeprofit:
                    self.current_trade.active = False
                    self.current_trade.exit_timestamp = datetime.strptime(data["5m"]["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S')
                    self.current_trade.close_price = self.current_trade.takeprofit
                    self.close_trade(self.current_trade)
                    self.current_trade = None
                    return
            
@dataclass
class Trade:
    amount: float
    order_type: str
    open_price: float
    close_price: float
    entry_timestamp: int
    exit_timestamp: int
    active: bool
    stoploss: float = 0
    takeprofit: float = 0
    trailing_stoploss: float = 0
    leverage: int = 1

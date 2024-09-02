import collections.abc as c
from datetime import datetime
import math
from typing import Dict
import pandas as pd
from dataclasses import dataclass

class Strategy:
    def __init__(self, symbol: str, open_trade: c.Callable, close_trade: c.Callable, deployment_limit: float = .25):
        self.symbol = symbol
        self.open_trade = open_trade
        self.close_trade = close_trade
        self.deployment_limit = deployment_limit
        self.deployed = 0
        self.current_trade = None
        self.balance = 0

    
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
            if self.current_trade.order_type == "buy":
                self.current_trade.stoploss = max(self.current_trade.stoploss, data["5m"]["high"].iloc[-1] - self.current_trade.trailing_stoploss)

            if self.current_trade.order_type == "sell":
                self.current_trade.stoploss = min(self.current_trade.stoploss if self.current_trade.stoploss > 0 else math.inf, data["5m"]["high"].iloc[-1] + self.current_trade.trailing_stoploss)

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

from datetime import datetime
from typing import Dict
import collections.abc as c
import pandas as pd
import numpy as np

from strategies.strategy import Strategy, Trade
from utils.indicators.average_true_range import average_true_range
from utils.patterns.PIPPatternMiner import PIPPatternMiner
from utils.patterns.pips import find_pips

pd.options.mode.chained_assignment = None

class NovelPatternsStrategy(Strategy):
    def __init__(self, symbol: str, open_trade: c.Callable, close_trade: c.Callable, training_data: pd.DataFrame, deployment_limit: float = .25):
        
        self.pattern_miner = PIPPatternMiner(n_pips=5, lookback=24, hold_period=6)

        training_data['date'] = training_data['timestamp'].astype('datetime64[s]')
        training_data = training_data.set_index('date')
        training_data = np.log(training_data[["open", "high", "low", "close"]])
        training_data = training_data["close"].to_numpy()

        self.pattern_miner.train(training_data)

        print("Trained!")

        super().__init__(symbol, open_trade, close_trade, deployment_limit)

    def generate_trade(self, data: Dict[str, pd.DataFrame]):
        if data["5m"]["timestamp"].iloc[-1] != data["30m"]["timestamp"].iloc[-1]:
            # print(data["5m"]["timestamp"].iloc[-1], data["30m"]["timestamp"].iloc[-1])
            # print()
            return
        data = data["30m"]
        data['date'] = data['timestamp'].astype('datetime64[s]')
        data = data.set_index('date')
        logged_data = np.log(data[["open", "high", "low", "close"]])

        x = logged_data["close"].to_numpy()[-24:]

        _, pips_y = find_pips(x, 5, 3)

        pred, _, confidence = self.pattern_miner.predict(pips_y)

        buy = pred == 1 
        sell = pred == -1

        amount = self.balance * self.deployment_limit / data["close"].iloc[-1]

        if self.current_trade is not None:
            if (self.current_trade.order_type == "sell" and buy) or (self.current_trade.order_type == "buy" and sell):
                self.current_trade.active = False
                self.current_trade.exit_timestamp = datetime.strptime(data["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S')
                self.current_trade.close_price = data["close"].iloc[-1]
                self.close_trade(self.current_trade)
                self.current_trade = None
                return
        if self.current_trade is None:
            if buy:
                self.current_trade = Trade(amount, "buy", data["close"].iloc[-1], None, datetime.strptime(data["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S'), None, active=False, stoploss=0, takeprofit=0, trailing_stoploss=average_true_range(data.tail(14), 14).iloc[-1]* 2)
                return

            if sell:
                self.current_trade = Trade(amount, "sell", data["close"].iloc[-1], None, datetime.strptime(data["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S'), None, active=False, stoploss=0, takeprofit=0, trailing_stoploss=average_true_range(data.tail(14), 14).iloc[-1]* 2)
                return
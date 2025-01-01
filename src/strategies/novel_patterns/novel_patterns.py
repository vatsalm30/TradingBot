from datetime import datetime
import json
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
    def __init__(self, symbol: str, open_trade: c.Callable, close_trade: c.Callable, training_data: pd.DataFrame, deployment_limit: float = .25, load_data: bool = False, save_data: bool = False):
        
        self.pattern_miner = PIPPatternMiner(n_pips=5, lookback=24, hold_period=6)
        training_data['date'] = training_data['timestamp'].astype('datetime64[s]')
        training_data = training_data.set_index('date')
        training_data = np.log(training_data[["open", "high", "low", "close"]])
        training_data = training_data["close"].to_numpy()

        if not load_data:
            self.pattern_miner.train(training_data)
            print("Trained!")

            if save_data:
                with open('src/strategies/novel_patterns/patterns_5m.json', 'w') as file:
                    print(np.array(self.pattern_miner._selected_long).tolist())
                    patterns = {
                        "_n_pips": self.pattern_miner._n_pips,
                        "_lookback": self.pattern_miner._lookback,
                        "_hold_period": self.pattern_miner._hold_period,
                        "_unique_pip_patterns": self.pattern_miner._unique_pip_patterns,
                        "_unique_pip_indices": self.pattern_miner._unique_pip_indices,
                        "_cluster_centers": self.pattern_miner._cluster_centers,
                        "_pip_clusters": self.pattern_miner._pip_clusters,
                        "selected_long": np.array(self.pattern_miner._selected_long).tolist(),
                        "selected_short": np.array(self.pattern_miner._selected_short).tolist(),
                    }
                    json.dump(patterns, file)
        else:
            with open('src/strategies/novel_patterns/patterns_5m_newlymined.json', 'r') as file:
                patterns = json.load(file)
                self.pattern_miner._n_pips = patterns["_n_pips"]
                self.pattern_miner._lookback = patterns["_lookback"]
                self.pattern_miner._hold_period = patterns["_hold_period"]
                self.pattern_miner._unique_pip_patterns = patterns["_unique_pip_patterns"]
                self.pattern_miner._unique_pip_indices = patterns["_unique_pip_indices"]
                self.pattern_miner._cluster_centers = patterns["_cluster_centers"]
                self.pattern_miner._pip_clusters = patterns["_pip_clusters"]
                self.pattern_miner._selected_long = patterns["selected_long"]
                self.pattern_miner._selected_short = patterns["selected_short"]
                

        super().__init__(symbol, open_trade, close_trade, deployment_limit)

    def generate_trade(self, data: Dict[str, pd.DataFrame]):
        if data["5m"]["timestamp"].iloc[-1] != data["5m"]["timestamp"].iloc[-1]:
            # print(data["5m"]["timestamp"].iloc[-1], data["30m"]["timestamp"].iloc[-1])
            # print()
            return
        data = data["5m"]
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
                hard_stop_loss = data["close"].iloc[-1] * 0.998 * 0
                hard_takeprofit = data["close"].iloc[-1] * 1.01 * 0
                self.current_trade = Trade(amount, "buy", data["close"].iloc[-1], None, datetime.strptime(data["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S'), None, active=False, stoploss=hard_stop_loss, takeprofit=hard_takeprofit, trailing_stoploss=average_true_range(data.tail(14), 14).iloc[-1]* 2 * 0)
                return

            if sell:
                hard_stop_loss = data["close"].iloc[-1] * 1.002 * 0
                hard_takeprofit = data["close"].iloc[-1] * 0.99 * 0
                self.current_trade = Trade(amount, "sell", data["close"].iloc[-1], None, datetime.strptime(data["timestamp"].iloc[-1], '%Y-%m-%d %H:%M:%S'), None, active=False, stoploss=hard_stop_loss, takeprofit=hard_takeprofit, trailing_stoploss=average_true_range(data.tail(14), 14).iloc[-1]* 2 * 0)
                return
from typing import Dict
import pandas as pd
from strategies.strategy import Strategy, Trade

class Backtester:
    def __init__(self, strategy: Strategy, backTestData: Dict[str, pd.DataFrame], data_window: int = 100, starting_balance = 10_000):
        '''
            data_window: in days
        '''

        self.strategy = strategy
        self.backTestData = backTestData
        self.data_window = data_window * 288 # translated to 5 minute intervals

        self.trade_history = []

        self.strategy.open_trade = self.open_trade
        self.strategy.close_trade = self.close_trade
        self.strategy.balance = starting_balance
    
    def open_trade(self, trade: Trade):
        self.trade_history.append(trade)

    def close_trade(self, trade: Trade):
        self.strategy.balance += (trade.close_price - trade.open_price) * trade.amount if trade.order_type == 'buy' else (trade.open_price - trade.close_price) * trade.amount
        self.trade_history.append(trade)

    def run_test(self):
        start_index = 0

        while start_index+self.data_window < len(self.backTestData['5m']):
            input_data = {
                "1d": self.backTestData['1d'].iloc[start_index // 288: (start_index+self.data_window) // 288 if (start_index+self.data_window) // 288 < len(self.backTestData['1d']) else len(self.backTestData['1d']) - 1],
                "4h": self.backTestData['4h'].iloc[start_index // 48: (start_index+self.data_window) // 48 if (start_index+self.data_window) // 48 < len(self.backTestData['4h']) else len(self.backTestData['4h']) - 1],
                "1h": self.backTestData['1h'].iloc[start_index // 12: (start_index+self.data_window) // 12 if (start_index+self.data_window) // 12 < len(self.backTestData['1h']) else len(self.backTestData['1h']) - 1],
                "30m": self.backTestData['30m'].iloc[start_index // 6: (start_index+self.data_window) // 6 if (start_index+self.data_window) // 6 < len(self.backTestData['30m']) else len(self.backTestData['30m']) - 1],
                "5m": self.backTestData['5m'].iloc[start_index: start_index+self.data_window if start_index+self.data_window < len(self.backTestData['5m']) else len(self.backTestData['5m']) - 1],
            }
            self.strategy.generate_trade(input_data)
            self.strategy.execute_trade(input_data)
            start_index += 1
            if start_index % 10000 == 0:
                print(f"Index: {start_index}")
                print(self.strategy.balance)

    def get_results(self):
        return BacktestResult(self.trade_history)
    
    def display_test(self):
        return self.trade_history

class BacktestResult:
    def __init__(self, trade_history):
        self.trade_history = trade_history

    def calculate_statistics(self):
        pass

    def display_test(self):
        pass


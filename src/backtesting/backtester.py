from typing import Dict
import pandas as pd
from strategies.strategy import Strategy, Trade
import finplot as fplt

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
                "1d": self.backTestData['1d'].iloc[start_index // 288: (start_index+self.data_window) // 288 + 1 if (start_index+self.data_window) // 288 < len(self.backTestData['1d']) else (len(self.backTestData['1d']) - 1)],
                "4h": self.backTestData['4h'].iloc[start_index // 48: (start_index+self.data_window) // 48 + 1 if (start_index+self.data_window) // 48 < len(self.backTestData['4h']) else (len(self.backTestData['4h']) - 1)],
                "1h": self.backTestData['1h'].iloc[start_index // 12: (start_index+self.data_window) // 12 + 1 if (start_index+self.data_window) // 12 < len(self.backTestData['1h']) else (len(self.backTestData['1h']) - 1)],
                "30m": self.backTestData['30m'].iloc[start_index // 6: (start_index+self.data_window) // 6 + 1 if (start_index+self.data_window) // 6 < len(self.backTestData['30m']) else (len(self.backTestData['30m']) - 1)],
                "5m": self.backTestData['5m'].iloc[start_index: start_index+self.data_window if start_index+self.data_window < len(self.backTestData['5m']) else (len(self.backTestData['5m']) - 1)],
            }
            self.strategy.generate_trade(input_data)
            self.strategy.execute_trade(input_data)
            start_index += 1
            if start_index % 10000 == 0:
                print(f"Index: {start_index}")
                print(self.strategy.balance)

    def return_backtest_result(self):
        last_trade = ""

        max_loss = 0
        max_profit = 0

        winning_trades = 0
        losing_trades = 0

        loss_percent = 0
        gain_percent = 0

        for trade in self.trade_history:
            if trade.active:
                continue

            open_price = trade.open_price
            close_price = trade.close_price
            change = (close_price - open_price) / open_price

            if last_trade == 'buy':
                # balance += balance * change

                if change < max_loss:
                    max_loss = change
                if change > max_profit:
                    max_profit = change

                if change > 0:
                    winning_trades += 1
                    gain_percent += change
                else:
                    losing_trades += 1
                    loss_percent -= change

            else:
                # balance -= balance * change

                if change < max_loss:
                    max_loss = change
                if change > max_profit:
                    max_profit = change

                if change < 0:
                    winning_trades += 1
                    gain_percent -= change
                else:
                    losing_trades += 1
                    loss_percent += change

        return (self.strategy.balance, max_loss, max_profit, winning_trades, losing_trades, loss_percent, gain_percent)
    
    def plot_backtest_result(self):
        pass
from typing import Dict
import numpy as np
import pandas as pd
from strategies.strategy import Strategy, Trade
import finplot as fplt
from utils.indicators import average_directional_index, moving_average, relative_strength_index, average_true_range
from utils.patterns.lines import trend_line

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

        self.input_data = {}
        self.trades_df = pd.DataFrame()
    
    def open_trade(self, trade: Trade):
        self.trade_history.append(trade)

    def close_trade(self, trade: Trade):
        self.strategy.balance += (trade.close_price - trade.open_price) * trade.amount if trade.order_type == 'buy' else (trade.open_price - trade.close_price) * trade.amount
        self.trade_history.append(trade)

        # Add one for each time frame testing out 5m for now
        adx = average_directional_index.adx(self.input_data['5m'])
        rsi = relative_strength_index.rsi(self.input_data['5m'])
        ema_24 = moving_average.exponential_moving_average(self.input_data['5m'], 24)
        ema_100 = moving_average.exponential_moving_average(self.input_data['5m'], 100)

        # support_resistance_distance = average_directional_index.adx(self.input_data['5m'])

        trendline_slope = trend_line.fit_trendlines_single(self.input_data['5m']["close"].to_numpy())
        ema50_slope = moving_average.moving_average_slope(self.input_data['5m'], 50, moving_average_function=moving_average.exponential_moving_average)
        atr = average_true_range.average_true_range(self.input_data['5m'], 14)

        self.save_trade_with_labels(trade, adx, rsi, ema_24, ema_100, trendline_slope, ema50_slope, atr)

    def run_test(self):
        start_index = 0

        while start_index+self.data_window < len(self.backTestData['5m']):
            self.input_data = {
                "1d": self.backTestData['1d'].iloc[start_index // 288: (start_index+self.data_window) // 288 + 1 if (start_index+self.data_window) // 288 < len(self.backTestData['1d']) else (len(self.backTestData['1d']) - 1)],
                "4h": self.backTestData['4h'].iloc[start_index // 48: (start_index+self.data_window) // 48 + 1 if (start_index+self.data_window) // 48 < len(self.backTestData['4h']) else (len(self.backTestData['4h']) - 1)],
                "1h": self.backTestData['1h'].iloc[start_index // 12: (start_index+self.data_window) // 12 + 1 if (start_index+self.data_window) // 12 < len(self.backTestData['1h']) else (len(self.backTestData['1h']) - 1)],
                "30m": self.backTestData['30m'].iloc[start_index // 6: (start_index+self.data_window) // 6 + 1 if (start_index+self.data_window) // 6 < len(self.backTestData['30m']) else (len(self.backTestData['30m']) - 1)],
                "5m": self.backTestData['5m'].iloc[start_index: start_index+self.data_window if start_index+self.data_window < len(self.backTestData['5m']) else (len(self.backTestData['5m']) - 1)],
            }
            self.strategy.generate_trade(self.input_data)
            self.strategy.execute_trade(self.input_data)
            start_index += 1
            if start_index % 10000 == 0:
                print(f"Index: {start_index}")
                print(self.strategy.balance)

        self.trades_df.to_csv("trades.csv", encoding='utf-8', index=False)


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
    
    def save_trade_with_labels(self, trade: Trade, adx, rsi, ema_24, ema_100, trendline_slope, ema50_slope, atr):
        
        '''
        print("ADX: " + str(adx.iloc[-1]))
        print("RSI: " + str(rsi.iloc[-1]))
        print("EMA 24: " + str(ema_24.iloc[-1]))
        print("EMA 100: " + str(ema_100.iloc[-1]))
        print("Support Slope: " + str(trendline_slope[0][0]))
        print("Resistance Slope: " + str(trendline_slope[1][0]))
        print("EMA 50 Slope: " + str(ema50_slope.iloc[-1]))
        print("ATR: " + str(atr.iloc[-1]))
        '''

        new_row = pd.DataFrame({
            "price": trade.open_price,
            "order_type": trade.order_type,
            "amount": trade.amount,
            "adx": adx.iloc[-1],
            "rsi": rsi.iloc[-1],
            "ema_24_100_diff": ema_24.iloc[-1] - ema_100.iloc[-1],
            "support_trendline_slope": trendline_slope[0][0],
            "resist_trendline_slope": trendline_slope[1][0],
            "ema50_slope": ema50_slope.iloc[-1],
            "atr": atr.iloc[-1]
        }, index=[0])

        self.trades_df = pd.concat([self.trades_df, new_row], ignore_index=True)

        # self.trade_history.append(trade)

    def plot_backtest_result(self):
        pass
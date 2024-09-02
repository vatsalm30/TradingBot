# from secret import secrets
# import ccxt

# exchange = ccxt.binance(
# {
#     'options': {
#         'adjustForTimeDifference': True,
#         'defaultType': 'future',
#     },
#     'apiKey': secrets["apiKey"],
#     'secret': secrets["secret"],
#     'enableRateLimit': True,
# })

# exchange.set_sandbox_mode(True)

# from typing import List
# from strategies.breakout.breakout_strategy import BreakoutStrategy
# from backtesting.backtester import Backtester
# import pandas as pd

# from strategies.strategy import Trade

# strat = BreakoutStrategy("BTC/USDT", None, None, 1)

# data = {
#     "1d": pd.read_csv("src/data/ETHUSDT/1d.csv"),
#     "4h": pd.read_csv("src/data/ETHUSDT/4h.csv"),
#     "1h": pd.read_csv("src/data/ETHUSDT/1h.csv"),
#     "30m": pd.read_csv("src/data/ETHUSDT/30m.csv"),
#     "5m": pd.read_csv("src/data/ETHUSDT/5m.csv"),
# }


# tester = Backtester(strat, data, 100)

# tester.run_test()

# def calc_profit(test_res: List[Trade]):
#     last_trade = ""
#     last_trade_price = 0
#     balance = 10_000

#     max_loss = 0
#     max_profit = 0

#     winning_trades = 0
#     losing_trades = 0

#     loss_percent = 0
#     gain_percent = 0

#     for trade in test_res:
#         if trade.active:
#             continue

#         open_price = trade.open_price
#         close_price = trade.close_price
#         change = (close_price - open_price) / open_price

#         if last_trade == 'buy':
#             # balance += balance * change

#             if change < max_loss:
#                 max_loss = change
#             if change > max_profit:
#                 max_profit = change

#             if change > 0:
#                 winning_trades += 1
#                 gain_percent += change
#             else:
#                 losing_trades += 1
#                 loss_percent -= change

#         else:
#             # balance -= balance * change

#             if change < max_loss:
#                 max_loss = change
#             if change > max_profit:
#                 max_profit = change

#             if change < 0:
#                 winning_trades += 1
#                 gain_percent -= change
#             else:
#                 losing_trades += 1
#                 loss_percent += change

#     return (balance, max_loss, max_profit, winning_trades, losing_trades, loss_percent, gain_percent)


# res = tester.display_test()
# # print(res)
# print(len(res))
# stats = calc_profit(res)
# print("Ending Balance:" + str(tester.strategy.balance))
# print("Max Loss:" + str(stats[1]))
# print("Max Profit:" + str(stats[2]))
# print("Winrate: " + str((stats[3] / (stats[3] + stats[4])) * 100) + "%")
# print("Average Gain: " + str(stats[6]))
# print("Average Loss: " + str(stats[5]))

import math
import pandas as pd
import numpy as np
from utils.patterns.rolling_window import plot_rolling_window
from utils.patterns.directional_change import plot_directional_change
from utils.patterns.pips import plot_pips, find_pips
from utils.patterns.PIPPatternMiner import PIPPatternMiner
import matplotlib.pyplot as plt
import finplot as fplt
from sklearn.preprocessing import MinMaxScaler

data = {
    "1d": pd.read_csv("src/data/ETHUSDT/1d.csv"),
    "4h": pd.read_csv("src/data/ETHUSDT/4h.csv"),
    "1h": pd.read_csv("src/data/ETHUSDT/1h.csv"),
    "30m": pd.read_csv("src/data/ETHUSDT/30m.csv"),
    "5m": pd.read_csv("src/data/ETHUSDT/5m.csv"),
}

data = data["1h"]
data['date'] = data['timestamp'].astype('datetime64[s]')
data = data.set_index('date')

fplt.candlestick_ochl(data[['open','close','high','low']])


data = np.log(data[["open", "high", "low", "close"]])

arr = data[data.index < '01-01-2024']['close'].to_numpy()
pip_miner = PIPPatternMiner(n_pips=5, lookback=24, hold_period=6)

pip_miner.train(arr, n_reps=-1)
# pip_miner.run_test(arr)

candles = data
candles["date"] = candles.index

pip_miner.show_cluster(0, candles.iloc[-5760:])

fplt.show()

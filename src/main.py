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

import pandas as pd
import numpy as np
from strategies.novel_patterns.novel_patterns import NovelPatternsStrategy
from backtesting.backtester import Backtester
from utils.patterns.lines.trend_line import fit_trendlines_single
from utils.patterns.lines.trendline_breakout import trendline_breakout
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from utils.meta_labeling.Labeling import Labeler
from strategies.novel_patterns_labaled.novel_patterns_labaled import NovelPatternsLabaledStrategy



data = {
    "1d": pd.read_csv("src/data/ETHUSDT/1d.csv"),
    "4h": pd.read_csv("src/data/ETHUSDT/4h.csv"),
    "1h": pd.read_csv("src/data/ETHUSDT/1h.csv"),
    "30m": pd.read_csv("src/data/ETHUSDT/30m.csv"),
    "5m": pd.read_csv("src/data/ETHUSDT/5m.csv"),
}

data["1d"]["date"] = data["1d"]["timestamp"].astype('datetime64[s]')
data["4h"]["date"] = data["4h"]["timestamp"].astype('datetime64[s]')
data["1h"]["date"] = data["1h"]["timestamp"].astype('datetime64[s]')
data["30m"]["date"] = data["30m"]["timestamp"].astype('datetime64[s]')
data["5m"]["date"] = data["5m"]["timestamp"].astype('datetime64[s]')

data["1d"] = data["1d"].set_index('date')
data["4h"] = data["4h"].set_index('date')
data["1h"] = data["1h"].set_index('date')
data["30m"] = data["30m"].set_index('date')
data["5m"] = data["5m"].set_index('date')

train_data = {}

train_data["1d"] = data["1d"][data["1d"].index < '2024-01-01']
train_data["4h"] = data["4h"][data["4h"].index < '2024-01-01']
train_data["1h"] = data["1h"][data["1h"].index < '2024-01-01']
train_data["30m"] = data["30m"][data["30m"].index < '2024-01-01']
train_data["5m"] = data["5m"][data["5m"].index < '2024-01-01']

test_data = {}

test_data["1d"] = data["1d"][data["1d"].index >= '2024-01-01']
test_data["4h"] = data["4h"][data["4h"].index >= '2024-01-01']
test_data["1h"] = data["1h"][data["1h"].index >= '2024-01-01']
test_data["30m"] = data["30m"][data["30m"].index >= '2024-01-01']
test_data["5m"] = data["5m"][data["5m"].index >= '2024-01-01']

training_strategy = NovelPatternsStrategy("ETHUSDT", None, None, pd.read_csv("src/data/ETHUSDT/1h.csv"), 1, True, False)


labeler = Labeler(training_strategy, None, "src/data/models/randomforest5m/", train_data)

strategy = NovelPatternsLabaledStrategy("ETHUSDT", None, None, pd.read_csv("src/data/ETHUSDT/1h.csv"), 1, True, False)
backtester = Backtester(strategy, test_data, 100, 10_000)

backtester.run_test()

results = backtester.return_backtest_result()

print("Balance: ", results[0])
print("Max Loss: ", results[1])
print("Max Profit: ", results[2])
print("Winning Trades: ", results[3])
print("Losing Trades: ", results[4])
print("Loss Percent: ", results[5])
print("Gain Percent: ", results[6])

with open("src/trades.json", "w") as f:
    f.write(backtester.trades_df)

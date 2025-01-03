import pandas as pd
import numpy as np
from strategies.novel_patterns.novel_patterns import NovelPatternsStrategy
from backtesting.backtester import Backtester
from utils.patterns.lines.trend_line import fit_trendlines_single
from utils.patterns.lines.trendline_breakout import trendline_breakout
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from utils.meta_labeling.Labeling import Labeler
from strategies.novel_patterns_labeled.novel_patterns_labeled import NovelPatternsLabeledStrategy



data = {
    "1d": pd.read_csv("src/data/ETHUSDT/1d.csv", on_bad_lines='skip'),
    "4h": pd.read_csv("src/data/ETHUSDT/4h.csv", on_bad_lines='skip'),
    "1h": pd.read_csv("src/data/ETHUSDT/1h.csv", on_bad_lines='skip'),
    "30m": pd.read_csv("src/data/ETHUSDT/30m.csv", on_bad_lines='skip'),
    "5m": pd.read_csv("src/data/ETHUSDT/5m.csv", on_bad_lines='skip'),
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

training_strategy = NovelPatternsStrategy("ETHUSDT", None, None, pd.read_csv("src/data/ETHUSDT/5m.csv"), 1, False, True)

labeler = Labeler(training_strategy, None, "src/data/models/randomforest5m/", train_data)

strategy = NovelPatternsLabeledStrategy("ETHUSDT", None, None, pd.read_csv("src/data/ETHUSDT/1h.csv"), 1, True, False)
backtester = Backtester(strategy, data, 100, 10_000)

backtester.run_test()

results = backtester.return_backtest_result()

print("Balance: ", results[0])
print("Max Loss: ", results[1])
print("Max Profit: ", results[2])
print("Winning Trades: ", results[3])
print("Losing Trades: ", results[4])
print("Loss Percent: ", results[5])
print("Gain Percent: ", results[6])

backtester.trades_df.to_csv("src/trades.csv")

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

data = {
    "1d": pd.read_csv("src/data/ETHUSDT/1d.csv"),
    "4h": pd.read_csv("src/data/ETHUSDT/4h.csv"),
    "1h": pd.read_csv("src/data/ETHUSDT/1h.csv"),
    "30m": pd.read_csv("src/data/ETHUSDT/30m.csv"),
    "5m": pd.read_csv("src/data/ETHUSDT/5m.csv"),
}


strategy = NovelPatternsStrategy("ETHUSDT", None, None, data["1h"], 1, True, False)
backtester = Backtester(strategy, data)


backtester.run_test()

results = backtester.return_backtest_result()

# data = data["1d"]
# data['date'] = data['timestamp'].astype('datetime64[s]')
# data = data.set_index('date')

# data["close"] = np.log(data["close"])

# lookback = 30
# support_slope = [np.nan] * len(data)
# resist_slope = [np.nan] * len(data)
# for i in range(lookback - 1, len(data)):
#     support_coefs, resist_coefs =  fit_trendlines_single(data["close"].iloc[i - lookback + 1: i + 1].to_numpy())
#     support_slope[i] = support_coefs[0]
#     resist_slope[i] = resist_coefs[0]

# data['support_slope'] = support_slope
# data['resist_slope'] = resist_slope

# print(data)

# plt.style.use('dark_background')
# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot(np.exp(data["close"]), label='BTC-USDT', color='white')
# ax2.plot(data['support_slope'], label='Support Slope', color='green')
# ax2.plot(data['resist_slope'], label='Resistance Slope', color='red')
# plt.title("Trend Line Slopes ETH-USDT Hourly")
# plt.legend()
# plt.show()
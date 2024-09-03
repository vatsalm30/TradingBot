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

data = {
    "1d": pd.read_csv("src/data/ETHUSDT/1d.csv"),
    "4h": pd.read_csv("src/data/ETHUSDT/4h.csv"),
    "1h": pd.read_csv("src/data/ETHUSDT/1h.csv"),
    "30m": pd.read_csv("src/data/ETHUSDT/30m.csv"),
    "5m": pd.read_csv("src/data/ETHUSDT/5m.csv"),
}


strategy = NovelPatternsStrategy("ETHUSDT", None, None, data["1h"], 1)
backtester = Backtester(strategy, data)


backtester.run_test()

results = backtester.return_backtest_result()

print(results)
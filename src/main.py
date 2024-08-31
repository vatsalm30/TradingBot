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

from typing import List
from strategies.breakout.breakout_strategy import BreakoutStrategy
from backtesting.backtester import Backtester
import pandas as pd

from strategies.strategy import Trade

# def buy():
#     print("buy")
# def sell():
#     print("sell")

strat = BreakoutStrategy("BTC/USDT", None, None, 10000)

data = {
    "1d": pd.read_csv("src/data/ETHUSDT/1d.csv"),
    "4h": pd.read_csv("src/data/ETHUSDT/4h.csv"),
    "1h": pd.read_csv("src/data/ETHUSDT/1h.csv"),
    "30m": pd.read_csv("src/data/ETHUSDT/30m.csv"),
    "5m": pd.read_csv("src/data/ETHUSDT/5m.csv"),
}


tester = Backtester(strat, data, 100)

tester.run_test()

def calc_profit(test_res: List[Trade]):
    last_trade = ""
    last_trade_price = 0
    balance = 10_000

    max_loss = 0
    max_profit = 0

    winning_trades = 0
    losing_trades = 0

    for trade in test_res:
        if trade.active:
            continue

        open_price = trade.open_price
        close_price = trade.close_price
        change = (close_price - open_price) / open_price

        if last_trade == 'buy':
            balance += balance * change

            if change < max_loss:
                max_loss = change
            if change > max_profit:
                max_profit = change

            if change > 0:
                winning_trades += 1
            else:
                losing_trades += 1

        else:
            balance -= balance * change

            if change < max_loss:
                max_loss = change
            if change > max_profit:
                max_profit = change

            if change < 0:
                winning_trades += 1
            else:
                losing_trades += 1

    return (balance, max_loss, max_profit, winning_trades, losing_trades)


res = tester.display_test()
# print(res)
print(len(res))
stats = calc_profit(res)
print("Ending Balance:" + str(stats[0]))
print("Max Loss:" + str(stats[1]))
print("Max Profit:" + str(stats[2]))
print("Winrate: " + str((stats[3] / (stats[3] + stats[4])) * 100) + "%")
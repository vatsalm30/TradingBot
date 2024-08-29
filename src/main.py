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

from strategies.breakout.breakout_strategy import BreakoutStrategy
import pandas as pd

def buy():
    print("buy")
def sell():
    print("sell")

strat = BreakoutStrategy("BTC/USDT", buy, sell)

data = {
    "4h": pd.read_csv("src/data/ETHUSDT/4h.csv"),
}

print(strat.generate_signal(data))
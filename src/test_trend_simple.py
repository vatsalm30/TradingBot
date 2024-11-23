import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import mplfinance as mpf
from utils.patterns.lines.trendline_break_dataset import trendline_breakout_dataset
from utils.patterns.lines.trend_line import fit_trendlines_single
from sklearn.ensemble import RandomForestClassifier
import sklearn

def plot_trade(ohlc: pd.DataFrame, trades: pd.DataFrame, trade_i: int, lookback: int):

    plt.style.use('dark_background')

    trade = trades.iloc[trade_i]
    entry_i = int(trade['entry_i'])
    exit_i = int(trade['exit_i']) 
    
    candles = np.log(ohlc.iloc[entry_i - lookback:exit_i+1])
    resist = [(candles.index[0], trade['intercept']), (candles.index[lookback], trade['intercept'] + trade['slope'] * lookback)]
    tp = [(candles.index[lookback], trade['tp']), (candles.index[-1], trade['tp'])]
    sl = [(candles.index[lookback], trade['sl']), (candles.index[-1], trade['sl'])]

    mco = [None] * len(candles)
    mco[lookback] = 'blue'
    fig, axs = plt.subplots(2, sharex=True, height_ratios=[3, 1])
    axs[1].set_title('Volume')

    mpf.plot(candles, volume=axs[1], alines=dict(alines=[resist, tp, sl], colors=['w', 'b', 'r']), type='candle', style='charles', ax=axs[0], marketcolor_overrides=mco)
    plt.show()


data = pd.read_csv('src/data/ETHUSDT/1h.csv')
data['date'] = data['timestamp'].astype('datetime64[s]')
data = data.set_index('date')
data = data.dropna()
data = data[data.index < '2024-01-01']

plt.style.use('dark_background')

trades, data_x, data_y = trendline_breakout_dataset(data, 72)
trades.plot.scatter('return', 'vol')
plt.show()
trades.plot.scatter('return', 'atr')
plt.show()
trades.plot.scatter('return', 'slope')
plt.show()
trades.plot.scatter('return', 'resist_s')
plt.show()
trades.plot.scatter('return', 'adx')
plt.show()
trades.plot.scatter('return', 'max_dist')
plt.show()
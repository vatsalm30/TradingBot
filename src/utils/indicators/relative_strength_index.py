import pandas_ta as ta

def rsi(ohlcv, lookback=14):
    return ta.rsi(ohlcv['close'], lookback)
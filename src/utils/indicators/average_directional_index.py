import pandas_ta as ta

def adx(ohlcv, lookback=14):
    return ta.adx(ohlcv['high'], ohlcv['low'], ohlcv['close'], lookback)["ADX_14"]
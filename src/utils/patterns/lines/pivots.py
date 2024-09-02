import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

def calculate_pivot_points(df):
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values

    # Calculate Traditional Pivot Points
    pivot = (high + low + close) / 3
    r1 = 2 * pivot - low
    s1 = 2 * pivot - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    r3 = high + 2 * (pivot - low)
    s3 = low - 2 * (high - pivot)
    
    # Create DataFrame with pivot points
    pivot_df = pd.DataFrame({
        'Traditional_Pivot': pivot,
        'Traditional_R1': r1,
        'Traditional_S1': s1,
        'Traditional_R2': r2,
        'Traditional_S2': s2,
        'Traditional_R3': r3,
        'Traditional_S3': s3
    }, index=df.index)
    
    return pivot_df

def plot_candlestick_with_pivots(df, pivot_points):
    df = df.rename(columns={'timestamp': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})
    df.index = pd.DatetimeIndex(df['Date'])

    mpf.plot(df, type='candle', style='yahoo', title='Traditional Pivot Points', ylabel='Price', volume=True)

import pandas as pd

def average_true_range(data: pd.DataFrame, period: int):
    return data["high"].rolling(period).max() - data["low"].rolling(period).min()
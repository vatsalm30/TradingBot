import pandas as pd

def simple_moving_average(data: pd.DataFrame, period: int, source: str = "close"):
    return data[source].rolling(period).mean()

def exponential_moving_average(data: pd.DataFrame, period: int, source: str = "close"):
    return data[source].ewm(span=period, adjust=False).mean()
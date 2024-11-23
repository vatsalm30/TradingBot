import pandas as pd

def simple_moving_average(data: pd.DataFrame, period: int, source: str = "close"):
    return data[source].rolling(period).mean()

def exponential_moving_average(data: pd.DataFrame, period: int, source: str = "close"):
    return data[source].ewm(span=period, adjust=False).mean()

def moving_average_slope(data: pd.DataFrame, period: int, source: str = "close", moving_average_function = simple_moving_average):
    return moving_average_function(data, period, source).diff(1)
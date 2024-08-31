import pandas as pd

def simple_moving_average(data: pd.DataFrame, period: int, source: str = "close"):
    return data[source].rolling(period).mean()
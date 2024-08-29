import pandas as pd

def simple_moving_average(data: pd.DataFrame, period: int):
    return data.rolling(period).mean()
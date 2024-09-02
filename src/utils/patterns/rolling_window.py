from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def rolling_window_top(data: np.array, current_index: int, order: int):
    if current_index < order * 2 + 1:
        return False
    
    top = True
    k = current_index - order
    v = data[k]

    for i in range(order):
        if data[k + i] > v or data[k - 1] > v:
            top = False
            break
        
    return top

def rolling_window_bottom(data: np.array, current_index: int, order: int):
    if current_index < order * 2 + 1:
        return False
    
    bottom = True
    k = current_index - order
    v = data[k]

    for i in range(order):
        if data[k + i] < v or data[k - 1] < v:
            bottom = False
            break
        
    return bottom

def rolling_window_extremes(data: np.array, order: int):
    tops = []
    bottoms = []
    
    for i in range(len(data)):
        if rolling_window_top(data, i, order):
            top = [i, i - order, data[i - order]]
            tops.append(top)

        if rolling_window_bottom(data, i, order):
            bottom = [i, i - order, data[i - order]]
            bottoms.append(bottom)

    return tops, bottoms

def plot_rolling_window(data: pd.DataFrame):
    data['date'] = data['timestamp'].astype('datetime64[s]')
    data = data.set_index('date')

    tops, bottoms = rolling_window_extremes(data['close'].to_numpy(), 10)
    data['close'].plot()
    idx = data.index
    for top in tops:
        plt.plot(idx[top[1]], top[2], marker='o', color='green')

    for bottom in bottoms:
        plt.plot(idx[bottom[1]], bottom[2], marker='o', color='red')


    plt.show()
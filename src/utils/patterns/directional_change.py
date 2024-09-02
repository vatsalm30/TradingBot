import numpy as np
import finplot as fplt
import pandas as pd

def directional_change(close: np.array, high: np.array, low: np.array, sigma: float):
    up_zig = True
    tmp_max = high[0]
    tmp_min = low[0]
    tmp_max_i = 0
    tmp_min_i = 0

    tops = []
    bottoms = []

    for i in range(len(close)):
        if up_zig:
            if high[i] > tmp_max:
                tmp_max = high[i]
                tmp_max_i = i
            elif close[i] < tmp_max - tmp_max * sigma:
                top = [i, tmp_max_i, tmp_max]
                tops.append(top)

                up_zig = False
                tmp_min = low[i]
                tmp_min_i = i
        else:
            if low[i] < tmp_min:
                tmp_min = low[i]
                tmp_min_i = i
            elif close[i] > tmp_min - tmp_min * sigma:
                bottom = [i, tmp_min_i, tmp_min]
                bottoms.append(bottom)

                up_zig = True
                tmp_max = high[i]
                tmp_max_i = i

    return tops, bottoms

def plot_directional_change(data: pd.DataFrame):
    data['date'] = data['timestamp'].astype('datetime64[s]')
    data = data.set_index('date')

    tops, bottoms = directional_change(data['close'].to_numpy(), data['high'].to_numpy(), data['low'].to_numpy(), 0.02)

    ax = fplt.create_plot()
    fplt.candlestick_ochl(data[['open','close','high','low']])

    idx = data.index

    for top in tops:
        fplt.plot(idx[top[1]], top[2], color='#00ff00', style='o')

    for bottom in bottoms:
        fplt.plot(idx[bottom[1]], bottom[2], color='#ff0000', style='o')
    

    fplt.show()
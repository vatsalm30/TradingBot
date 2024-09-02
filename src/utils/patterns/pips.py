from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import finplot as fplt


def find_pips(data: np.array, n_pips: int, dist_measure: int):
    # dist_measure
    # 1 = Euclidean Distance
    # 2 = Perpindicular Distance
    # 3 = Vertical Distance

    pips_x = [0, len(data) - 1]  # Index
    pips_y = [data[0], data[-1]] # Price

    for curr_point in range(2, n_pips):

        md = 0.0 # Max distance
        md_i = -1 # Max distance index
        insert_index = -1

        for k in range(0, curr_point - 1):

            # Left adjacent, right adjacent indices
            left_adj = k
            right_adj = k + 1

            time_diff = pips_x[right_adj] - pips_x[left_adj]
            price_diff = pips_y[right_adj] - pips_y[left_adj]
            slope = price_diff / time_diff
            intercept = pips_y[left_adj] - pips_x[left_adj] * slope;

            for i in range(pips_x[left_adj] + 1, pips_x[right_adj]):
                
                d = 0.0 # Distance
                if dist_measure == 1: # Euclidean distance
                    d =  ( (pips_x[left_adj] - i) ** 2 + (pips_y[left_adj] - data[i]) ** 2 ) ** 0.5
                    d += ( (pips_x[right_adj] - i) ** 2 + (pips_y[right_adj] - data[i]) ** 2 ) ** 0.5
                elif dist_measure == 2: # Perpindicular distance
                    d = abs( (slope * i + intercept) - data[i] ) / (slope ** 2 + 1) ** 0.5
                else: # Vertical distance    
                    d = abs( (slope * i + intercept) - data[i] )

                if d > md:
                    md = d
                    md_i = i
                    insert_index = right_adj

        pips_x.insert(insert_index, md_i)
        pips_y.insert(insert_index, data[md_i])

    return pips_x, pips_y

def plot_pips(data: pd.DataFrame):
    data['date'] = data['timestamp'].astype('datetime64[s]')
    data = data.set_index('date')

    i = 300

    pips_len = 24

    fplt.candlestick_ochl(data[['open','close','high','low']].iloc[i-pips_len:i])

    x = data['close'].iloc[i-pips_len:i].to_numpy()
    pips_x, pips_y = find_pips(x, 5, 2)

    idx = data.iloc[i-pips_len:i].index

    fplt.plot(idx[pips_x], pips_y, color='#00ff00', style='o')


    for p in range(1, len(pips_x)):
        fplt.add_line((idx[pips_x[p]], pips_y[p]), (idx[pips_x[p - 1]], pips_y[p - 1]), color='#000000', width=2)

    print(pips_y)

    fplt.show()


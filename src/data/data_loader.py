import ccxt
import pandas as pd
import time

data_provider = ccxt.binance(
    {
        'enableRateLimit': True,
    }
)

symbol = 'ETH/USDT'  # Crypto pair
timeframe = '5m'  # Timeframe for candles

time_inc = 60 * 5 * 1000 * 1 * 500 # 5 minutes

since_time = 1483228800000

print(time.time())

df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

while since_time < time.time() * 1000:
    ohlcv = data_provider.fetch_ohlcv(symbol, timeframe, since=since_time, limit=500)
    df = pd.concat([df, pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])], ignore_index=True)
    since_time += time_inc

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.to_csv("src/data/ETHUSDT/5m.csv", sep=",", mode='a', header=False)
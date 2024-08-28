# Breakout Strategy

### 1. Identification of Dynamic Support and Resistance Levels
Instead of relying solely on static support and resistance levels, a sophisticated bot can dynamically calculate these levels using price action and technical indicators. Some methods to define support and resistance include:
- **Pivot Points:** automaticly detect where price switches direction --> used to find support and resistance
- **Trendlines and Channels:** Bot automatically detects trendlines using pivot points and linear regeression
- **Fibonacci Retracement/Extensions:** these levels are calculated using Fibonacci ratios (23.6%, 38.2%, 61.8%, etc.) based on previous price swings (high and low)

### 2. Chart Patterns for Breakout Detection
The bot will use pivot points and trendlines to figure out chart patterns which will allow it predict how the market may react in the future

**Key Patterns for Breakouts:**
- **Ascending/Descending Triangles**
- **Range trading:** bot finds one support and one resistance that price is unable to break and the price keeps on making pivot points arround the support and resistance points so the bot starts trading the swings
- **Head and Shoulders/Inversted Variant**
- **Double Tops/Bottoms:** bot checks where if there are ever a series of pivots in the same direction in the same vicinity to find double tops and bottoms

### 3. Entry and Exit Strategies
- **Partial Entries:** the bot can place a small initial position on the breakout and scale into the trade as the breakout gains momentum, reducing risk in case of a fakeout
- **Confirmation Breakout Entries:** the bot will wait for confirmation before placing an entry order, reducing the risk of enterings that could be fakeouts
- **Trailing Stop Losses:** the bot will place a trailing stop loss based on ATR, this allows the bot to seal profits even if the price direction reverses
- **Take Profit with Fibonacci Extensions:** The bot can automatically calculate Fibonacci extension levels as profit targets after the breakout occurs. For example, after breaking out, the bot can take partial profits at the 1.618 Fibonacci extension level.
### 4. Multi-Timeframe Analysis
Multi-timeframe analysis allows the bot to check for breakouts on multiple chart timeframes for stronger signals. For example, if the bot detects a breakout on both the daily and 4-hour charts, it may give more weight to the signal. This provides higher confidence for the trade:
- **Higher Timeframe for Trend:** The bot identifies the overall trend on a higher timeframe (e.g., daily).
- **Lower Timeframe for Entry:** The bot zooms into a lower timeframe (e.g., 1-hour) to detect precise breakout levels and execute the trade.
### 5. Entry Signals
1. Resistance Breakout with Confirmation
2. Support Breakout
3. Bollinger Band Breakout
4. Donchian Channel Breakout
5. Volume Spike with Breakout
6. Ichimoku Cloud Breakout
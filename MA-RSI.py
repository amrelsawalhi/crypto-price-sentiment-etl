import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

# Load the data from CSV
df = pd.read_csv('bitcoin_daily_ohlcv.csv', parse_dates=['timestamp'], index_col='timestamp')

# Calculate the Moving Average (200)
df['MA200'] = df['close'].rolling(window=200).mean()

# Calculate the RSI (Relative Strength Index)
delta = df['close'].diff()
gain = (delta.where(delta > 0, 0)).fillna(0)
loss = (-delta.where(delta < 0, 0)).fillna(0)

avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

df['RSI'] = rsi

# Prepare the moving average and RSI for plotting
ma200 = mpf.make_addplot(df['MA200'], color='blue', panel=0)  # On the main chart
rsi = mpf.make_addplot(df['RSI'], color='red', panel=1)  # On a separate RSI panel

# Plotting the candlestick chart with the Moving Average and RSI
mpf.plot(df, type='candle', addplot=[ma200, rsi], figsize=(10, 8), title="Bitcoin Price with MA(200) and RSI", ylabel='Price', ylabel_lower='RSI')

# Adjust title placement
plt.suptitle("Bitcoin Price with MA(200) and RSI", fontsize=16)

# Show the plot
plt.show()

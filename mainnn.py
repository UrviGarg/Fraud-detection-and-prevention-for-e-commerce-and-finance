import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf, pacf

# Load data
data = pd.read_csv('onlinefraud.csv')

# Set 'step' as index
data.set_index('step', inplace=True)

# Select the 'amount' column for time series analysis
ts = data['amount']

# Reduce data size for testing (e.g., use first 1000 rows)
ts = ts.head(1000)

# Check for stationarity
result = adfuller(ts)
print('ADF Statistic:', result[0])
print('p-value:', result[1])

# Differencing to achieve stationarity
ts_diff = ts.diff().dropna()

# ACF and PACF plots
plt.figure(figsize=(12, 8))

# ACF Plot
plt.subplot(211)
plt.title('ACF Plot')
plt.plot(acf(ts_diff, nlags=20))
plt.xlabel('Lag')
plt.ylabel('ACF')

# PACF Plot
plt.subplot(212)
plt.title('PACF Plot')
plt.plot(pacf(ts_diff, nlags=20))
plt.xlabel('Lag')
plt.ylabel('PACF')

plt.tight_layout()
plt.show()

# Determine ARIMA parameters (p, d, q)
# For simplicity, let's use (1, 1, 1) as a starting point
p, d, q = 1, 1, 1

# Fit ARIMA model
model = ARIMA(ts, order=(p, d, q))
model_fit = model.fit()
print(model_fit.summary())

# Forecast
forecast_steps = 30
forecast = model_fit.forecast(steps=forecast_steps)

# Plot Original Time Series vs. Forecast
plt.figure(figsize=(12, 6))
plt.plot(ts, label='Original')
plt.plot(np.arange(len(ts), len(ts) + forecast_steps), forecast, color='red', label='Forecast')
plt.title('Original Time Series vs. Forecast')
plt.xlabel('Step')
plt.ylabel('Amount')
plt.legend()
plt.show()

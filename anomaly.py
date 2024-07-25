import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Load data
data = pd.read_csv('onlinefraud.csv')

# Set 'step' as index
data.set_index('step', inplace=True)

# Select the 'amount' column for anomaly detection
X = data[['amount']].values

# Fit Isolation Forest model
iso = IsolationForest(contamination=0.1, random_state=42)
labels = iso.fit_predict(X)

# Identify anomalies
anomalies = X[labels == -1]

# Plot anomalies
plt.figure(figsize=(10, 6))
plt.plot(data.index, X, label='Amount')
plt.scatter(data.index[labels == -1], anomalies, color='red', label='Anomalies')
plt.xlabel('Step')
plt.ylabel('Amount')
plt.title('Anomaly Detection using Isolation Forest')
plt.legend()
plt.show()

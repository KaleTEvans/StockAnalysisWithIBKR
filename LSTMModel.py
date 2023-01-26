from IBKRconnections.App import App
from ibapi.client import *
import time
import datetime

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

from HistoricalDataAnalysis import HistoricalData

# Plot function for data visualization
def interactive_plot(df, title):
    fig = px.line(title = title)

    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'], y = df[i], name = i)

    fig.show()

hd = HistoricalData("SPY", "1 M", "5 mins", "TRADES")
hd.show_time()
time.sleep(1)

historical_data_df = hd.get_data()

time.sleep(.1)
del hd

# Get just the volume and price data for the model
price_volume_df = historical_data_df[['Date', 'Close', 'Volume']]
print(price_volume_df)

# Normalize the data
training_data = price_volume_df.iloc[:, 1:3].values

sc = MinMaxScaler(feature_range = (0,1))
training_set_scaled = sc.fit_transform(training_data)

# Create the training and testing data
x = []
y = []

for i in range(1, len(price_volume_df)):
    x.append(training_set_scaled[i-1:i, 0])
    y.append(training_set_scaled[i, 0])

    # Convert into array format
X = np.asarray(x)
Y = np.asarray(y)

# Split the data for 70% training and 30% testing
split = int(0.7 * len(X))
X_train = X[:split]
Y_train = Y[:split]
X_test = X[split:]
Y_test = Y[split:]

# Reshape the 1D arrays to 3D arrays to feed to model
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Create the model
inputs = tf.keras.layers.Input(shape = (X_train.shape[1], X_train.shape[2]))
# Define LSTM network
x_t = tf.keras.layers.LSTM(150, return_sequences=True)(inputs) # 150 neurons 
x_t = tf.keras.layers.Dropout(0.3)(x_t)
x_t = tf.keras.layers.LSTM(150, return_sequences=True)(x_t)
x_t = tf.keras.layers.Dropout(0.3)(x_t)
x_t = tf.keras.layers.LSTM(150)(x_t) 
outputs = tf.keras.layers.Dense(1, activation = 'linear')(x_t)

model = tf.keras.Model(inputs = inputs, outputs = outputs)
model.compile(optimizer = 'adam', loss = 'mse')
model.summary()

# Train the model
history = model.fit(X_train, Y_train, epochs=20, batch_size=32, validation_split=0.2) # increase epochs to reduce error

# Make prediction
predicted = model.predict(X)

# Format the data for visual comparison
test_predicted = []
for i in predicted:
    test_predicted.append(i[0])

df_predicted = price_volume_df[1:][['Date']]
df_predicted['Predicted Price'] = test_predicted

close = []
for i in training_set_scaled:
    close.append(i[0])

df_predicted['Close'] = close[1:]

print(df_predicted)

interactive_plot(df_predicted, 'Original Price vs LSTM Predictions')

    

from IBKRconnections.App import App
from ibapi.client import *
import time
import pyodbc

import pandas as pd
import plotly.express as px
import matplotlib as mpl
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

# Connect to db
conn = pyodbc.connect("Driver={SQL Server};"
                        "Server=DESKTOP-FRBUP45\SQLEXPRESS;"
                        "Database=SocialSentimentDB;"
                        "Trusted_Connection=yes;")

cursor = conn.cursor()

# Import twitter and reddit mentions to dataframe
query = 'SELECT date, source, mention FROM finnhub ORDER BY date ASC'
sentiment_df = pd.read_sql(query, conn)

# Now plot
fig, ax = plt.subplots()
for label, grp in sentiment_df.groupby('source'):
    grp.plot(x = 'date', y = 'mention', ax=ax, label=label)

plt.show()

print(sentiment_df)
print(sentiment_df.dtypes)
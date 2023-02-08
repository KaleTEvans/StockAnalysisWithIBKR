from IBKRconnections.App import App
from ibapi.client import *
from datetime import datetime
from dateutil.tz import tzutc, tzlocal
import pyodbc
import pytz

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

# Function to convert from UTC to CST
def convertTime(date):
    dt_utc = date.replace(tzinfo=pytz.UTC)

    return dt_utc.astimezone(tzlocal())

# Connect to db
conn = pyodbc.connect("Driver={SQL Server};"
                        "Server=DESKTOP-FRBUP45\SQLEXPRESS;"
                        "Database=SocialSentimentDB;"
                        "Trusted_Connection=yes;")

cursor = conn.cursor()

# Import twitter and reddit mentions to dataframe
query = 'SELECT date, source, mention FROM finnhub ORDER BY date ASC'
sentiment_df = pd.read_sql(query, conn)

# Extract desired date range
start_date = '2022-12-01'
end_date = '2022-12-31'

mask = (sentiment_df['date'] >= start_date) & (sentiment_df['date'] <= end_date)
sentiment_df = sentiment_df.loc[mask]

sentiment_df['date'] = sentiment_df['date'].apply(convertTime)

reddit_df = sentiment_df[sentiment_df['source'] == 'reddit']
twitter_df = sentiment_df[sentiment_df['source'] == 'twitter']

fig = go.Figure(data=[
    go.Bar(x=reddit_df['date'], name='reddit', y=reddit_df['mention']),
    go.Bar(x=twitter_df['date'], name='twitter', y=twitter_df['mention'])
])

fig.update_layout(barmode='stack')
fig.show()


print(sentiment_df)
print(sentiment_df.dtypes)
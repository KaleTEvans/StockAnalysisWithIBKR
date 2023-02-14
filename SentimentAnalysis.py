from dateutil.tz import tzlocal
import pyodbc
import pytz

import pandas as pd
import plotly.express as px
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


from HistoricalDataAnalysis import HistoricalData

# Function to convert from UTC to CST
def convertTime(date):
    dt_utc = date.replace(tzinfo=pytz.UTC)

    return dt_utc.astimezone(tzlocal())

class SocialSentimentData():
    def __init__(self):

        # Connect to db
        self.conn = pyodbc.connect("Driver={SQL Server};"
                                "Server=DESKTOP-FRBUP45\SQLEXPRESS;"
                                "Database=SocialSentimentDB;"
                                "Trusted_Connection=yes;")
        
        print('Connected to db')

        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    # Create a string from an array of inputs for different queries
    def input_string(self, inputs):
        input_str = inputs[0]
        for i in inputs[1:]:
            input_str += f',{i}'

        return input_str

    # Will use inputs as an array of columns user wishes to select
    def query_data(self, ticker, inputs, db):

        input_str = self.input_string(inputs)

        query = f"SELECT {input_str} FROM {db} WHERE symbol = '{ticker}' ORDER BY date asc"
        print(query)
        sentiment_df = pd.read_sql(query, self.conn)

        # Update date to local time
        sentiment_df['date'] = sentiment_df['date'].apply(convertTime)
        sentiment_df = sentiment_df.set_index('date')

        return sentiment_df
    
    def query_by_date(self, ticker, inputs, db, start_date, end_date):
        
        input_str = self.input_string(inputs)

        query = f"SELECT {input_str} FROM {db} WHERE symbol = '{ticker}' AND date BETWEEN '{start_date}' AND '{end_date}' ORDER BY date asc"
        sentiment_df = pd.read_sql(query, self.conn)

        # Update date to local time
        sentiment_df['date'] = sentiment_df['date'].apply(convertTime)
        sentiment_df = sentiment_df.set_index('date')

        return sentiment_df

ss = SocialSentimentData()

inputs = ['date', 'source', 'mention', 'positive_mention', 'negative_mention', 'score']

sentiment_df_AAPL = ss.query_by_date('AAPL', inputs, 'finnhub', '2023-01-30', '2023-01-31 23:00:00')
sentiment_df_AMD = ss.query_by_date('AMD', inputs, 'finnhub', '2023-01-01', '2023-01-31 23:00:00')

sentiment_df_AAPL['negative_mention'] *= -1


# Extract desired date range
# start_date = '2022-01-01'
# end_date = '2022-12-31'

# mask = (sentiment_df['date'] >= start_date) & (sentiment_df['date'] <= end_date)
# sentiment_df = sentiment_df.loc[mask]

# reddit_df = sentiment_df[sentiment_df['source'] == 'reddit']
twitter_df_AAPL = sentiment_df_AAPL[sentiment_df_AAPL['source'] == 'twitter']
twitter_df_AMD = sentiment_df_AMD[sentiment_df_AMD['source'] == 'twitter']
daily_df_AAPL = twitter_df_AAPL.resample('D').agg({'mention':np.sum, 'score':np.mean})
daily_df_AMD = twitter_df_AMD.resample('D').agg({'mention':np.sum, 'score':np.mean})

# daily_df_AAPL['Color'] = np.where(daily_df_AAPL['score'] < 0, 'red', 'green')

fig = go.Figure(data=[
    go.Bar(x=daily_df_AAPL.index, name= 'AAPL', y=daily_df_AAPL['mention']),
    go.Bar(x=daily_df_AMD.index, name= 'AMD', y=daily_df_AMD['mention'])                                                            
    # go.Bar(x=daily_df_AAPL.index, y=daily_df_AAPL['mention'], marker_color=daily_df_AAPL['Color'] )
])

fig.update_layout(barmode='group')
fig.show()


# print(daily_df)
# daily_df.to_csv('SavedCSV/fourHour.csv')
# print(sentiment_df.dtypes)
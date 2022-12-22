from IBKRconnections.App import App
import time

from ibapi.client import *
import pandas as pd

import plotly.graph_objects as go

class HistoricalData(App):
    def __init__(self, symbol, time_frame, bar_size, include_data):
        # Not inheriting from app to ensure there won't be confusion with variable names
        self.app = App("127.0.0.1", 7496, 0)
        # Give time for app to connect
        time.sleep(0.1)
        self.symbol = symbol
        self.time_frame = time_frame
        self.bar_size = bar_size
        self.include_data = include_data

        # Retrieve Contract Info
        self.contract_fields = {
            "symbol": self.symbol,
            "secType": "STK",
            "exchange": "SMART",
            "currency": "USD"
        }
        self.contract_res = self.app.get_stock_contract(self.contract_fields)
        self.contract = self.contract_res.contract

    def __del__(self):
        self.app.disconnect()

    def show_time(self):
        requested_time = self.app.server_clock()
        print('Current time from server is: {}'.format(requested_time))

    def get_data(self):
        # Retrieve Historical Data
        self.historic_data = self.app.historical_data(self.contract, self.time_frame, self.bar_size, self.include_data)

        self.bar_fields = {
            "Date": [],
            "Open": [],
            "Close": [],
            "High": [],
            "Low": [],
            "Volume": []
        }

        for bar in self.historic_data:
            self.bar_fields["Date"].append(bar.date)
            self.bar_fields["Open"].append(bar.open)
            self.bar_fields["Close"].append(bar.close)
            self.bar_fields["High"].append(bar.high)
            self.bar_fields["Low"].append(bar.low)
            self.bar_fields["Volume"].append(bar.volume)
    

def main():
    hd = HistoricalData("SPY", "1 M", "5 mins", "TRADES")
    hd.show_time()
    time.sleep(1)
    hd.get_data()

    historical_data_df = pd.DataFrame(hd.bar_fields)
    print(historical_data_df)

    fig = go.Figure(data=[go.Candlestick(x=historical_data_df['Date'],
                    open=historical_data_df['Open'],
                    close=historical_data_df['Close'],
                    high=historical_data_df['High'],
                    low=historical_data_df['Low'])])

    fig.show()

    time.sleep(1)
    del hd
    # app.disconnect()

if __name__ == '__main__':
    main()
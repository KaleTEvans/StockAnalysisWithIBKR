from App import App
import time

from ibapi.client import *
import pandas as pd

def main():
    # Connect to localhost, note 7497 is for paper trading, 7496 is for live trading
    app = App("127.0.0.1", 7496, 0)

    requested_time = app.server_clock()
    print('Current time from server is: {}'.format(requested_time))

    contract_fields = {
        "symbol": "AAPL",
        "secType": "STK",
        "exchange": "SMART",
        "currency": "USD"
    }
    res = app.get_stock_contract(contract_fields)
    print('ID: {}'.format(res.contract.conId))

    historical_data = app.historical_data(res.contract, '3 M', '1 day', 'TRADES')
    bar_fields = {
        "Date": [],
        "Open": [],
        "Close": [],
        "High": [],
        "Low": [],
        "Volume": []
    }
    for bar in historical_data:
        bar_fields["Date"].append(bar.date)
        bar_fields["Open"].append(bar.open)
        bar_fields["Close"].append(bar.close)
        bar_fields["High"].append(bar.high)
        bar_fields["Low"].append(bar.low)
        bar_fields["Volume"].append(bar.volume)

    historical_data_df = pd.DataFrame(bar_fields)
    print(historical_data_df)

    time.sleep(2)
    app.disconnect()

if __name__ == '__main__':
    main()
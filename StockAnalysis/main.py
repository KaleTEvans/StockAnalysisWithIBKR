from App import App
import time

from ibapi.client import *

def main():
    # Connect to localhost, note 7497 is for paper trading, 7496 is for live trading
    app = App("127.0.0.1", 7496, 0)

    requested_time = app.server_clock()
    print('Current time from server is: {}'.format(requested_time))

    res = app.stock_details('AAPL')
    print('ID: {}'.format(res.contract.conId))

    time.sleep(2)
    app.disconnect()

if __name__ == '__main__':
    main()
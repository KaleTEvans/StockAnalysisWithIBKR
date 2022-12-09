from App import App
import time

def main():
    # Connect to localhost, note 7497 is for paper trading, 7496 is for live trading
    app = App("127.0.0.1", 7496, 0)

    requested_time = app.server_clock()
    print('Current time from server is: {}'.format(requested_time))

    time.sleep(2)
    app.disconnect()

if __name__ == '__main__':
    main()
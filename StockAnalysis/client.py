import sys
import os.path

TWSimport = os.path.join(sys.path[0], 'C:\\TWS API\\source\\pythonclient')
# print(TWSimport)
sys.path.insert(1, TWSimport)

from ibapi.client import *
import datetime

class Client(EClient):

    def __init__(self, wrapper):
        EClient. __init__(self, wrapper)
        
    def queue_handler(self, req_queue, max_wait_time = 5):
        try:
            requested_data = req_queue.get(timeout = max_wait_time)
        except queue.Empty():
            print('The queue was empty or the max time was reached')
            requested_data = None

        while self.wrapper.is_error():
            print('Error:')
            print(self.get_error(timeout=5))

        return requested_data

    # ---------------------------
    # Time Handling Methods
    # ---------------------------
    # Use this at the beginning of each program to ensure server connection has been established
    def server_clock(self):
        print('Retreiving unix time from server')

        # Create a queue to store the time
        time_storage = self.wrapper.init_queue()   

        requested_time = self.reqCurrentTime()

        requested_time = self.queue_handler(time_storage)

        del time_storage

        return datetime.datetime.utcfromtimestamp(requested_time).strftime('%Y-%m-%d %H:%M:%S')

    # ---------------------------
    # Retrieve Tickers by Desctiption
    # ---------------------------
    def symbol_by_desc(self, descs):
        print('Retreiving related contracts')

        self.reqMatchingSymbols(0, descs)

    # ---------------------------
    # Contract Info 
    # ---------------------------
    def stock_details(self, ticker):
        print('Retreiving contract info')

        contract = Contract()
        contract.symbol = ticker
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'

        contract_storage = self.wrapper.init_queue()

        self.reqContractDetails(1, contract)

        requested_contract = self.queue_handler(contract_storage)

        del contract_storage
        
        return requested_contract
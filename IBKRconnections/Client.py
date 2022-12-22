import sys
import os.path

TWSimport = os.path.join(sys.path[0], 'C:\\TWS API\\source\\pythonclient')
# print(TWSimport)
sys.path.insert(1, TWSimport)

from ibapi.client import *
from ibapi.account_summary_tags import *
import datetime
import time

class Client(EClient):

    def __init__(self, wrapper):
        EClient. __init__(self, wrapper)

    # ---------------------------
    # Time Handling Methods
    # ---------------------------
    # Use this at the beginning of each program to ensure server connection has been established
    def server_clock(self):
        # print('Retreiving unix time from server')
        # Create a queue to store the time
        time_storage = self.wrapper.init_queue()   
        # Request the data
        self.reqCurrentTime()
        # Retrieve data from queue
        try:
            requested_time = time_storage.get(timeout = 1)
        except queue.Empty:
            print('CURRENT TIME: The queue was empty or the max time was reached')
            requested_time = None

        while self.wrapper.is_error():
            print('Error:')
            print(self.get_error(timeout=5))

        # Remove empty queue
        del time_storage
        return datetime.datetime.utcfromtimestamp(requested_time).strftime('%Y-%m-%d %H:%M:%S')

    # -------------------------
    # Account Info
    # -----------------------
    def account_info(self):
        print('Account Information:')
        account_info_storage = self.wrapper.init_queue()
        self.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)
        # Not sure how to tell when queue is full, will wait for it to fill 
        time.sleep(.1)
        requested_acct_info = []

        try:
            requested_acct_info.append(account_info_storage.get(timeout = 1))
        except queue.Empty:
            print('ACCOUNT INFO: The queue was empty or the max time was reached')
            requested_acct_info = None
        else:
            while not account_info_storage.empty():
                requested_acct_info.append(account_info_storage.get(timeout = 1))

        while self.wrapper.is_error():
            print('Error:')
            print(self.get_error(timeout=5))
        
        del account_info_storage
        self.cancelAccountSummary(9001)

        return requested_acct_info

    # ---------------------------
    # Retrieve Tickers by Desctiption
    # ---------------------------
    def symbol_by_desc(self, descs):
        print('Retreiving related contracts')

        self.reqMatchingSymbols(0, descs)

    # ---------------------------
    # Contract Info 
    # ---------------------------
    def get_stock_contract(self, fields):

        contract = Contract()
        
        if "symbol" in fields:
            contract.symbol = fields["symbol"]
        if "secType" in fields:
            contract.secType = fields["secType"]
        if "lastTradeDateOrContractMonth" in fields:
            contract.lastTradeDateOrContractMonth = fields["lastTradeDateOrContractMonth"]
        if "strike" in fields:
            contract.strike = fields["strike"]
        if "right" in fields:
            contract.right = fields["right"]
        if "multiplier" in fields:
            contract.multiplier = fields["multiplier"]
        if "exchange" in fields:
            contract.exchange = fields["exchange"]
        if "primaryExchange" in fields:
            contract.primaryExchange = fields["primaryExchange"]
        if "currency" in fields:
            contract.currency = fields["currency"]
        if "localSymbol" in fields:
            contract.localSymbol = fields["localSymbol"]
        if "tradingClass" in fields:
            contract.tradingClass = fields["tradingClass"]
        if "includeExpired" in fields:
            contract.includeExpired = fields["includeExpired"]
        if "secIdType" in fields:
            contract.secIdType = fields["secIdType"]
        if "secId" in fields:
            contract.secId = fields["secId"]

        contract_storage = self.wrapper.init_queue()
        
        self.reqContractDetails(1001, contract)

        try:
            requested_contract = contract_storage.get(timeout = 1)
        except queue.Empty:
            print('CONTRACT DETAILS: The queue was empty or the max time was reached')
            requested_contract = None

        while self.wrapper.is_error():
            print('Error:')
            print(self.get_error(timeout=5))

        del contract_storage
        
        return requested_contract

    # ------------------------
    # Retrieve Historical Data
    # ------------------------
    def historical_data(self, contract, duration, bar_size, include, trading_hours = 0, format_date = 1, refresh = False):
        # include: see api docs for available data
        # trading_hours: 0 for extended trading hours, 1 for regular
        # refresh: set to true if you would like data to be updated real time
        print('Retrieving historical data for {}'.format(contract.symbol))
        # Get current date and time
        queryTime = (datetime.datetime.now()).strftime("%Y%m%d-%H:%M:%S")
        print(queryTime)

        historical_data_storage = self.wrapper.init_queue()
        self.reqHistoricalData(4001, contract, queryTime, duration, bar_size, include, trading_hours, format_date, refresh, [])
        # Not sure how to tell when queue is full, will wait for it to fill 
        time.sleep(1)
        requested_bar_info = []

        try:
            bar_data = historical_data_storage.get(timeout = 5)
            requested_bar_info.append(bar_data)
        except queue.Empty:
            print('HISTORICAL DATA: The queue was empty or the max time was reached')
            requested_bar_info = None
        else:
            while not historical_data_storage.empty():
                bar_data = historical_data_storage.get(timeout = 1)
                requested_bar_info.append(bar_data)

        while self.wrapper.is_error():
            print('Error:')
            print(self.get_error(timeout=5))
        
        del historical_data_storage
        if refresh == False: self.cancelHistoricalData(4001)

        return requested_bar_info
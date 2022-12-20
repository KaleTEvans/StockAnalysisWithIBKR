import sys
import os.path

TWSimport = os.path.join(sys.path[0], 'C:\\TWS API\\source\\pythonclient')
# print(TWSimport)
sys.path.insert(1, TWSimport)

from ibapi.wrapper import *

import queue
import time
import math

# The wrapper handles incoming messages from the server
# This will override the defaulr api methods to produce cleaner and more readable information

class Wrapper(EWrapper):

    # ---------------------------
    # Error Handling
    # ---------------------------
    # This class will also overwrite the api's default error handling
    def init_error(self):
        error_queue = queue.Queue()
        self.my_errors_queue = error_queue

    # Check if a message was returned from the queue
    def is_error(self):
        error_exist = not self.my_errors_queue.empty()
        return error_exist

    def get_error(self, timeout=6):
        if self.is_error():
            try:
                return self.my_errors_queue.get(timeout=timeout)
            except queue.Empty:
                # Can add output here if error is received
                return None
        return None

    def error(self, id, error_code, error_str, advancedOrderRejectJson):
        # Override the native method
        # Skip over error codes 2104, 2106, and 2158. These are just messages saying connection 
        # has been established, but add noise to the terminal       
        if error_code not in [2104, 2106, 2158]:
            errormessage = 'IB error: %s , ID: %d returned with code %d' % (error_str, id, error_code)
            self.my_errors_queue.put(errormessage)

    # Queue for handling data returned to the wrapper
    def init_queue(self):
        wrapper_queue = queue.Queue()
        self.my_wrapper_queue = wrapper_queue
        return wrapper_queue


    def currentTime(self, server_time):
        ## Overriden method
        self.my_wrapper_queue.put(server_time)

    def accountSummary(self, reqId, account, tag, value, currency):
        self.my_wrapper_queue.put({
            "reqId": reqId,
            "account": account,
            "tag": tag,
            "value": value,
            "currency": currency
        })

    def symbolSamples(self, req_id, descs):
        # Print the number of symbols in the returned results
        for desc in descs:
            if (desc.contract.symbol != ''):
                print('Symbol: {}'.format(desc.contract.symbol))

    def contractDetails(self, req_id, details):
        print('Retrieving contract id for {}'.format(details.longName))
        self.my_wrapper_queue.put(details)

    def historicalData(self, reqId, bar):
        # Add items to the queue
        self.my_wrapper_queue.put(bar)
        
        



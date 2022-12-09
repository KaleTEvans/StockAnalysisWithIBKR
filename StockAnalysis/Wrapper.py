import sys
import os.path

TWSimport = os.path.join(sys.path[0], 'C:\\TWS API\\source\\pythonclient')
# print(TWSimport)
sys.path.insert(1, TWSimport)

from ibapi.wrapper import *

import queue
import datetime
import time
import math

# The wrapper handles incoming messages from the server
# This will override the defaulr api methods to produce cleaner and more readable information

class Wrapper(EWrapper):
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

    def error(self, id, errorCode, errorStr, advancedOrderRejectJson):
        # Override the native method
        # Skip over error codes 2104, 2106, and 2158. These are just messages saying connection 
        # has been established, but add noise to the terminal       
        if errorCode not in [2104, 2106, 2158]:
            errormessage = 'IB error: %s , ID: %d returned with code %d' % (errorStr, id, errorCode)
            self.my_errors_queue.put(errormessage)

    # Time handling methods
    def init_time(self):
        time_queue = queue.Queue()
        self.my_time_queue = time_queue
        return time_queue

    def currentTime(self, server_time):
        ## Overriden method
        self.my_time_queue.put(server_time)


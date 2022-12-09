import sys
import os.path

TWSimport = os.path.join(sys.path[0], 'C:\\TWS API\\source\\pythonclient')
# print(TWSimport)
sys.path.insert(1, TWSimport)

from ibapi.client import *

class Client(EClient):
    ''' Serves as the client and the wrapper '''

    def __init__(self, wrapper):
        EClient. __init__(self, wrapper)

    def server_clock(self):
        print('Retreiving unix time from server')

        # Create a queue to store the time
        time_storage = self.wrapper.init_time()   

        self.reqCurrentTime()

        # Max wait time if there is no connection
        max_wait_time = 10

        try:
            requested_time = time_storage.get(timeout = max_wait_time)
        except queue.Empty():
            print('The queue was empty or the max time was reached')
            requested_time = None

        while self.wrapper.is_error():
            print('Error:')
            print(self.get_error(timeout=5))

        return requested_time

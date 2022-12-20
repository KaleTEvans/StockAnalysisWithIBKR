from IBKRconnections.Client import Client
from IBKRconnections.Wrapper import Wrapper

from threading import Thread

class App(Wrapper, Client):
    # Initialize the main classes
    def __init__(self, ipaddr, portid, clientid):
        Wrapper.__init__(self)
        Client.__init__(self, wrapper=self)

        # Connect to server 
        self.connect(ipaddr, portid, clientid)

        # Initialize threading
        thread = Thread(target=self.run)
        thread.start()
        setattr(self, "_thread", thread)

        # Start listening for errors
        self.init_error()
import sys
import os.path

TWSimport = os.path.join(sys.path[0], 'C:\\TWS API\\source\\pythonclient')
print(TWSimport)
sys.path.insert(1, TWSimport)

import ibapi
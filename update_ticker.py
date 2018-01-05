import json
from money import *

def update_ticker(V,T):
    V['ticker'] = Money(T.returnTicker()[V['currencyPair']]['last'])
    return V


    #while True:
    #    try:
    #        with open('.data.dat', 'r') as f:
    #            PV = json.loads(f.read())
    #        break
    #    except:
    #        print("Error accessing data file")
    #return PV


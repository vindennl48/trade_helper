from money import *
import sys
from time import sleep

def get_buy_fee(V,T):
    if V['orderNumber'] == 'fake':
        V['actual_fee'] = Money(0.0015)
        V['amount_coins'] = V['amount_coins'] * (Money(1)-V['actual_fee'])
        return V

    for x in range(10):
        try:
            trades = T.returnTradeHistory(V['currencyPair'])
            for trade in trades:
                if V['orderNumber'] == trade['orderNumber']:
                    V['actual_fee'] = Money(trade['fee'].rstrip())
                    V['amount_coins'] = V['amount_coins'] * (Money(1)-V['actual_fee'])
                    return V
        except: pass

    raise Exception("Trade does not exist!")


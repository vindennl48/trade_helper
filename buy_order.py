from money import *
import sys

def create_buy_order(V,T):
    if V['balance'] >= V['amount_usd']:
        V['amount_coins'] = V['amount_usd']/V['rate']

        info = {}
        if not 'fake' in V:
            info = T.buy(
                V['currencyPair'],
                V['rate'],
                V['amount_coins']
            )

        if 'error' in info:
            print("ERROR: {}".format(info['error']))
            sys.exit()

        try:
            V['orderNumber'] = info['orderNumber']
        except:
            V['orderNumber'] = 'fake'
    else:
        print("You do not have enough money for this trade!!")
        sys.exit()

    return V

def confirm_buy_open_order(PV,V):
    orders = PV['open_orders'][V['currencyPair']]
    for order in orders:
        if V['orderNumber'] == order['orderNumber'] or \
            V['orderNumber'] == 'fake':

            return True
    return False

def confirm_buy_close_order(PV,V):
    trades = PV['trade_history'][V['currencyPair']]
    for trade in trades:
        if V['orderNumber'] == trade['orderNumber'] or \
            V['orderNumber'] == 'fake':

            return True
    return False

def get_fee(PV,V):
    trades = PV['trade_history'][V['currencyPair']]
    for trade in trades:
        if V['orderNumber'] == trade['orderNumber']:
            V['actual_fee'] = Money(trade['fee'].rstrip())
            V['amount_coins'] = V['amount_coins'] * (Money(1)-V['actual_fee'])
            return V

    if V['orderNumber'] == 'fake':
        V['actual_fee'] = Money(0.0015)
        V['amount_coins'] = V['amount_coins'] * (Money(1)-V['actual_fee'])
        return V
    else:
        raise Exception("Trade does not exist!")


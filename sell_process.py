from misc_funcs import *
import sys



def hit_stoploss(V):
    if V['sl_rate']*V['sl_fast'] >= V['ticker']:
        return True
    return False

def sell_now(V,T):
    if 'fake' in V:
        V['orderNumber'] = 'fake'
        return V

    info = {}
    while True:
        try:
            info = T.sell(
                V['currencyPair'],
                V['ticker']*0.6,
                V['amount_coins']
            )
            break
        except: print("ERROR: Dumping coins failed.. Trying again..")

    if 'error' in info:
        print("ERROR: {}".format(info['error']))
        sys.exit()
    elif 'orderNumber' in info:
        V['orderNumber'] = info['orderNumber']
    else:
        print("ERROR: Unknown return from buy order..")
        sys.exit()

    return V

def watching_stoploss(V):
    if V['ticker'] >= V['buy_rate']*1.005:
        return False
    return True


def confirm_halfp_close_order(V,T):
    if V['orderNumber'] == 'fake':
        return True

    try:
        trades = T.returnTradeHistory(V['currencyPair'])
        for trade in trades:
            if V['halfp_orderNumber'] == trade['orderNumber']:
                return True
    except: pass

    return False

def watching_full(V):
    if V['ticker'] <= V['buy_rate']:
        return False
    return True

def cancel_full_open_order(V,T):
    info = {}
    if not 'fake' in V:
        while True:
            try:
                info = T.cancel(
                    V['currencyPair'],
                    V['orderNumber']
                )
                break
            except:
                print("Error while tryinig to cancel full open order!")

def cancel_halfp_open_order(V,T):
    info = {}
    if not 'fake' in V and \
        V['halfp'] == 'No' and \
        V['halfp_active']:

        while True:
            try:
                T.cancel(
                    V['currencyPair'],
                    V['halfp_orderNumber']
                )
                break
            except:
                print("Error while tryinig to cancel halfp open order!")


def create_half_p(V,T):
    if V['halfp'] == 'No' and \
        V['halfp_active']:

        if 'fake' in V:
            V['halfp_orderNumber'] = 'fake'
            return V

        info = {}
        info = T.sell(
            V['currencyPair'],
            V['halfp_rate'],
            V['amount_coins'] / 2
        )

        if 'error' in info:
            print("ERROR: {}".format(info['error']))
            sys.exit()

        V['halfp_orderNumber'] = info['orderNumber']

    return V

def confirm_open_sell_order(PV,V):
    if V['orderNumber'] == 'fake':
        return True

    try:
        orders = PV['open_orders'][V['currencyPair']]
        for order in orders:
            if V['orderNumber'] == order['orderNumber']:
                return True

        trades = PV['trade_history'][V['currencyPair']]
        for trade in trades:
            if V['orderNumber'] == trade['orderNumber']:
                return True
    except: pass
        
    return False

def confirm_open_halfp_order(PV,V):
    if not V['halfp_active']:
        return True

    if V['halfp_orderNumber'] == 'fake':
        return True

    try:
        orders = PV['open_orders'][V['currencyPair']]
        for order in orders:
            if V['halfp_orderNumber'] == order['orderNumber']:
                return True

        trades = PV['trade_history'][V['currencyPair']]
        for trade in trades:
            if V['halfp_orderNumber'] == trade['orderNumber']:
                return True
    except: pass
        
    return False

from misc_funcs import *



def hit_stoploss(PV,V):
    if V['sl_rate']*1.005 >= get_market_rate(PV,V):
        return True
    return False

def sell_now(PV,V,T):
    info = {}
    if not 'fake' in V:
        info = T.sell(
            V['currencyPair'],
            get_market_rate(PV,V)*0.6,
            V['amount_coins']
        )

    if 'error' in info:
        print("ERROR: {}".format(info['error']))
        sys.exit()

    try:
        V['orderNumber'] = info['orderNumber']
    except:
        V['orderNumber'] = 'fake'

    return V

def watching_stoploss(PV,V):
    if get_market_rate(PV,V) >= V['buy_rate']*1.005:
        return False
    return True

def confirm_sell_close_order(PV,V):
    trades = PV['trade_history'][V['currencyPair']]
    for trade in trades:
        if V['orderNumber'] == trade['orderNumber']:
            return True
        elif V['orderNumber'] == 'fake':
            if get_market_rate(PV,V) >= V['full_rate']:
                return True
    return False

def watching_full(PV,V):
    if get_market_rate(PV,V) <= V['buy_rate']:
        return False
    return True

def cancel_full_open_order(PV,V,T):
    info = {}
    if not 'fake' in V:
        try:
            T.cancel(
                V['currencyPair'],
                V['orderNumber']
            )
        except:
            print("Error while tryinig to cancel full open order!")

def create_sell_order(V,T):
    info = {}
    if not 'fake' in V:
        info = T.sell(
            V['currencyPair'],
            V['full_rate'],
            V['amount_coins']
        )

    if 'error' in info:
        print("ERROR: {}".format(info['error']))
        sys.exit()

    try:
        V['orderNumber'] = info['orderNumber']
    except:
        V['orderNumber'] = 'fake'

    return V

def confirm_open_sell_order(PV,V):
    if V['orderNumber'] == 'fake':
        return True

    orders = PV['open_orders'][V['currencyPair']]
    for order in orders:
        if V['orderNumber'] == order['orderNumber']:
            return True

    trades = PV['trade_history'][V['currencyPair']]
    for trade in trades:
        if V['orderNumber'] == trade['orderNumber']:
            return True
        
    return False

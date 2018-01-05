from misc_funcs import *
import sys



def hit_stoploss(PV,V):
    if V['sl_rate']*V['sl_fast'] >= get_market_rate(PV,V):
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
    try:
        trades = PV['trade_history'][V['currencyPair']]
        for trade in trades:
            if V['orderNumber'] == trade['orderNumber']:
                return True
            elif V['orderNumber'] == 'fake':
                if get_market_rate(PV,V) >= V['full_rate']:
                    return True
    except: pass
    return False

def confirm_halfp_close_order(PV,V):
    if not V['halfp_active']:
        return False

    try:
        trades = PV['trade_history'][V['currencyPair']]
        for trade in trades:
            if V['halfp_orderNumber'] == trade['orderNumber']:
                return True
            elif V['halfp_orderNumber'] == 'fake':
                if get_market_rate(PV,V) >= V['halfp_rate']:
                    return True
    except: pass
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

def cancel_halfp_open_order(PV,V,T):
    info = {}
    if not 'fake' in V and \
        V['halfp'] == 'No' and \
        V['halfp_active']:

        try:
            T.cancel(
                V['currencyPair'],
                V['halfp_orderNumber']
            )
        except:
            print("Error while tryinig to cancel halfp open order!")

def create_sell_order(PV,V,T):
    info = {}
    if not 'fake' in V:

        if V['halfp_active']:
            amount = V['amount_coins'] / 2
        else:
            balance = Money(PV['balance'][V['currency']])
            amount = V['amount_coins']
            if amount > balance:
                amount = balance

        info = T.sell(
            V['currencyPair'],
            V['full_rate'],
            amount
        )

    if 'error' in info:
        print("ERROR: {}".format(info['error']))
        sys.exit()

    try:
        V['orderNumber'] = info['orderNumber']
    except:
        V['orderNumber'] = 'fake'

    return V

def create_half_p(V,T):
    if V['halfp'] == 'No' and \
        V['halfp_active']:

        info = {}
        if not 'fake' in V:
            info = T.sell(
                V['currencyPair'],
                V['halfp_rate'],
                V['amount_coins'] / 2
            )

        if 'error' in info:
            print("ERROR: {}".format(info['error']))
            sys.exit()

        try:
            V['halfp_orderNumber'] = info['orderNumber']
        except:
            V['halfp_orderNumber'] = 'fake'

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

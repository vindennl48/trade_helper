from money import *
from time import sleep
import json, sys


def create_order(buy_sell,V,T):
    if 'fake' in V:
        V['orderNumber'] = 'fake'
        V['amount_coins'] = V['amount_usd']/V['rate']
        return V

    V['balance'] = Money(T.returnBalances()['USDT'])

    if buy_sell == "buy":
        if V['balance'] < V['amount_usd']:
            print("You do not have enough money for this trade!!")
            sys.exit()

        V['amount_coins'] = V['amount_usd']/V['rate']
        info = {}
        for x in range(10):
            try:
                info = T.buy(
                    V['currencyPair'],
                    V['rate'],
                    V['amount_coins']
                )
                break
            except:
                print("ERROR: Either an input data error, or a connection error... Trying again..")

        if 'error' in info:
            print("ERROR: {}".format(info['error']))
            sys.exit()
        elif 'orderNumber' in info:
            V['orderNumber'] = info['orderNumber']
        else:
            print("ERROR: Unknown return from buy order..")
            sys.exit()


    elif buy_sell == "sell":
        if V['halfp_active']:
            amount = V['amount_coins'] / 2
        else:
            balance = V['balance']
            amount = V['amount_coins']
            if amount > balance:
                amount = balance

        info = {}
        info = T.sell(
            V['currencyPair'],
            V['full_rate'],
            amount
        )

        if 'error' in info:
            print("ERROR: {}".format(info['error']))
            sys.exit()
        elif 'orderNumber' in info:
            V['orderNumber'] = info['orderNumber']
        else:
            print("ERROR: Unknown return from buy order..")
            sys.exit()

    return V



def confirm_close_order(V,T):
    if V['orderNumber'] == 'fake':
        return True

    try:
        trades = T.returnTradeHistory(V['currencyPair'])
        for trade in trades:
            if V['orderNumber'] == trade['orderNumber']:
                return True
    except: pass

    return False



def json_pretty(json_obj):
    return json.dumps(json_obj, indent=4, separators=(',', ': '))

def set_now_profit(V):
    try:
        start_profit = V['start_profit']
    except:
        start_profit = False

    if V['position'] != '....' and start_profit:
        if V['halfp'] == 'Yes' and V['halfp_active']:
            ratio = V['halfp_rate'] / V['buy_rate']
            result = (V['amount_usd']/2)* ratio * V['fee_inv'] * V['fee_inv']
            profit = result - (V['amount_usd']/2)

            ratio = V['ticker'] / V['buy_rate']
            result = (V['amount_usd']/2)* ratio * V['fee_inv'] * V['fee_inv']
            profit = profit + (result - (V['amount_usd']/2))

            V['now_profit'] = profit
        else:
            ratio = V['ticker'] / V['buy_rate']
            result = V['amount_usd'] * ratio * V['fee_inv'] * V['fee_inv']
            result = result - V['amount_usd']
            V['now_profit'] = result
    else:
        V['now_profit'] = Money(0)
    return V

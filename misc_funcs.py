from money import *
import json

def get_market_rate(PV,V):
    return Money(
        PV['ticker'][V['currencyPair']]['last']
    )

def json_pretty(json_obj):
    return json.dumps(json_obj, indent=4, separators=(',', ': '))

def set_now_profit(PV,V):
    if V['position'] != '....':
        if V['halfp'] == 'Yes' or True:
            ratio = V['halfp_rate'] / V['buy_rate']
            result = (V['amount_usd']/2)* ratio * V['fee_inv'] * V['fee_inv']
            profit = result - (V['amount_usd']/2)

            ratio = get_market_rate(PV,V) / V['buy_rate']
            result = (V['amount_usd']/2)* ratio * V['fee_inv'] * V['fee_inv']
            profit = profit + (result - (V['amount_usd']/2))

            V['now_profit'] = profit
        else:
            ratio = get_market_rate(PV,V) / V['buy_rate']
            result = V['amount_usd'] * ratio * V['fee_inv'] * V['fee_inv']
            result = result - V['amount_usd']
            V['now_profit'] = result
    else:
        V['now_profit'] = Money(0)
    return V

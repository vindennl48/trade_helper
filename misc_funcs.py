from money import *
import json

def get_market_rate(PV,V):
    return Money(
        PV['ticker'][V['currencyPair']]['last']
    )

def json_pretty(json_obj):
    return json.dumps(json_obj, indent=4, separators=(',', ': '))


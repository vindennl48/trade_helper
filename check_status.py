from money      import *
from misc_funcs import *


def check_status(PV,V):
    # update ticker
    V['now_price'] = get_market_rate(PV,V)

    # update now_profit
    if 'amount_coins' in V:
        now_profit = Money(
            (
                V['amount_usd'] * (V['now_price']/V['buy_rate'])
            ) * V['fee_inv'] * V['fee_inv'] 
        ) - V['amount_usd']

    else:
        now_profit = Money(0)

    V['now_profit'] = now_profit

    # update position
    if 'orderNumber' in V:
        if V['orderNumber'] != 'stoploss':
            open_orders = PV['open_orders'][V['currencyPair']]
            try:
                trade_history = PV['trade_history'][V['currencyPair']]
            except:
                trade_history = []

            is_open_order = False
            for open_order in open_orders:
                if V['orderNumber'] == open_order['orderNumber']:
                    is_open_order = True
                    missing = 0
                    V['position'] = open_order['type']
                    break

            is_past_trade = False
            if not is_open_order:
                for trade in trade_history:
                    if V['orderNumber'] == trade['orderNumber']:
                        is_past_trade = True
                        missing = 0
                        if trade['type'] == 'buy':
                            if V['position'] != 'bought':
                                V['position'] = 'bought'
                                fi = 1-float(trade['fee'])
                                amount_coins = float(str(V['amount_coins']))
                                V['amount_coins'] = Money(amount_coins * fi)
                        elif trade['type'] == 'sell':
                            V['position'] = 'sold'
                        else:
                            V['position'] = 'Type?'
                        break
                if not is_past_trade:
                    if V['position'] != '..' and \
                    V['position'] != '......' and \
                    V['position'] != 'N/A':
                        print("#################################")
                        print("Buy order does not exist anymore!")
                        print("#################################")
                        if missing >= 10:
                            sys.exit()
                        missing += 1
                    else:
                        V['position'] = '......'
    else:
        V['position'] = "N/A"

#     # update half-profit
#     # if not 'halfp' in V:
#     #     V['halfp'] = 'No'
#     #     V['halfp_orderNumber'] = ""
#     # elif V['halfp'] == 'No':
#     #     for trade in trade_history:
#     #         if V['halfp_orderNumber'] == trade['orderNumber']:
#     #             V['halfp'] = 'Yes'
#     #             break

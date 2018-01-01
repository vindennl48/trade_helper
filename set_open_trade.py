from money import *

def set_open_trade():
    global V
    global PV
    balance = Money(PV['balance'][V['base_currency']])

    # if we havent bought yet, we need to buy first
    # Next, if price is below our bought price, make sure
    #    our order for halfp and full are canceled, and
    #    we watch for stoploss levels
    # If price is above our bought price and 10%, set halfp
    #    and full orders

    if V['position'] == 'N/A':          # we need to buy
        if balance >= V['amount_usd']:
            amount_usd = float(str(V['amount_usd']))
            rate       = float(str(V['rate']))
            V['amount_coins'] = Money(amount_usd/rate)
            info = {}
            #info = T.buy(V['currencyPair'],
            #    str(V['rate']),
            #    str(V['amount_coins'])
            #)

            if 'error' in info:
                print("ERROR: {}".format(info['error']))
                sys.exit()

            V['orderNumber']  = info['orderNumber']

            # set stoploss and full rate settings
            amount_usd = float(str(V['amount_usd']))
            profit     = float(str(V['profit']))
            risk       = float(str(V['risk']))
            buy_rate   = float(str(V['buy_rate']))
            fi         = float(str(fee_inv))
            V['sl_rate']   = Money(
                (((amount_usd-(profit/risk))/fi/fi)/amount_usd)*buy_rate
            )
            V['full_rate'] = Money(
                (((amount_usd+profit)/fi/fi)/amount_usd)*buy_rate
            )

            # set position to prevent repeat buys
            V['position'] = '..'

        else:
            print("You do not have enough money for this trade!!")
                                        # we need to sell
    elif V['position'] == 'bought':
        V['orderNumber'] = 'stoploss'
        V['position'] = 'sell'
    elif V['position'] == 'sell':
        now_rate = get_market_rate(PV,V)

        # watch for stoploss
        if now_rate <= V['buy_rate']:
            try:
                T.cancel(V['currencyPair'],V['orderNumber'])
            except:
                pass
            V['orderNumber'] = 'stoploss'
            sl_rate = float(str(V['sl_rate']))
            if float(str(now_rate)) <= sl_rate*1.005:
                # SELL!
                sell_rate = Money(sl_rate*.6)
                for x in range(10):
                    try:
                        info = T.sell(
                            V['currencyPair'],
                            str(sell_rate),
                            str(V['amount_coins'])
                        )
                        break
                    except:
                        print("Debug | now_rate: {}, pair: {}, sell_rate: {}, coins: {}".format(
                            str(now_rate),V['currencyPair'],str(sell_rate),V['amount_coins']
                        ))
                        print("Error trying to sell stoploss... Attempt No. {}".format(x+1))
                        if x+1 == 10:
                            sys.exit()
                V['position'] = 'sold'
        # set sell
        elif float(str(now_rate)) >= float(str(V['buy_rate']))*1.01:
            if V['orderNumber'] == 'stoploss' or \
               V['orderNumber'] == '':
                for x in range(10):
                    try:
                        info = T.sell(V['currencyPair'],
                            str(V['full_rate']),
                            str(V['amount_coins'])
                        )
                        break
                    except:
                        print("Error trying to sell full profit... Attempt No. {}".format(x+1))
                        if x+1 == 10:
                            sys.exit()

                V['orderNumber'] = info['orderNumber']

    elif V['position'] == 'sold':       # we are finished!
        print("Success!")
        sys.exit()

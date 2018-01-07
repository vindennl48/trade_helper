from GetArgs    import *
from money      import *
from misc_funcs import *

def get_variables(V,T):
    myargs = getargs([
        '--currency', 'base',     'currency',
        '--amount',   'amount',
        '--buy-rate', 'buy_rate',
        '--risk',     'risk',
        '--profit',   'profit',
        '--sl-rate',  'sl_rate',
        '--full-rate','full_rate',
        '--fake',     'fake',
        '--halfp',    'halfp_active',
        '--sl-fast',  'sl_fast',
        '--percent',  'percent'
    ])
    args = myargs.getargs()

    ## CURRENCY PAIR ##
    if '--currency' in args:
        V['base_currency'] = args['base'].rstrip().upper()
        V['currency']      = args['currency'].rstrip().upper()
        V['currencyPair']  = "{}_{}".format(V['base_currency'], V['currency'])
    else:
        raise Exception("You Need Currency Pair Set!")

    ## INITIALIZE VARIABLES ##
    V['fee']         = Money(0.0015)
    V['fee_inv']     = Money(1-V['fee'].float())
    V['now_profit']  = Money(0)
    V['orderNumber'] = ''
    V['update_id']   = 0
    V['balance']     = Money(T.returnBalances()[V['base_currency']])
    V['ticker']      = Money(T.returnTicker()[V['currencyPair']]['last'])

    ## TRADING AMOUNT USD ##
    if '--amount' in args:
        V['amount_usd'] = Money(args['amount'].rstrip())
    else:
        V['amount_usd'] = Money(10)

    ## BUY RATE ##
    if '--buy-rate' in args:
        V['rate'] = Money(args['buy_rate'].rstrip())
    else:
        V['rate'] = V['ticker']
    V['buy_rate'] = Money(V['rate'])

    ## TRADE DETAILS ##
    if '--percent' in args:
        # SL RATE AND FULL RATE MUST BE PRESENT!
        if not '--sl-rate' in args and not '--full-rate' in args:
            raise Exception("You Need stoploss rate and full rate if you want to use percent!")

        V['sl_rate']   = (Money(1) - (Money(args['sl_rate'].rstrip())   / Money(100))) * V['rate']
        V['full_rate'] = (Money(1) + (Money(args['full_rate'].rstrip()) / Money(100))) * V['rate']
        V['risk']      = (V['full_rate'] - V['buy_rate']) / (V['buy_rate'] - V['sl_rate'])
        V['profit']    = (((V['full_rate'] / V['buy_rate']) * V['amount_usd']) - V['amount_usd']) * V['fee_inv'] * V['fee_inv']

    else:
        if '--sl-rate' in args and '--full-rate' in args:
            V['sl_rate']   = Money(args['sl_rate'].rstrip())
            V['full_rate'] = Money(args['full_rate'].rstrip())
            V['risk']      = (V['full_rate'] - V['buy_rate']) / (V['buy_rate'] - V['sl_rate'])
            V['profit']    = (((V['full_rate'] / V['buy_rate']) * V['amount_usd']) - V['amount_usd']) * V['fee_inv'] * V['fee_inv']
        elif '--sl-rate' in args and not '--full-rate' in args:
            if not '--profit' in args:
                raise Exception("You need to include profit with these options!")

            V['profit']    = Money(args['profit'].rstrip())
            V['sl_rate']   = Money(args['sl_rate'].rstrip())
            V['full_rate'] = (
                (
                    (
                        (
                            V['amount_usd']+V['profit']
                        )/V['fee_inv']/V['fee_inv']
                    )/V['amount_usd']
                )*V['buy_rate']
            )
            V['risk']      = (V['full_rate'] - V['buy_rate']) / (V['buy_rate'] - V['sl_rate'])
        elif not '--sl-rate' in args and '--full-rate' in args:
            if not '--risk' in args:
                raise Exception("You need to include risk with these options!")

            V['risk']      = Money(args['risk'].rstrip())
            V['full_rate'] = Money(args['full_rate'].rstrip())
            V['profit']    = (((V['full_rate'] / V['buy_rate']) * V['amount_usd']) - V['amount_usd']) * V['fee_inv'] * V['fee_inv']
            V['sl_rate'] = (
                (
                    (
                        (
                            V['amount_usd'] - (V['profit']/V['risk']) 
                        )/V['fee_inv']/V['fee_inv']
                    )/V['amount_usd']
                )*V['buy_rate']
            )
        else:
            V['profit'] = Money(args['profit'].rstrip())
            V['risk']   = Money(args['risk'].rstrip())


    if '--halfp' in args:
        V['halfp_active'] = True
        V['halfp_rate']   = ((V['full_rate'] - V['buy_rate']) / 2) + V['buy_rate']
    else:
        V['halfp_active'] = False
        V['halfp_rate']   = Money(0)
    V['halfp'] = 'No'
    V['halfp_orderNumber'] = ''

    if '--sl-fast' in args:
        V['sl_fast'] = Money(args['sl_fast'].rstrip())
    else:
        V['sl_fast'] = Money(1)


    if '--fake' in args:
        V['fake'] = args['fake'].rstrip()


    return V

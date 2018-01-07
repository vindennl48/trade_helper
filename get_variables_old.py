from GetArgs    import *
from money      import *
from misc_funcs import *

def get_variables(V,T):
    myargs = getargs([
        '-c',         'base',     'currency',
        '--currency', 'base',     'currency',
        '-a',         'amount',
        '--amount',   'amount',
        '-r',         'buy_rate',
        '--buy-rate', 'buy_rate',
        '-x',         'risk',
        '--risk',     'risk',
        '-p',         'profit',
        '--profit',   'profit',
        '--sl-rate',  'sl_rate',
        '--full-rate','full_rate',
        '--fake',     'fake',
        '--halfp',    'halfp_active',
        '--sl-fast',  'sl_fast',
        '--percent',  'percent'
    ])
    args = myargs.getargs()

    V['fee']     = Money(0.0015)
    V['fee_inv'] = Money(1-V['fee'].float())

    if '-c' in args or '--currency' in args:
        V['base_currency'] = args['base'].rstrip().upper()
        V['currency']      = args['currency'].rstrip().upper()
        V['currencyPair']  = "{}_{}".format(V['base_currency'], V['currency'])
    else:
        raise Exception("You Need Currency Pair Set!")

    V['balance'] = Money(T.returnBalances()[V['base_currency']])
    V['ticker'] = Money(T.returnTicker()[V['currencyPair']]['last'])


    if '-a' in args or '--amount' in args:
        V['amount_usd'] = Money(args['amount'].rstrip())
    else:
        V['amount_usd'] = Money(10)

    if '-r' in args or '--buy-rate' in args:
        V['rate'] = Money(args['buy_rate'].rstrip())
    else:
        V['rate'] = V['ticker']
    V['buy_rate'] = Money(V['rate'])

    if '-p' in args or '--profit' in args:
        V['profit'] = Money(args['profit'].rstrip())
    else:
        V['profit'] = Money(1)

    if '-x' in args or '--risk' in args:
        V['risk'] = Money(args['risk'].rstrip())
    else:
        V['risk'] = Money(2)

    if '--sl-rate' in args:
        if '--percent' in args:
            V['sl_rate'] = (Money(1) - (Money(args['sl_rate'].rstrip()) / Money(100))) * V['rate']
        else:
            V['sl_rate'] = Money(args['sl_rate'].rstrip())
    else:
        V['sl_rate'] = (
            (
                (
                    (
                        V['amount_usd'] - (V['profit']/V['risk']) 
                    )/V['fee_inv']/V['fee_inv']
                )/V['amount_usd']
            )*V['buy_rate']
        )

    if '--full-rate' in args:
        if '--percent' in args:
            V['full_rate'] = (Money(1) + (Money(args['full_rate'].rstrip()) / Money(100))) * V['rate']
        else:
            V['full_rate'] = Money(args['full_rate'].rstrip())
    else:
        V['full_rate'] = (
            (
                (
                    (
                        V['amount_usd']+V['profit']
                    )/V['fee_inv']/V['fee_inv']
                )/V['amount_usd']
            )*V['buy_rate']
        )

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

    V['now_profit']  = Money(0)
    V['orderNumber'] = ''

    V['update_id'] = 0
    

    return V

from screen_table import st_build
from GetArgs import *
from tradeapi import *
from money import *
from time import sleep
import json, os, sys, thread


T           = Poloniex()    # Trading API
LOOP_DELAY  = 1000          # in milliseconds
PV          = {}            # Poloniex Variables
V           = {}            # Trade Variables
fee         = Money(0.0015)
fee_inv     = Money(1-0.0015)
missing     = 0


def EventLoop():
    L = []
    thread.start_new_thread(wait_for_enter, (L,))

    while True:             # MAIN EVENT LOOP
        if L:
            get_pause_menu(L)
        else:
            update_variables()
            check_status()
            set_open_trade()
            print_screen()
        delay()


def print_screen():
    global V
    global PV
    os.system('clear')
    st_build(
        [8,9,8,8,10,8,5,10],
        [
            [ 
                ['Amount'],
                ['Buy Price'],
                ['Target'],
                ['Stop'],
                ['Now Price'],
                ['Profit'],
                ['HalfP'],
                ['Position']
            ],
            [ 
                [str(V['amount_usd'])   ,'right'],
                [str(V['buy_rate'])     ,'right'],
                [str(V['full_rate'])    ,'right'],
                [str(V['sl_rate'])      ,'right'],
                [str(get_market_rate()) ,'right'],
                [str(V['now_profit'])   ,'right'],
                ['No'                   ,'right'],
                [str(V['position'])     ,'right']
            ]
        ]
    )
    print("Update ID: {}".format(PV['update_id']))
    print("Debug | Order Id: {}".format(V['orderNumber']))


def update_variables():
    global PV
    while True:
        try:
            with open('.data.dat', 'r') as f:
                PV = json.loads(f.read())
            break
        except:
            print("Error accessing data file")


def check_status():
    global V
    global missing

    # update ticker
    V['now_price'] = get_market_rate()

    # update now_profit
    if 'amount_coins' in V:
        amount    = float(str(V['amount_usd']))
        now_price = float(str(V['now_price']))
        buy_rate  = float(str(V['buy_rate']))
        fi        = float(str(fee_inv))
        ratio     = now_price/buy_rate
        now_profit = ((amount * ratio) * fi * fi) - amount
    else:
        now_profit = 0

    V['now_profit'] = Money(now_profit)

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

    # update half-profit
    # if not 'halfp' in V:
    #     V['halfp'] = 'No'
    #     V['halfp_orderNumber'] = ""
    # elif V['halfp'] == 'No':
    #     for trade in trade_history:
    #         if V['halfp_orderNumber'] == trade['orderNumber']:
    #             V['halfp'] = 'Yes'
    #             break


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
        now_rate = get_market_rate()

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


def get_pause_menu(L):
    answer = raw_input("Are You Sure You Want To Quit?? (y/n)").rstrip()
    if answer == 'y' or answer == 'Y':
        print("Exiting...")
        T.cancel(V['currencyPair'], V['orderNumber'])
        sys.exit()
    elif answer == 'n' or answer == 'N':
        del L[:]
        thread.start_new_thread(wait_for_enter, (L,))
    else:
        print("Not a valid answer...")


def run():
    update_variables()
    get_variables()
    EventLoop()
    print("Complete")



def get_market_rate():
    return Money(
        PV['ticker'][V['currencyPair']]['last']
    )



def get_variables():
    global V

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
        '--profit',   'profit'
    ])
    args = myargs.getargs()

    if '-c' in args or '--currency' in args:
        V['base_currency'] = args['base'].rstrip().upper()
        V['currency']      = args['currency'].rstrip().upper()
        V['currencyPair']  = "{}_{}".format(V['base_currency'], V['currency'])
    else:
        raise Exception("You Need Currency Pair Set!")

    if '-a' in args or '--amount' in args:
        V['amount_usd'] = Money(args['amount'].rstrip())
    else:
        V['amount_usd'] = Money(10)

    if '-r' in args or '--buy-rate' in args:
        V['rate'] = Money(args['buy_rate'].rstrip())
    else:
        V['rate'] = get_market_rate()
    V['buy_rate'] = Money(float(str(V['rate'])))

    if '-p' in args or '--profit' in args:
        V['profit'] = Money(args['profit'].rstrip())
    else:
        V['profit'] = Money(1)

    if '-x' in args or '--risk' in args:
        V['risk'] = Money(args['risk'].rstrip())
    else:
        V['risk'] = Money(2)



def delay():
    sleep(LOOP_DELAY/1000)

def wait_for_enter(L):
    x = raw_input().rstrip()
    L.append(None)



if __name__ == "__main__": run()

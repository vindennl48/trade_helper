from tradeapi import *
from money import *
from time import sleep
import thread, os

T           = Poloniex()
LOOP_DELAY  = 200    #in milliseconds
i           = 0

def run():
    try:
        global i
        i+=1
        json_raw = {}

        get_ticker(json_raw)
        get_balance(json_raw)
        get_open_orders(json_raw)
        get_trade_history(json_raw)
        get_update_id(json_raw)

        with open('.data.dat',"w") as f:
            f.write(json_pretty(json_raw))

        os.system('clear')
        print("Updated: {} times".format(i))
    except:
        print("connection issues..")



def get_ticker(json_raw):
    json_raw['ticker'] = T.returnTicker()

def get_balance(json_raw):
    json_raw['balance'] = T.returnBalances()

def get_open_orders(json_raw):
    json_raw['open_orders'] = T.returnOpenOrders('all')

def get_trade_history(json_raw):
    json_raw['trade_history'] = T.returnTradeHistory('all')

def get_update_id(json_raw):
    json_raw['update_id'] = str(i)

def json_pretty(json_obj):
    return json.dumps(json_obj, indent=4, separators=(',', ': '))



def delay():
    sleep(LOOP_DELAY/1000)

def wait_for_enter(L):
    x = raw_input().rstrip()
    L.append(None)

if __name__ == "__main__":

    L = []
    thread.start_new_thread(wait_for_enter, (L,))

    while True:                             # EVENT LOOP START
        if L:
            break
        else: run()
        delay()                             # EVENT LOOP END

    print("Exiting..")

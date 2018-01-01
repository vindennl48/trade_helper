from time import sleep
import sys, thread

def delay(delay=1000):
    sleep(delay/1000)

def wait_for_enter(L):
    x = raw_input().rstrip()
    L.append(None)

def get_pause_menu(V,T,L):
    answer = raw_input("Are You Sure You Want To Quit?? (y/n)").rstrip()
    if answer == 'y' or answer == 'Y':
        print("Exiting...")
        try:
            T.cancel(V['currencyPair'], V['orderNumber'])
        except: pass
        sys.exit()
    elif answer == 'n' or answer == 'N':
        del L[:]
        thread.start_new_thread(wait_for_enter, (L,))
    else:
        print("Not a valid answer...")


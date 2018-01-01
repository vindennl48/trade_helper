from tradeapi         import *
from update_variables import *
from get_variables    import *
from event_loop       import *
from misc_funcs       import *


def run():
    T  = Poloniex()    # Trading API
    PV = {}            # Poloniex Variables
    V  = {}            # Trade Variables

    # initialize
    PV = update_variables()
    V  = get_variables(PV,V)

    # run main loop
    EventLoop(PV,V,T)
    print("Complete")



if __name__ == "__main__": run()

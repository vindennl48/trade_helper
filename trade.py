from tradeapi         import *
from get_variables    import *
from event_loop       import *
from misc_funcs       import *


def run():
    T  = Poloniex()    # Trading API
    PV = {}            # Poloniex Variables
    V  = {}            # Trade Variables

    # initialize
    #V = update_ticker(V,T)
    V  = get_variables(V,T)

    # run main loop
    EventLoop(PV,V,T)
    print("Complete")



if __name__ == "__main__": run()

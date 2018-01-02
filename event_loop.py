from   update_variables import *
from   check_status     import *
from   set_open_trade   import *
from   print_screen     import *
from   pause_menu       import *
from   get_variables    import *
from   buy_order        import *
from   sell_process     import *
import thread

i = 0

def EventLoop(PV,V,T):
    status = 0
    
    # for pause menu
    L = []
    thread.start_new_thread(wait_for_enter, (L,))
    #############################################

    while True:             # MAIN EVENT LOOP
        if L:
            get_pause_menu(V,T,L)
        else:
            # constantly keep variables updated
            PV = update_variables()


            # 0: initialization ############################################
            if status == 0:
                V = get_variables(PV,V)    # terminal arguments and settings
                V['position'] = '....'      # unknown status
                status = 1                  # proceed to next step


            # 1: create buy order ##########################################
            elif status == 1:
                V = create_buy_order(V,T)   # create open buy order
                status = 2                  # proceed to next step


            # 2: confirm buy open order ####################################
            elif status == 2:
                if confirm_buy_open_order(PV,V): # when open order is confirmed
                    V['position'] = 'open buy'
                    status = 3              # proceed to next step


            # 3: confirm buy closed order ###################################
            elif status == 3:
                if confirm_buy_close_order(PV,V):
                    V = get_fee(PV,V)
                    V['position'] = 'bought'
                    V['start_profit'] = True
                    status = 4


            # 4: stoploss watch #############################################
            elif status == 4:
                V['position'] = 'watch stop'
                if hit_stoploss(PV,V):
                    V = sell_now(PV,V,T)
                    status = -99
                elif not watching_stoploss(PV,V):
                    status = 5

            # 5: set sell order #############################################
            elif status == 5:
                V = create_half_p(V,T)
                V = create_sell_order(PV,V,T)
                status = 6

            # 6: confirm sell order #########################################
            elif status == 6:
                V['position'] = '.....'
                if confirm_open_sell_order(PV,V) and \
                    confirm_open_halfp_order(PV,V):
                    status = 7

            # 7: full sell watch ############################################
            elif status == 7:
                V['position'] = 'watch sell'
                if confirm_sell_close_order(PV,V):
                    status = 99
                    V['position'] = 'sold'
                elif V['halfp'] == 'No' and \
                    confirm_halfp_close_order(PV,V):
                    V['halfp'] = 'Yes'
                elif not watching_full(PV,V):
                    cancel_full_open_order(PV,V,T)
                    cancel_halfp_open_order(PV,V,T)
                    status = 4

            elif status == 99:
                print("Success!")
                sys.exit()
            elif status == -99:
                print("You lost..")
                sys.exit()


            else:
                raise Exception("Status Level Unknown!")

            V = set_now_profit(PV,V)
            print_screen(PV,V)          # display data on screen

        delay(1000)




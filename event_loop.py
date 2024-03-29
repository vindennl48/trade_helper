from   update_ticker    import *
from   check_status     import *
from   set_open_trade   import *
from   print_screen     import *
from   pause_menu       import *
from   get_variables    import *
from   buy_order        import *
from   sell_process     import *
from   misc_funcs       import *
import thread


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
            V = update_ticker(V,T)


            # 0: initialization ############################################
            if status == 0:
                V = get_variables(V,T)      # terminal arguments and settings
                V['position'] = '....'      # unknown status
                status = 1                  # proceed to next step


            # 1: create buy order ##########################################
            elif status == 1:
                V = create_order('buy',V,T)   # create open buy order
                V['position'] = 'open buy'
                status = 3                    # proceed to next step

            # 3: confirm buy closed order ###################################
            elif status == 3:
                if confirm_close_order(V,T):
                    V = get_buy_fee(V,T)
                    V['position'] = 'bought'
                    V['start_profit'] = True
                    status = 4


            # 4: stoploss watch #############################################
            elif status == 4:
                V['position'] = 'watch stop'
                if hit_stoploss(V):
                    V = sell_now(V,T)
                    status = -99
                elif not watching_stoploss(V):
                    status = 5

            # 5: set sell order #############################################
            elif status == 5:
                while True:
                    try:
                        V = create_half_p(V,T)
                        break
                    except:
                        print("ERROR: Either an input data error, or a connection error... Trying again..")
                        sleep(2)

                while True:
                    try:
                        V = create_order('sell',V,T)
                        break
                    except:
                            print("ERROR: Either an input data error, or a connection error... Trying again..")
                            sleep(2)

                V['position'] = 'watch sell'
                status = 7

            # 7: full sell watch ############################################
            elif status == 7:
                if confirm_close_order(V,T):
                    status = 99
                    V['position'] = 'sold'
                elif V['halfp'] == 'No' and \
                    confirm_halfp_close_order(V,T):
                    V['halfp'] = 'Yes'
                elif not watching_full(V):
                    cancel_full_open_order(V,T)
                    cancel_halfp_open_order(V,T)
                    status = 4

            elif status == 99:
                print("Success!")
                sys.exit()
            elif status == -99:
                print("You lost..")
                sys.exit()


            else:
                raise Exception("Status Level Unknown!")

            V = set_now_profit(V)
            print_screen(V)          # display data on screen

        V['update_id'] += 1
        delay(1000)




from screen_table import st_build
from misc_funcs import *
import os

def print_screen(PV,V):
    os.system('clear')
    st_build(
        [8,9,8,8,10,8,5,10],
        [
            [ 
                ['Amount'],
                ['Buy Price'],
                ['Stop'],
                ['Target'],
                ['Now Price'],
                ['Profit'],
                ['HalfP'],
                ['Position']
            ],
            [ 
                [str(V['amount_usd'])   ,'right'],
                [str(V['buy_rate'])     ,'right'],
                [str(V['sl_rate'])      ,'right'],
                [str(V['full_rate'])    ,'right'],
                [str(get_market_rate(PV,V)) ,'right'],
                [str(V['now_profit'])   ,'right'],
                [str(V['halfp'])        ,'right'],
                [str(V['position'])     ,'right']
            ],
            [
                ['Risk'],
                #['Flip'],
                [''],
                ['Loss'],
                ['Profit'],
                ['halfp r'],
                [''],
                [''],
                ['']
            ],
            [ 
                [str(V['risk'])      ,'right'],
                #[str(V['buy_rate']*1.01),'right'],
                [''],
                [str(V['profit']/-2) ,'right'],
                [str(V['profit'])    ,'right'],
                [str(V['halfp_rate']) ,'right'],
                [''],
                [''],
                ['']
            ],
        ]
    )
    print("Update ID: {}".format(PV['update_id']))
    print("Debug | Order Id: {}".format(V['orderNumber']))

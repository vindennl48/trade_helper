from screen_table import st_build
from misc_funcs import *
import os

def print_screen(V):
    os.system('clear')

    if V['halfp_active']:
        halfp = 'Yes'
    else:
        halfp = 'No'

    st_build(
        [8,9,8,8,10,8,6,10],
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
                [str(V['ticker']) ,'right'],
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
                [''],
                [''],
                ['Active'],
                ['']
            ],
            [ 
                [str(V['risk'])      ,'right'],
                #[str(V['buy_rate']*1.01),'right'],
                [''],
                [str(V['profit']/V['risk']*-1) ,'right'],
                [str(V['profit'])    ,'right'],
                [''],
                [''],
                [halfp               ,'right'],
                ['']
            ],
        ]
    )
    print("Update ID: {}".format(V['update_id']))
    print("Debug | Order Id: {}".format(V['orderNumber']))

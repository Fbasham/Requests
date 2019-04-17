# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:51:18 2019
@author: Fbasham
"""

import requests
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


import requests
import pandas as pd
import matplotlib.pyplot as plt


def top_coins(top, timeframe):
    
    coin_url = 'https://api.coinranking.com/v1/public/coins'
    r = requests.get(coin_url)

    alias = {}
    for i in r.json()['data']['coins'][:top]:
        alias[i['id']] = i['name']


    df = pd.DataFrame()
    for coin_id, coin_name in alias.items():

        url = f'https://api.coinranking.com/v1/public/coin/{coin_id}/history/{timeframe}'
        r = requests.get(url)
       
        frame = pd.DataFrame(r.json()['data']['history']).astype(float).set_index('timestamp')
        frame.columns = [coin_name]
        frame.index = pd.to_datetime(frame.index, unit='ms')
        frame = frame.resample('D').mean()
   
        if df.empty:
            df = frame
        else:
            df = df.join(frame, how='outer')
            
    df = df.dropna()
    #normalized_df=(df-df.mean())/df.std()
    normalized_df=(df-df.min())/(df.max()-df.min())
    normalized_df.plot()
    plt.show()


##Example function call: 
top_coins(3, '5y')

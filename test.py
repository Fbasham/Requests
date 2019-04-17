import requests
from datetime import datetime
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
        dates = []
        prices = []

        for item in r.json()['data']['history']:
            time = datetime.fromtimestamp(item['timestamp']/1000)
            price = item['price']
            dates.append(time)
            prices.append(price)

        frame = pd.DataFrame({coin_name: prices}, index=dates).astype(float)
        frame = frame.resample('D').mean()
   
        if df.empty:
            df = frame
        else:
            df = df.join(frame, how='outer')

    df = df.dropna()
    normalized_df=(df-df.min())/(df.max()-df.min())
    normalized_df.plot()

    plt.show()


##Example function call: 
top_coins(25, '5y')

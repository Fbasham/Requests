import requests
import pandas as pd
import matplotlib.pyplot as plt


def get_rate(country1, country2, start, end): 

    url = 'https://api.exchangeratesapi.io/history'
    payload = {'base': country1, 'symbols': country2, 'start_at': start, 'end_at': end}
    r = requests.get(url, params=payload)

    dates = []
    exchange = []
    for date, rate in sorted(r.json()['rates'].items()):
        dates.append(date)
        exchange.append(rate[country2])


    df = pd.DataFrame({'Date': dates,
                       'Exchange': exchange}).set_index('Date')

    df.plot(title=f'{country1} to {country2}')
    plt.xlabel(xlabel='Date')
    plt.ylabel(ylabel=f'{country1} per {country2}')
    plt.show()


get_rate('CAD', 'USD', '1999-01-01', '2019-04-13')

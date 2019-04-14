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
        exchange.append(rate)

    df = pd.DataFrame(exchange, index=dates)
 
    df.plot(title=f'{country1} to {country2}')
    plt.xlabel(xlabel='Date')
    plt.ylabel(ylabel=f'{country1} per {country2}')
    plt.show()


def get_rates(base, countries, start, end):

    url = 'https://api.exchangeratesapi.io/history'
    payload = {'base': base, 'symbols': countries, 'start_at': start, 'end_at': end}
    r = requests.get(url, params=payload)

    dates = []
    exchange = []
    for date, rates in sorted(r.json()['rates'].items()):
        dates.append(date)
        exchange.append(rates)

    df = pd.DataFrame(exchange, index=dates)

    df.plot(title=f'{base} to {", ".join(countries)}')
    plt.xlabel(xlabel='Date')
    plt.ylabel(ylabel=f'{base}')    
    plt.show()


##Sample input:
get_rate('CAD', 'USD', '2018-01-01', '2019-04-13')
get_rates('USD', ['CAD', 'GBP', 'EUR'],'1990-04-01', '2019-04-13')

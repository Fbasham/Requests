# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:29:01 2019

@author: Fbasham
"""

import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://restcountries.eu/rest/v2/all'
r = requests.get(url)

with open('Countries.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    headers = ['name', 'region', 'subregion', 'capital', 'area', 'population']
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    
    rows = []
    for item in r.json():
        name = item['name']
        region = item['region']
        subregion = item['subregion']
        capital = item['capital']
        area = item['area']
        population = item['population']
        row = [name, region, subregion, capital, area, population]
        rows.append(row)
        writer.writerow(dict(zip(headers,row)))
    
    df = pd.DataFrame(rows, columns=headers)
    df['density'] = df['population']/df['area']
    df = df.groupby(['subregion']).mean()
    df[['density']].plot(kind='barh')
    plt.show()

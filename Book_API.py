# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:59:51 2019

@author: Fbasham
"""

import requests
import datetime
import csv

''' The purpose of this script is to demonstrate how to connect to an API using the Requests library,
    extract the information we want from the JSON response, and save down to a csv file '''

today = datetime.date.today().strftime('%d %m %Y')
day, month ,year = today.split()

payload = {'timefirst': f'{year}-{month}-01', 'timelast': f'{year}-{month}-{day}', 'limit1': '1000'}
r = requests.get('http://libgen.io/json.php?mode=last', params = payload)

with open('Books API.csv', 'w', newline = '', encoding='utf-8-sig') as csvfile:
    headers = ['id', 'title', 'year', 'pages']
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for book in r.json():
        writer.writerow(dict(zip(headers, [book[i] for i in headers])))
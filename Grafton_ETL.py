# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 08:55:42 2019

@author: Fbasham
"""

from bs4 import BeautifulSoup
import csv
import requests
import datetime


with requests.Session() as s:
 
    login = {'sUsrNam': 'User', 'sUsrPwd': 'Password'}    
    r = s.post('http://website.com/login?', data = login)
    
    day, month, year = datetime.datetime.today().strftime('%d/%m/%Y').split('/')   
    payload = {'dStrTim': f'{year}-{month}-01',
               'dEndTim': f'{year}-{month}-{day}'}
    
    report = s.post('http://website.com/reports?iRptIdx=10', params = payload)
    

    soup = BeautifulSoup(report.content, 'lxml')
    div = soup.find_all('div')

    x = [i.span.text.replace('\xa0',' ') if i.span else None for i in div]

    # create a list of the indexes of all None types in x
    idx = [i for i, _ in enumerate(x) if _ is None]


    with open('test.csv', 'w', newline='') as csvfile:
        
        headers = ['Inventory', 'Net', 'End Time', 'Driver', 'Carrier', 'Consignee',
                   'BOL2', 'BOL', 'Supplier', 'Railcar']

        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        
        '''
        create a list of lists using slices between the None type indexes
        if len of row is 7 or 9, it is either a truck lifting or rail offload (i.e. useful rows)
        insert '' values at given index to normalize row length and to match headers
        '''
        for i in range(len(idx)-1):
            row = x[idx[i]+1:idx[i+1]]
            if len(row) in [7,9]:
                if len(row) is 7:
                    for j in range(3):
                        row.insert(3,'')
                else:
                    row.insert(-3,'')

                writer.writerow(dict(zip(headers,row)))



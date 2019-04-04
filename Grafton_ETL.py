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

    #create a list of the indexes of all None types in x:
    idx = [i for i, _ in enumerate(x) if _ is None]


    with open('test.csv', 'w', newline='') as csvfile:
        
        headers = ['Type','Inventory', 'Net', 'End Time', 'Driver', 'Carrier',
                   'Consignee', 'BOL', 'GVM BOL', 'Supplier', 'Railcar']

        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        
        rows = []
        #create a list of lists using slices between the None type indexes:
        for i in range(len(idx)-1):
            row = x[idx[i]+1:idx[i+1]]
            if len(row) in [7,9]:
                if len(row) is 7:
                    for j in range(3):
                        row.insert(3,'')
                    row.insert(0,'Rail')
                else:
                    row.insert(-3,'')
                    row.insert(0,'Truck')
                            
                writer.writerow(dict(zip(headers,row)))
                
                #used creating a Dataframe with Pandas:
                rows.append(row)

              
        #alternative to above using Pandas to modify the data and output to csv file:
        alias = {'1000': 'NGL Supply', '1001': 'Patriot', '2001': 'Ray Energy', '3001': 'NGL Wholesale'}
        df = pd.DataFrame(rows, columns=headers)
        df = df[['Type', 'Supplier', 'End Time', 'BOL', 'GVM BOL', 'Railcar', 'Net', 'Inventory']]
        df = df.sort_values(['Supplier', 'Type'])
        df['Supplier'] = df['Supplier'].map(alias)
        df.to_csv('Grafton Inventory Report.csv', index=False)

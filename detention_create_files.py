# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 08:14:34 2019

@author: Fbasham
"""

import pandas as pd
from datetime import datetime, timedelta
import os

day, month, year = (datetime.today() - timedelta(15)).strftime('%d %m %Y').split()
path = f'H:\TDunlop\Rail\Detention\{year}\{year}.{month}'

try:
    os.makedirs(path)
except Exception as e:
    repr(e)

df = pd.read_excel(f'{path}\{year}.{month} - Detention Master Workbook.xlsx', sheet_name='Geo')
df = df.dropna(subset=['Consignee'])
df = df[df['Total Charges'] > 0]


df = df.groupby('Consignee')

for consignee, items in df:
    consignee_dir = f'{path}\{consignee}'
    try: 
        os.makedirs(f'{consignee_dir}')
    except Exception as e:
        repr(e)
    
    headers = ['Consignee', 'Railcar', 'Origin.1', 'Destination.1', 'Actual Departed', 'Destn Arrived', 
               'Actual Arrived', 'Charge Start', 'Charge End', 'Lay days', 'Free Days', 'Total Charge Days',
               'Tier 1 Days', 'Tier 2 Days', 'Tier 1 Charges', 'Tier 2 Charges', 'Total Charges']
   
    frame = items[headers]
    total = frame[['Total Charges']].sum().rename('Total')
    frame = frame.append(total)
    
    frame.to_csv(f'{consignee_dir}\{year}.{month} - {consignee} Detention.csv', index=False)
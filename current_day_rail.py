# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 08:14:34 2019

@author: Fbasham
"""

import pandas as pd
from datetime import datetime


day, month, year = datetime.today().strftime('%d %m %Y').split()

##
df = pd.read_csv('P:\E1Report\FB Reports\current day rail.csv')
df = df.rename(columns={'Car/Truck': 'Railcar'})
df['Ship Date'] = pd.to_datetime(df['Ship Date']).dt.strftime('%d/%m/%Y')
df['key'] = df['Ship Date'] + df['Railcar'].str[:4] + df['Railcar'].str[4:].str.zfill(6)

##
df_trace = pd.read_excel(r'H:\Logistics\Trace\Geometrix Logistics Trace\Geometrix Trace Dump.xlsx')
df_trace = df_trace[['Railcar', 'L_E', 'Actual Departed', 'Contract Code', 'Location', 'Destination']]
df_trace = df_trace.rename(columns={'Actual Departed': 'Ship Date'})
df_trace['Ship Date'] = pd.to_datetime(df_trace['Ship Date']).dt.strftime('%d/%m/%Y')
df_trace['key'] = df_trace['Ship Date'] + df_trace['Railcar']

##
dff = df.merge(df_trace[['L_E', 'Location', 'Destination', 'key']], how='left', on='key', suffixes= (' E1', ' Geo'),  sort=False)

##
df_fill = pd.read_csv(f'{year}.{month} - Current Day Rail Merged with Geo.csv')
dff['L_E'] = dff['L_E'].fillna(df_fill['L_E'])

#def loading_correct(row):
#    date, loading_state = row
#    if date == f'{day}/{month}/{year}' and loading_state == 'L':
#        return 'E'
#    else:
#        return loading_state
#
#
#dff['Corrected Loading State'] = dff[['Ship Date', 'L_E']].apply(loading_correct, axis=1)

##
dff.to_csv(f'{year}.{month} - Current Day Rail Merged with Geo.csv', index = False)
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 08:14:34 2019

@author: Fbasham
"""

import pandas as pd
import grafton_request
import datetime


# Request new data from GVM using the main function from grafton_request module
grafton_request.main()

# Save new trace to historical Grafton trace report (essentially appending new info with using a context manager)
old = pd.read_csv(r'Grafton Trace.csv')
old['Actual Departed'] = pd.to_datetime(old['Actual Departed']).dt.date
dff = pd.read_excel(r'H:\Logistics\Trace\Geometrix Logistics Trace\Geometrix Trace Dump.xlsx')
dff['Destination'] = dff['Destination'] = dff['Destination'].fillna('No Location Specified')
dff = dff[dff['Destination'].str.contains('Graf')]
dff['Actual Departed'] = pd.to_datetime(dff['Actual Departed']).dt.date
new = pd.concat([old,dff], sort=False)
new = new.drop_duplicates(['Railcar', 'Actual Departed', 'Origin'])
new.to_csv(r'Grafton Trace.csv', index=False)


# Transaction detail report dataframe and cleanup
df_trans = pd.read_csv(r'P:\E1Report\FB Reports\Grafton E1 Transaction Detail by Origin Report.csv')
df_trans['Car/Truck'] = df_trans['Car/Truck'].str[:4] + df_trans['Car/Truck'].str[4:].str.zfill(6)
df_trans = df_trans[['Origin', 'Deal/Contract      Line', 'Car/Truck', 'Origin Quantity', 'Ship Date', 'BOL/Ticket']]
df_trans.columns = ['Origin', 'Contract', 'Railcar', 'BOL Volume', 'Ship Date', 'BOL']
df_trans['Ship Date'] = pd.to_datetime(df_trans['Ship Date']).dt.date


# Trace dump dataframe and cleanup
df_trace = pd.read_csv(r'Grafton Trace.csv')
df_trace['Actual Departed'] = pd.to_datetime(df_trace['Actual Departed']).dt.date
df_trace['Destination'] = df_trace['Destination'].fillna('No Location Specified')
df_trace = df_trace[df_trace['Destination'].str.contains('Graf')]
df_trace = df_trace[['Railcar', 'L_E', 'Location', 'Actual Departed', 'Origin', 'Fleet', 'Owner']]
df_trace.columns = ['Railcar', 'L_E', 'Location', 'Ship Date', 'Origin', 'Fleet', 'Owner']


# Function to create a unique key for merging reports                    
def create_key(row):
    railcar, ship_date = row
    ship_date = ship_date.strftime('%m%Y')
    return f'{ship_date}{railcar}'

for frame in [df_trans, df_trace]:
    frame['key'] = frame[['Railcar', 'Ship Date']].apply(create_key, axis=1)

df_trans = df_trans.set_index('key')
df_trace = df_trace.set_index('key')


# Merge trace and transaction detail reports
df = df_trace.merge(df_trans, how='outer', on=['key', 'Railcar'], suffixes=('_geo', '_E1'))
   
                                                                                         
# Create dataframe for GVM report and manipulate it before merging 
df_gvm = pd.read_csv(r'Grafton Inventory Report.csv', thousands=',')
df_gvm = df_gvm[(df_gvm['Supplier'].isin(['NGL Supply', 'Patriot'])) & (df_gvm['Type']=='Rail')]
df_gvm['Railcar'] = df_gvm['Railcar'].str[:4] + df_gvm['Railcar'].str[4:].str.zfill(6)
df_gvm['Net'] = pd.to_numeric(df_gvm['Net'])
df_gvm['End Time'] = pd.to_datetime(df_gvm['End Time'], yearfirst=True).dt.date
df_gvm = df_gvm[['Net', 'BOL', 'Railcar', 'End Time', 'Supplier']]


# Merge GVM report with trace and transcation detail reports
df = df.merge(df_gvm, how='outer', on=['Railcar', 'BOL'])
df = df[['Railcar', 'Location','L_E', 'Fleet','Origin_geo', 'Origin_E1', 'Ship Date_geo', 'Ship Date_E1',
         'BOL', 'BOL Volume', 'Net', 'End Time']]
                                 

# Find all rows where there are duplicate BOLs and return as a dataframe
duplicates = df[df.duplicated(subset='BOL', keep=False) == True]
duplicates = duplicates[['BOL', 'Net', 'End Time']].dropna().values.tolist()

for bol, volume, date in duplicates:
    df.loc[df['BOL']==bol, ['Net', 'End Time']] = volume, date

df = df.drop_duplicates('BOL')

day, month, year = datetime.datetime.today().strftime('%d %m %Y').split()
df.to_csv(f'{year}.{month} - Grafton_Reconciliation.csv', index=False)   

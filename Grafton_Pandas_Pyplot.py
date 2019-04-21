"""
Created on Wed Apr  3 08:55:42 2019

@author: Fbasham
"""

import pandas as pd
from matplotlib import pyplot as plt
import datetime
import grafton_request


df = pd.read_csv(r'H:\FBasham\Python (do not delete code please)\Grafton Inventory Report.csv', thousands=',')

all_suppliers = df['Supplier'].unique()
default = ['NGL Supply', 'Patriot']
def grafton(arr, new_data=False):
   
    #request new data if True.  This should use threading to wait until request is obtained, but this works for quick immplementation
    if new_data is True:
        try:
            grafton_request.main()
        except Exception as e:
            print(e)
            print('Using old data if available in Fbasham\'s folder')
                 
        
    #Convert to useful units of measure and define dataframe of DateIndexes for current month, used for extending data to current day
    df['Inventory'] = df['Inventory'].apply(pd.to_numeric)
    df['End Time'] = pd.to_datetime(df['End Time'], yearfirst=True)
    today = datetime.date.today()
    period = pd.Period(today, freq='M')
    dates = pd.date_range(start=period.start_time, end=today, freq='D')


    def supplier_data(supplier):
        ''' returns x-axis cooridnates and grouped volumes by truck and rail respecitively'''
        day_inventory = df[df['Supplier'] == supplier][['Inventory']].groupby(df['End Time'].dt.date).last()
        sum_rail = df[(df['Supplier'] == supplier) & (df['Type'] == 'Rail')][['Net']].groupby(df['End Time'].dt.date).sum()
        sum_truck = df[(df['Supplier'] == supplier) & (df['Type'] == 'Truck')][['Net']].groupby(df['End Time'].dt.date).sum().abs()
        
        #Extend the above dataframes to current date and nornmalize to 0 if no liftings/offloads in report:
        day_inventory = day_inventory.reindex(dates).bfill().ffill()
        sum_rail = sum_rail.reindex(dates).fillna(0)
        sum_truck = sum_truck.reindex(dates).fillna(0)  
        return [day_inventory, sum_rail, sum_truck]


    def inventory(arr):
        ''' Generate dataframe of supplier inventory, n defaults to all suppliers at the terminal if no kwargs passed.
            The 'dates' dataframe is created in order to increment current month's date if no inventory is reported from
            in the downloaded reports. Placeholder column needs to exist, but doesn't impact inventory calc '''
        inventories = [supplier_data(i)[0] for i in arr]
        combined_inventory = pd.concat(inventories, axis=1, sort=True)
        combined_inventory.columns = arr 
        combined_inventory['Inventory'] = combine_inventory.sum(axis=1) 
        return combined_inventory


    def rail_offloads(arr):
        offloads = [supplier_data(i)[1] for i in arr]
        combined_offloads = pd.concat(offloads, axis=1, sort=True)  
        combined_offloads.columns = arr    
        return combined_offloads


    def truck_liftings(arr):
        liftings = [supplier_data(i)[2] for i in arr]
        combined_liftings = pd.concat(liftings, axis=1, sort=True)
        combined_liftings.columns = arr 
        return combined_liftings


    fig, axes = plt.subplots(nrows=3, ncols=1, squeeze=False, sharex=True)
    inventory(arr)[['Inventory']].plot(ax=axes[0,0], title='Inventory', marker='*', style='--')
    rail_offloads(arr).plot(ax=axes[1,0], title='Rail Offloads', marker='.', style=':')
    truck_liftings(arr).plot(ax=axes[2,0], title='Truck Liftings', marker='x', style=':')
    plt.show()
    

if __name__ == '__main__':    
    grafton(default, new_data=True)
    grafton(all_suppliers, new_data=True)

import pandas as pd
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
import datetime


df = pd.read_csv('Grafton Inventory Report.csv', thousands=',')

all_suppliers = list(set(df['Supplier']))
default = ['NGL Supply', 'Patriot']
def grafton(n = default):
    
    #Convert to useful units of measure and define dataframe of DateIndexes for current month, used for extending data to current day
    df['Inventory'] = df['Inventory'].apply(pd.to_numeric)
    df['End Time'] = pd.to_datetime(df['End Time'], yearfirst=True)
    today = datetime.date.today()
    period = pd.Period(today, freq='M')
    d = pd.DatetimeIndex(start=period.start_time, end=today, freq='D')
    dates = pd.DataFrame({'placeholder': 0}, index=d.date)


    def supplier_data(supplier):
        ''' returns x-axis cooridnates and grouped volumes by truck and rail respecitively'''
        x_mean_date = df[df['Supplier'] == supplier].groupby(df['End Time'].dt.date).mean()
        x_sum_rail = df[(df['Supplier'] == supplier) & (df['Type'] == 'Rail')].groupby(df['End Time'].dt.date).sum()
        x_sum_truck = df[(df['Supplier'] == supplier) & (df['Type'] == 'Truck')].groupby(df['End Time'].dt.date).sum().abs()
        
        #Extend the above dataframes to current date and nornmalize to 0 if no liftings/offloads in report:
        x_sum_rail = pd.concat([x_sum_rail, dates], axis=1, sort=True).fillna(0)
        x_sum_rail['Net'] = x_sum_rail['Net'] + x_sum_rail['placeholder']
        x_sum_truck = pd.concat([x_sum_truck, dates], axis=1, sort=True).fillna(0)
        x_sum_truck['Net'] = x_sum_truck['Net'] + x_sum_truck['placeholder']
        
        return [x_mean_date, x_sum_rail, x_sum_truck]


    def inventory(n):
        ''' Generate dataframe of supplier inventory, n defaults to all suppliers at the terminal if no kwargs passed.
            The 'dates' dataframe is created in order to increment current month's date if no inventory is reported from
            in the downloaded reports. Placeholder column needs to exist, but doesn't impact inventory calc '''
        inventories = [supplier_data(i)[0]['Inventory'] for i in n]
        combined_inventory = pd.concat(inventories + [dates], axis=1, sort=True)
        combined_inventory['Inventory'] = combined_inventory.bfill().ffill()
        combined_inventory.columns = n + ['placeholder']
        combined_inventory['Inventory'] = sum([combined_inventory[i] for i in n])
        
        return combined_inventory

    
    #Begin Plotting
    pd.plotting.register_matplotlib_converters(explicit=True)
    fig, ax = plt.subplots()
    plt.plot(inventory(n).index, inventory(n)['Inventory'], marker='.',markersize=7, linewidth=0.75)
    for s in n:
        plt.plot(supplier_data(s)[1].index, supplier_data(s)[1]['Net'], marker='.',markersize=7, linewidth=0.75)
        plt.plot(supplier_data(s)[2].index, supplier_data(s)[2]['Net'], marker='.',markersize=7, linewidth=0.75)
    plt.title(label='Grafton Inventory Summary')
    plt.xlabel('Time')
    plt.ylabel('USG')
    plt.legend(['Inventory'] + [f'{s} Rail' for s in n] + [f'{s} Truck' for s in n], bbox_to_anchor=(1,1),
               bbox_transform=fig.transFigure, ncol=(2*len(n)//2 + 1), loc='upper right', fontsize='small')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.tick_params(axis='x', labelsize=8)
    plt.xticks(rotation = 25)


    #Used for generating marker annotations
    marker_arr = [inventory(n)['Inventory']] + [supplier_data(s)[i]['Net'] for s in n for i in [1,2]]
    for i, frame in enumerate(marker_arr):
        for j, txt in enumerate(frame):
            plt.annotate(f'{int(txt/1000)}k', (frame.index[j], frame.values[j]+2000)).set_fontsize(7.5)

    plt.show()

if __name__ == '__main__':    
    grafton()

import pandas as pd
from matplotlib import pyplot as plt
import datetime


df = pd.read_csv('Grafton Inventory Report.csv', thousands=',')

#Convert to useful units of measure
df['Inventory'] = df['Inventory'].apply(pd.to_numeric)
df['End Time'] = pd.to_datetime(df['End Time'], yearfirst=True)

def supplier_data(supplier):
    x_mean_date = df[df['Supplier'] == supplier].groupby(df['End Time'].dt.date).mean()
    x_sum_rail = df[(df['Supplier'] == supplier) & (df['Type'] == 'Rail')].groupby(df['End Time'].dt.date).sum()
    x_sum_truck = df[(df['Supplier'] == supplier) & (df['Type'] == 'Truck')].groupby(df['End Time'].dt.date).sum().abs()    
    return [x_mean_date, x_sum_rail, x_sum_truck]


#Define supplier variables
x1,x3,x4 = supplier_data('NGL Supply')
x2,x5,x6 = supplier_data('Patriot')


#Inventory at current time
inv_df = pd.concat([x1['Inventory'],x2['Inventory']], axis=1, sort=True)
inv_df['Inventory'] = inv_df['Inventory'].bfill().ffill()
inv_df.columns = ['NGL', 'Patriot']
inv_df['Inventory'] = inv_df['NGL'] + inv_df['Patriot']
inv_xtime = inv_df.index


#Begin Plotting
pd.plotting.register_matplotlib_converters(explicit=True)
plt.plot(inv_xtime, inv_df['Inventory'], x3.index, x3['Net'], x4.index, x4['Net'], x5.index, x5['Net'], x6.index, x6['Net'],
         marker='o',markersize=3, linewidth=0.75)
plt.title(label='Grafton Inventory Summary')
plt.xlabel('Time')
plt.ylabel('USG')
plt.legend(['Inventory', 'NGL Rail', 'NGL Truck', 'PATRIOT Rail', 'PATRIOT Truck'], loc='best', fontsize='small')


#Used for generating marker annotations
marker_arr = [inv_df['Inventory'], x3['Net'], x4['Net'], x5['Net'], x6['Net']]
for i, frame in enumerate(marker_arr):
    for j, txt in enumerate(frame):
        plt.annotate(f'{int(txt/1000)}k', (frame.index[j], frame.values[j]+2000)).set_fontsize(7.5)

plt.show()    

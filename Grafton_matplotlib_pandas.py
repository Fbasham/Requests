import pandas as pd
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
import datetime



df = pd.read_csv('Grafton Inventory Report.csv', thousands=',')

#Convert to useful units of measure
df['Inventory'] = df['Inventory'].apply(pd.to_numeric)
df['End Time'] = pd.to_datetime(df['End Time'], yearfirst=True)

def supplier_data(supplier):
    ''' returns x-axis cooridnates and grouped volumes by truck and rail respecitively'''
    x_mean_date = df[df['Supplier'] == supplier].groupby(df['End Time'].dt.date).mean()
    x_sum_rail = df[(df['Supplier'] == supplier) & (df['Type'] == 'Rail')].groupby(df['End Time'].dt.date).sum()
    x_sum_truck = df[(df['Supplier'] == supplier) & (df['Type'] == 'Truck')].groupby(df['End Time'].dt.date).sum().abs()    
    return [x_mean_date, x_sum_rail, x_sum_truck]


names = list(set(df['Supplier']))
def inventory(n = names):
    ''' generate dataframe of supplier inventory, n defaults to all suppliers if no kwargs passes'''
    inventories = [supplier_data(i)[0]['Inventory'] for i in n]
    combined_inventory = pd.concat(inventories, axis=1, sort=True)
    combined_inventory['Inventory'] = combined_inventory.bfill().ffill()
    combined_inventory.columns = n
    combined_inventory['Inventory'] = sum([combined_inventory[i] for i in n])
    return combined_inventory


#Define supplier variables
x1,x3,x4 = supplier_data('NGL Supply')
x2,x5,x6 = supplier_data('Patriot')
ngl_pat_inv = inventory(n=['NGL Supply', 'Patriot'])


#Begin Plotting
pd.plotting.register_matplotlib_converters(explicit=True)
fig, ax1 = plt.subplots()
plt.plot(ngl_pat_inv.index, ngl_pat_inv['Inventory'], x3.index, x3['Net'], x4.index, x4['Net'], x5.index, x5['Net'], x6.index, x6['Net'],
         marker='.',markersize=7, linewidth=0.75)
plt.title(label='Grafton Inventory Summary')
plt.xlabel('Time')
plt.ylabel('USG')
plt.legend(['Inventory', 'NGL Rail', 'NGL Truck', 'PATRIOT Rail', 'PATRIOT Truck'], bbox_to_anchor=(1,1),
           bbox_transform=fig.transFigure, ncol=5, loc='upper right', fontsize='small')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
plt.xticks(rotation = 25)


#Used for generating marker annotations
marker_arr = [ngl_pat_inv['Inventory'], x3['Net'], x4['Net'], x5['Net'], x6['Net']]
for i, frame in enumerate(marker_arr):
    for j, txt in enumerate(frame):
        plt.annotate(f'{int(txt/1000)}k', (frame.index[j], frame.values[j]+2000)).set_fontsize(7.5)

plt.show() 

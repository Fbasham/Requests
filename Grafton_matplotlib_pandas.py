import pandas as pd
from matplotlib import pyplot as plt
import datetime

df = pd.read_csv('Grafton Inventory Report.csv', thousands=',')
##df = df.groupby([df['End Time']]).mean()

##x = df[df['Supplier'] == 'NGL Supply']['End Time']
##y = df[df['Supplier'] == 'NGL Supply']['Inventory']
##
##plt.plot(x,y)
##plt.show()


df['Inventory'] = df['Inventory'].apply(pd.to_numeric)
df['End Time'] = pd.to_datetime(df['End Time'], yearfirst=True)

#Average volume offloaded/lifted across grouped time
df2 = df.groupby([df['End Time'].dt.date]).mean()
x = df2.index
y1 = df2['Inventory']
y2 = df2['Net']
#plt.plot(x,y2)
#plt.ylabel('USG')
#plt.title('Grafton Average Net Volume Lifted/Offloaded')
#plt.show()


#NGL Supply
x1 = df[df['Supplier'] == 'NGL Supply'].groupby(df['End Time'].dt.date).mean()
x3 = df[df['Supplier'] == 'NGL Supply'][df['Type'] == 'Rail'].groupby(df['End Time'].dt.date).sum()
x4 = df[df['Supplier'] == 'NGL Supply'][df['Type'] == 'Truck'].groupby(df['End Time'].dt.date).sum().abs()
##plt.plot(x3.index, x3['Net'], x4.index, x4['Net'])
##plt.show()


#Patriot
x2 = df[df['Supplier'] == 'Patriot'].groupby(df['End Time'].dt.date).mean()
x5 = df[df['Supplier'] == 'Patriot'][df['Type'] == 'Rail'].groupby(df['End Time'].dt.date).sum()
x6 = df[df['Supplier'] == 'Patriot'][df['Type'] == 'Truck'].groupby(df['End Time'].dt.date).sum().abs()
##plt.plot(x5.index, x5['Net'], x6.index, x6['Net'])
##plt.show()


#NGL Supply Inventory at current time
ngl_inv = df['Inventory'].iloc[df[df['Supplier'] == 'NGL Supply']['End Time'].argmax()]
pat_inv = df['Inventory'].iloc[df[df['Supplier'] == 'Patriot']['End Time'].argmax()]

inv_df = pd.concat([x1['Inventory'],x2['Inventory']], axis=1, sort=True)
inv_df['Inventory'] = inv_df['Inventory'].bfill()
inv_df.columns = ['NGL', 'Patriot']
inv_df['Inventory'] = inv_df['NGL'] + inv_df['Patriot']
xtime = inv_df.index


pd.plotting.register_matplotlib_converters(explicit=True)
plt.plot(xtime, inv_df['Inventory'], x3.index, x3['Net'], x4.index, x4['Net'], x5.index, x5['Net'], x6.index, x6['Net'],marker='o')
plt.title(label='Rail/Truck Summary')
plt.legend(['Inventory', 'NGL Rail', 'NGL Truck', 'PATRIOT Rail', 'PATRIOT Truck'], loc='best')

for i, txt in enumerate(inv_df['Inventory']):
    plt.annotate(f'{txt//1000}k', (xtime[i], inv_df['Inventory'][i]+2000))

plt.show()

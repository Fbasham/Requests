import pandas as pd
import io
import numpy as np


'''the intent of this is to eventually re-factor rev-1 code that uses iteration and pd.concat
to modify a df several times.  this simpliefies that process and uses one concat
and groupby instead'''



inv = {'A': [222,432,121],
       'B': [786]}

data= {'A': list('ABC'),
       'B': [222,111,333],
       'C': [2000,1000,5000],
       'D': [100,400,500]}

df = pd.DataFrame(data)

dff = df.loc[df[df['A'].isin(inv.keys())].index.repeat([len(car) for car in inv.values()])]
dff['B'] = [car for cars in inv.values() for car in cars]

df = pd.concat([df,dff])
df = df.drop_duplicates(subset=['A', 'B'], keep='last')

df[['C','D']] = df.groupby('A')[['C','D']].transform(lambda x: x.mean()/len(x))
print(df)


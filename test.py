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



#######################################################################################################################################################
'''unstacking rows with groupby and custom aggregating of columns, useful for invoice upload since the collected raw data is in
stacked format.  The intent of unstacking it is especially useful for CAD currency codes where we don't want to include tax
in the upload, or in comparison with merge_asof results for shipments.  Rather, we want to include tax in the final summary 
for what's being paid per invoice'''

import pandas as pd


data = [

    ['111', 'tilx', 'freight', 2000],
    ['111', 'tilx', 'fsc', 100],
    ['111', 'tilx', 'tax', 50],
    ['111', 'cbtx', 'freight', 2000],
    ['111', 'cbtx', 'fsc', 100],
    ['111', 'cbtx', 'tax', 50],
    
    ['222', 'cctx', 'freight', 3000],
    ['222', 'cctx', 'fsc', 500],
    ['222', 'cctx', 'tax', 20],
    
    ['333', 'cbtx', 'freight', 2000],
    ['333', 'cbtx', 'fsc', 100]

    ]

df = pd.DataFrame(data, columns=['inv', 'car', 'desc', 'amt'])
print(df)

'''     inv   car     desc   amt
    0   111  tilx  freight  2000
    1   111  tilx      fsc   100
    2   111  tilx      tax    50
    3   111  cbtx  freight  2000
    4   111  cbtx      fsc   100
    5   111  cbtx      tax    50
    6   222  cctx  freight  3000
    7   222  cctx      fsc   500
    8   222  cctx      tax    20
    9   333  cbtx  freight  2000
    10  333  cbtx      fsc   100'''


dfs = df.set_index(['inv', 'car', 'desc']).unstack(level=2, fill_value=0)
dfs.columns = dfs.columns.droplevel(0)
dfs = dfs.reset_index()
dfs = dfs.groupby('inv').agg({'car': list,
                              'freight': lambda x: x.mean()/len(x),
                              'fsc': 'mean',
                              'tax': 'mean'
                              })

dfs = dfs.explode(column='car').reset_index()
print(dfs)

'''    inv   car  freight  fsc  tax
    0  111  cbtx     1000  100   50
    1  111  tilx     1000  100   50
    2  222  cctx     3000  500   20
    3  333  cbtx     2000  100    0'''

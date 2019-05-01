import pandas as pd
import numpy as np
from collections import defaultdict

path = r'H:\FBasham\Detention'
terms_csv = f'{path}\Detention Terms.csv'
contract_csv = f'{path}\TN Deal-Contract Status.csv'
geo_xlsx = f'{path}\geo.XLSX'

##Create df for detention terms with demurrage in the description and map mulity tier pricing to a new column
try:
    df_terms = pd.read_csv(terms_csv)
except KeyError:
    df_terms = pd.read_csv(terms_csv, header=15)

df_terms['Description.1']
df_terms = df_terms[df_terms['Description.1'].str.contains('Demurrage', na=False, regex=True)]
df_terms['key'] = df_terms['Deal Line'] + '||' + df_terms['Contract Ref']

contract_terms = defaultdict(str)
for key, terms in zip(df_terms['key'], df_terms['Description.1']):
    contract_terms[key] += terms

df_terms['key'] = df_terms['key'].map(contract_terms)


##Swap Canadian contract contacts with US counterparts 
marketers = ['Alex Smith', 'Andrew Edwards', 'Doug Begland', 'Dave McCulloch', 'Webster Mundy', 'Jason Spillman', 'Brandy Dickie', 
             'Jelena Rudan', 'David Palmer', 'Shane Wittig','Bobbi Lowry', 'Chris Skoog', 'Jay Jackson', 'Josh Duval', 
             'Mike Jones', 'Tom Krupa', 'Trevor Budgell']

try:
    df_marketers = pd.read_csv(contract_csv)
except KeyError:
    df_marketers = pd.read_csv(contract_csv, header=15)
 
    
df_marketers = df_marketers[df_marketers['Contract Contact'].isin(marketers)]

def marketer_swap(name1, name2):
    if name1 in ['David Palmer', 'Webster Mundy'] and name2 is not np.nan:
        return name2
    else:
        return name1

df_marketers['Contract Contact'] = list(map(marketer_swap, df_marketers['Contract Contact'], df_marketers['Reporting Contact']))
df_marketers = df_marketers[['Contract Ref', 'Contract Contact']]


##Join the marketers with the terms (note: join is outer incase there isn't a marketer assigned to a contract)
df = df_terms.merge(df_marketers, on='Contract Ref', how='outer')
df = df.drop_duplicates(subset=['Deal Line', 'Origin', 'Destination', 'Contract Ref'])
df = df.dropna(subset=['Item'])
df.to_csv(f'{path}\E1 Summary Detention Calcs.csv', index=False)


##Geo cleanup and filtering
df_geo = pd.read_excel(r'H:\FBasham\Detention\geo.XLSX')
df_geo = df_geo[~df_geo['Contract Code'].str.contains('REC|nan|TAMPA|STOR|Agreement|Storage|Throughput|Facility', na=False, regex=True)]
df_geo = df_geo.dropna(subset=['Contract Code'])
df_geo[['Deal', 'Contract', 'ID']] = df_geo['Contract Code'].str.split('-', expand =True)
df_geo = df_geo.drop(['Contract Code', 'Lay days', 'Quantity', 'Unit'], axis=1)
df_geo = df_geo[['Railcar', 'Trip L_E', 'Bill of Lading', 'Consignee', 'Origin',
       'Trip Destination', 'Deal', 'Contract', 'ID', 'Actual Departed', 'Destn Loc Arrival',
       'Destn Arrived', 'Constr Arrived', 'Placed Arrived', 'Actual Arrived',
       'Returning', 'Charge Start', 'Charge End']]

df_geo.to_csv(f'{path}\Cleaned Geo Data For Detention.csv', index=False)
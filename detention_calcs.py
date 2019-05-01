import pandas as pd
import numpy as np
from collections import defaultdict


##Create df for detention terms with demurrage in the description and map mulity tier pricing to a new column
df_terms = pd.read_csv(r'H:\FBasham\Detention\Detention Terms.csv')

df_terms = df_terms[df_terms['Description'].str.contains('Detention')]
df_terms['key'] = df_terms['Deal Line'] + '||' + df_terms['Contract Ref']

contract_terms = defaultdict(str)
for key, terms in zip(df_terms['key'], df_terms['Description.1']):
    contract_terms[key] += terms

df_terms['key'] = df_terms['key'].map(contract_terms)


##Swap Canadian contract contacts with US counterparts 
marketers = ['Alex Smith', 'Andrew Edwards', 'Doug Begland', 'Dave McCulloch', 'Webster Mundy', 'Jason Spillman', 'Brandy Dickie', 
             'Jelena Rudan', 'David Palmer', 'Shane Wittig','Bobbi Lowry', 'Chris Skoog', 'Jay Jackson', 'Josh Duval', 
             'Mike Jones', 'Tom Krupa', 'Trevor Budgell']


df_marketers = pd.read_csv(r'H:\FBasham\Detention\TN Deal-Contract Status.csv')
df_marketers = df_marketers[df_marketers['Contract Contact'].isin(marketers)]


def marketer_swap(name1, name2):
    if name1 in ['David Palmer', 'Webster Mundy'] and name2 is not np.nan:
        return name2
    else:
        return name1

df_marketers['Contract Contact'] = list(map(marketer_swap, df_marketers['Contract Contact'], df_marketers['Reporting Contact']))
df_marketers = df_marketers[['Contract Ref', 'Contract Contact']]


##Join the marketers with the terms
df = df_terms.merge(df_marketers, on='Contract Ref')
df = df.drop_duplicates(subset=['Deal Line', 'Origin', 'Destination', 'Contract Ref'])
df.to_csv('H:\FBasham\Detention\E1 Summary Detention Calcs.csv', index=False)

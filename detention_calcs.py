import pandas as pd
import numpy as np
from itertools import groupby


##Create df for detention terms with demurrage in the description and map mulity tier pricing to a new column
df_terms = pd.read_csv(r'H:\FBasham\Detention\Detention Terms.csv')

df_terms = df_terms[df_terms['Description'].str.contains('Detention')]
df_terms['concat'] = df_terms['Deal Line'] + '||' + df_terms['Contract Ref']

mapper = {}
for item, group in groupby(zip(df_terms['Deal Line']+'||'+df_terms['Contract Ref'], df_terms['Description.1']), key=lambda x: x[0]):
    terms = []
    for thing in list(set(group)):
        terms.append(thing[1])
    mapper.update({thing[0]: ''.join(terms)})

df_terms['concat'] = df_terms['concat'].map(mapper)


##Swap Canadian contract contacts with US counterparts 
marketers = ['Alex Smith', 'Andrew Edwards', 'Doug Begland', 'Dave McCulloch', 'Webster Mundy',
             'Jason Spillman', 'Brandy Dickie', 'Jelena Rudan', 'David Palmer', 'Shane Wittig',
             'Bobbi Lowry', 'Chris Skoog', 'Jay Jackson', 'Josh Duval', 'Mike Jones', 'Tom Krupa',
             'Trevor Budgell']

df_marketers = pd.read_csv(r'H:\FBasham\Detention\TN Deal-Contract Status.csv', header=15)
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
df.to_csv('H:\FBasham\Detention\E1 Summary.csv', index=False)

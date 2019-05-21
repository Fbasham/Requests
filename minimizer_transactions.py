# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:25:12 2019

@author: Fbasham
"""

from ortools.graph import pywrapgraph
import pandas as pd
from datetime import datetime
import random


##Read in current pricing report and create a new column for net price
df = pd.read_csv(r'H:\FBasham\prices.csv')
df = df.drop_duplicates(subset=['Counterparty', 'Deal Line', 'Contract Ref'])
df['Net Price'] = df['Ref Price'] + df['Fixed Price']


def price_adjust(price):
    dollar, cents = str(price).split('.')
    if '-' in dollar:
        return float(f'-0.{cents}')
    return float(f'0.{cents}')

def location_cleaner(loc):
    if 'AB' in loc:
        return 'East Edmonton, AB'
    elif loc in ['Hanna, OH', 'Houston, PA']:
        return 'HOUSTON/HOPEDALE (RULE 11), OH'
    elif loc == 'West Lebanon, NH':
        return 'WEST LEBANON (GRAFTON), NH'
    return loc.replace('*', '')


df['Supply'] = df['Supply'].apply(location_cleaner).str.upper()
df['Demand'] = df['Demand'].apply(location_cleaner).str.upper()
df['Net Price'] = df['Net Price'].apply(price_adjust)
df = df[df['Net Price'] != 0]
df = df[df['Item'].isin(['C3', 'C3o'])]


##Separate dataframes for purchases and sales, used later for merging
dfp = df[df['Category'] == 'Purchase'][['Counterparty', 'Deal Line', 'Contract Ref', 'Supply', 'Net Price']]
dfs = df[df['Category'] == 'Sale'][['Counterparty', 'Deal Line', 'Contract Ref', 'Demand', 'Net Price']]


##df for freight rates 
dfr = pd.read_excel(r'H:\FBasham\2019-2020 - Freight Minimizer - Copy.xlsx', sheet_name='C3 Rates')
dfr = dfr[dfr['Rate'] != 0]
dfr['Supply'] = dfr['Supply'].str.replace('HOUSTON/HOPEDALE (RULE 11), PA', 'HOUSTON/HOPEDALE (RULE 11), OH', regex=False)


##Merge purchase, sales, freight rates into one dataframe with left join
dff = dfp.merge(dfr, on='Supply')
dff = dff.merge(dfs, on='Demand', suffixes=['_Purchase','_Sale'], how='left')


dff = dff[['Counterparty_Purchase', 'Counterparty_Sale', 'Supply', 'Demand', 'Route', 'Net Price_Purchase', 'Net Price_Sale', 'Rate']]
dff.columns = ['Seller', 'Buyer', 'Supply', 'Demand', 'Route', 'Purchase', 'Sale', 'Freight']
dff['Buyer'] = dff['Buyer'].fillna('NGL Supply Co Ltd')
dff['Sale'] = dff['Sale'].fillna(0)*30000
dff['Purchase'] = dff['Purchase']*30000


inventory_cities = ['BEAUHARNOIS, QC', 'STEPHENS CITY, VA', 'MENTONE, IN', 'TIRZAH, SC', 'TAMPA, FL', 'MILFORD, VA',
                    'TERRYVILLE, CT', 'MARYSVILLE, MI', 'SARNIA, ON', 'PUTNAM, ON', 'NORTH GRAFTON, MA', 'BRIGHAM, QC']

##This is intended to create data for inventory demands since they aren't part of the pricing report
df_ngl = dff.copy()
df_ngl = df_ngl[(df_ngl['Demand'].isin(inventory_cities)) & (df_ngl['Sale'] != 0) & (df_ngl['Buyer'] != 'NGL Supply Co Ltd')]
df_ngl['Sale'] = 0
df_ngl['Buyer'] = 'NGL Supply Co Ltd'

##Combine all the data one last time (concat appends on axis=0 by default which what we want)
dff = pd.concat([dff, df_ngl])
dff['Total Cost'] = dff['Purchase'] + dff['Sale'] - dff['Freight']

dff.to_csv('123456.csv', index=False)



def freight_min(col_name):


    df = pd.read_csv('123456.csv')
    
    df['Supply'] = df['Seller'] + ' | ' + df['Supply']
    df['Demand'] = df['Buyer'] + ' | ' + df['Demand']
    
    
    if col_name == 'Total Cost':
        #minimize expenses (i.e. maximize revenue) by inverting the sign on total cost and setting inventory cities to a net positive arbitrary sales price       
       
        #Terminal Loss:
        #df.loc[(df['Sale'] == 0) & (df['Buyer'].str.contains('NGL Supply Co Ltd')), 'Total Cost'] /= random.randint(25,50)
        
        #Terminal Gain:
        df.loc[(df['Sale'] == 0) & (df['Buyer'].str.contains('NGL Supply Co Ltd')), 'Total Cost'] /= -random.randint(25,50)
        
        df['Total Cost'] *= -1

      
          
    supply_list = df["Supply"].tolist()
    supply_increment_dict = {city:i for i,city in enumerate(df["Supply"].unique())}
    supply_nodes = [supply_increment_dict[v] for v in supply_list]
    demand_list = df["Demand"].tolist()
    demand_increment_dict = {city:i for i,city in enumerate(df['Demand'].unique(), start=len(set(supply_list)))}
    demand_nodes = [demand_increment_dict[v] for v in demand_list]  
    capacities = [500] * len(supply_nodes)
    unit_costs = df[col_name].astype(int).tolist()


    supply_data = {#   Node       Supply
                    'Markwest | BLUESTONE, PA': 60,
                    'XTO Energy | BLUESTONE, PA': 80,
                    'Marathon Petroleum Company LLC | CATLETTSBURG, KY': 0,
                    'Keyera | EAST EDMONTON, AB': 0,
                    'Pembina Infrastructure and Logistics LP | EAST EDMONTON, AB': 83,
                    'Pembina Midstream (U.S.A.) Inc. | EAST EDMONTON, AB': 0,
                    'Shell Chemicals Canada | EAST EDMONTON, AB': 0,
                    'Tidewater Midstream & Infrastructure Ltd | EAST EDMONTON, AB': 0,
                    'BP Energy Company | EAST MORRIS, IL': 55,
                    'Dominion Gathering and Processing Inc. | GALMISH, WV': 35,
                    'EQT | HOUSTON/HOPEDALE (RULE 11), OH': 20,
                    'Markwest | HOUSTON/HOPEDALE (RULE 11), OH': 0,
                    'NGL Supply Wholesale, LLC | HOUSTON/HOPEDALE (RULE 11), OH': 25,
                    'EQT | MOUNDSVILLE, WV': 77,
                    'Jay Bee Production Company | NATRIUM, WV': 29,
                    'Pembina Infrastructure and Logistics LP | SARNIA, ON': 0,
                    'Shell Chemicals Canada | SARNIA, ON': 0,
                    'NGL Supply Wholesale, LLC | SCIO, OH': 20,
                    'Valero Energy Inc. | ST ROMUALD, QC': 55
                   }
      
    demand_data = {
                    'Suburban Propane | ALBANY, NY': 0,
                    'NGL Supply Co Ltd | ALTO, MI': 0,
                    'NGL Supply Co Ltd | ARCADIA, LA': 0,
                    'Suburban Propane | ASHEVILLE, NC': 1,
                    'Suburban Propane | ATHENS, TN': 0,
                    'Amerigas | ATLANTA, GA': 13,
                    'Highlands Fuel Delivery LLC | AUBURN, ME': 13,
                    'Suburban Propane | BALTIMORE, MD': 0,
                    'NGL Supply Co Ltd | BAYONNE, NJ': 0,
                    'NGL Supply Co Ltd | BAYWAY, NJ': 0,
                    'Hamel Propane | BEAUHARNOIS, QC': 2,
                    'NGL Supply Co Ltd | BEAUHARNOIS, QC': 36,
                    'NGL Supply Co Ltd | BIRMINGHAM, AL': 0,
                    'NGL Supply Co Ltd | BRANCHVILLE, VA': 0,
                    'NGL Supply Co Ltd | BRIGHAM, QC': 41,
                    'NGL Supply Co Ltd | BUCHANAN, GA': 0,
                    'Suburban Propane | BURNHAM, PA': 0,
                    'Universal | CALEXICO, CA': 0,
                    'Spar Gas Inc. | CARTHAGE, TN': 0,
                    'NGL Supply Co Ltd | CEDARS, QC': 0,
                    'NGL Supply Co Ltd | CHICAGO, IL': 0,
                    'Suburban Propane | CLEARWATER, FL': 2,
                    'NGL Supply Co Ltd | DARTMOUTH, NS': 0,
                    'Amerigas | DECHERD, TN': 5,
                    'NGL Supply Co Ltd | DRAGON, MS': 0,
                    'NGL Supply Co Ltd | EDMUNDSTON, NB': 0,
                    'Schagrin Gas | ELSMERE JCT, DE': 6,
                    'Suburban Propane | GAINESVILLE, VA': 0,
                    'NGL Supply Co Ltd | GENEVA, NY': 0,
                    'Schagrin Gas | GEORGETOWN, DE': 0,
                    'Bowman Gas | GULLIVER, MI': 0,
                    'Nasco | HALLNOR, ON': 0,
                    'Dead River Company | HAMPDEN, ME': 3,
                    'NGL Supply Co Ltd | HOWELLS TRANSFER, GA': 0,
                    'NGL Supply Co Ltd | JACKSONVILLE, FL': 0,
                    'NGL Supply Co Ltd | KAWKAWLIN, MI': 0,
                    'NGL Supply Co Ltd | KESWICK, VA': 0,
                    'Freepoint Commodities | LAREDO, TX': 0,
                    'NGL Supply Co Ltd | LIMA, OH': 0,
                    'Amerigas | LYNNDYL, UT': 0,
                    'Buckeye Energy Services LLC | MACUNGIE, PA': 6,
                    'NGL Supply Co Ltd | MARCUS HOOK, PA': 0,
                    'NGL Supply Co Ltd | MARYSVILLE, MI': 50,
                    'NGL Supply Co Ltd | MCFARLAND, WI': 0,
                    'NGL Supply Co Ltd | MENTONE, IN': 7,
                    'NGL Supply Co Ltd | MERLIN, OR': 0,
                    'Suburban Propane | MIAMI, FL': 0,
                    'NGL Supply Co Ltd | MILFORD, VA': 49,
                    'North Star Gas LTD Co. | MOBILE, AL': 0,
                    'NGL Supply Co Ltd | MONCTON, NB': 0,
                    'NGL Supply Co Ltd | MT VERNON, IN': 0,
                    'Bournes Propane | NEWPORT, VT': 3,
                    'NGL Supply Co Ltd | NOGALES, AZ': 0,
                    'NGL Supply Co Ltd | NORTH GRAFTON, MA': 16,
                    'Maine Energy Inc. | NORTH MAINE JUNCTION, ME': 1,
                    'Ray Energy Corp. | NORTH MAINE JUNCTION, ME': 8,
                    'NGL Supply Co Ltd | PAULSBORO, NJ': 0,
                    'NGL Supply Co Ltd | PHILADELPHIA, PA': 0,
                    'NGL Supply Co Ltd | PLAINVILLE, CT': 0,
                    'NGL Supply Co Ltd | PORT READING, NJ': 0,
                    'NGL Supply Co Ltd | PRESQUE ISLE, ME': 0,
                    'NGL Supply Co Ltd | PROCTOR, MN': 0,
                    'NGL Supply Co Ltd | PUTNAM, ON': 17,
                    'NGL Supply Co Ltd | REDDING, CA':0,
                    'Paraco Gas Corporation | RIVERHEAD, NY': 5,
                    'Eastern Propane | ROCHESTER, NH': 1,
                    'Suburban Propane | ROCKVILLE, MD': 0,
                    'NGL Supply Co Ltd | RUTLAND, VT': 0,
                    'NGL Supply Co Ltd | SAINT JOHN, NB': 0,
                    'North Star Gas LTD Co. | SAN DIEGO, CA': 0,
                    'NGL Supply Co Ltd | SARNIA, ON': 40,
                    'NGL Supply Co Ltd | SAVANNAH, GA': 0,
                    'NGL Supply Co Ltd | SELMA, NC': 0,
                    'NGL Supply Co Ltd | SEWAREN, NJ': 0,
                    'Spar Gas Inc. | SPARTA, TN': 0,
                    'Shipley Energy | STEELTON, PA': 5,
                    'NGL Supply Co Ltd | STEPHENS CITY, VA': 18,
                    'Suburban Propane | STEPHENS CITY, VA': 1,
                    'NGL Supply Co Ltd | SUMAS, WA': 0,
                    'NGL Supply Co Ltd | TALLAVAST (SARASOTA), FL': 0,
                    'NGL Supply Co Ltd | TAMPA, FL': 8,
                    'Suburban Propane | TAMPA, FL': 0,
                    'NGL Supply Co Ltd | TERRYVILLE, CT': 24,
                    'NGL Supply Co Ltd | TIRZAH, SC': 49,
                    'NGL Supply Co Ltd | TOMAHAWK, WI': 0,
                    'NGL Supply Co Ltd | WARREN, PA': 0,
                    'Rymes Propane & Oil Inc. | WEST LEBANON (GRAFTON), NH': 20,
                    'NGL Supply Co Ltd | WEST POINT, VA': 27,
                    'Keystone Propane Service, Inc. | WEST TOBYHANNA, PA': 3,
                    'NGL Supply Co Ltd | WESTBORO, MA': 0,
                    'NGL Supply Co Ltd | WHITE RIVER JCT, VT': 0,
                    'Suburban Propane | WOODENSBURG, MD': 0,
                    'NGL Supply Co Ltd | YAKIMA, WA': 0
                 }
    
    sc = [supply_data.get(city, 0) for city in supply_increment_dict]
    dc = [-demand_data.get(city,0) for city in demand_increment_dict]
    supplies = sc + dc


    # Instantiate a SimpleMinCostFlow solver.
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()

    # Add each arc.
    for i in range(0, len(supply_nodes)):
        min_cost_flow.AddArcWithCapacityAndUnitCost(supply_nodes[i], demand_nodes[i],
                                                capacities[i], unit_costs[i])

    # Add node supplies.
    for i in range(0, len(supplies)):
        min_cost_flow.SetNodeSupply(i, supplies[i])

    # Find the minimum cost flow   
    if min_cost_flow.SolveMaxFlowWithMinCost() == min_cost_flow.OPTIMAL:

        rows = []
        for i in range(min_cost_flow.NumArcs()):
            cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)  
                 
            if cost != 0:
                               
                row = [
                       list(supply_increment_dict.keys())[list(supply_increment_dict.values()).index(min_cost_flow.Tail(i))],                        
                       list(demand_increment_dict.keys())[list(demand_increment_dict.values()).index(min_cost_flow.Head(i))],                        
                       min_cost_flow.UnitCost(i),                                                                                                    
                       min_cost_flow.Flow(i),                                                                                                                                                                                                         
                       cost
                       ]                                                                                                                        
                
                rows.append(row)

        
        df = pd.DataFrame(rows, columns = ["Supply","Demand","Rate","Cars","Cost"])
        df = df.groupby(['Supply', 'Demand']).sum()                              
        df.to_csv(f'{datetime.today().date()}_{col_name}_freight_min_cost.csv')                                  
        print(df)
        print(f'total cars = {df["Cars"].sum()}')
        print(f'total cost = {df["Cost"].sum()}')
        print(f'minimizing: {col_name}')

    else:
        print('There was an issue with the min cost flow input.')

#Function call:
for i in ['Freight', 'Total Cost']:        
    freight_min(i)
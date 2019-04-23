# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:24:37 2019
@author: Fbasham
"""

from ortools.graph import pywrapgraph
import pandas as pd


def freight_min(commodity):

    '''Define four parallel arrays: start_nodes, end_nodes, capacities, and unit costs
    between each pair. For instance, the arc from node 0 to node 1 has a
    capacity of 15 and a unit cost of 4'''


    df = pd.read_excel(r"H:\FBasham\2019-2020 - Freight Minimizer.xlsx", sheet_name=commodity)[:-1]

    supply_list = list(df["Supply"])
    supply_increment_dict = {city:i for i,city in enumerate(df["Supply"].unique())}
    supply_nodes = [supply_increment_dict[v] for v in supply_list]
    demand_list = list(df["Demand"])
    demand_increment_dict = {city:i for i,city in enumerate(df['Demand'].unique(), start=len(set(supply_list)))}
    demand_nodes = [demand_increment_dict[v] for v in demand_list]  
    capacities = [300] * len(supply_nodes)
    unit_costs = list(df["USD Rate"].astype(int))
    routes = list(df["Route"])
    route_keys = [f'{supply_list[i]} {demand_list[i]}, {unit_costs[i]}' for i, _ in enumerate(unit_costs)]
    route_cost_dict = dict(zip(route_keys,routes))
    tariff = list(df["Tariff"].astype(str))
    tariff_dict = dict(zip(route_keys, tariff))
    
    supply_data = {#   Node       Supply
                 "EAST MORRIS, IL": 35,
                 "HOUSTON/HOPEDALE (RULE 11), PA": 31,
                 "HYDROCARBON, KY": 50,
                 "GALMISH, WV": 35,
                 "MOUNDSVILLE, WV": 77,
                 "NATRIUM, WV": 21,
                 "LEMONT, IL": 0,
                 "BLUESTONE, PA": 90,
                 "SARNIA, ON": 0,
                 "BUFFALO, NY": 0,
                 "BIRMINGHAM, AL": 0,
                 "ST JOHN, NB": 0,
                 "NANTICOKE, ON": 0,
                 "PARADIS, LA": 0,
                 "SCIO, OH": 0,
                 "ST ROMUALD, QC": 55,
                 "CATLETTSBURG, KY": 0,
                 "MARYSVILLE, MI": 0,
                 "EAST EDMONTON, AB": 116,
                 }
  
    demand_data = {
                 "STEPHENS CITY, VA": 16,
                 "BRANCHVILLE, VA": 1,
                 "ATLANTA, GA": 13,
                 "BEAUHARNOIS, QC": 41,
                 "DECHERD, TN": 5,
                 "MACUNGIE, PA": 6,
                 "NEWPORT, VT": 3,
                 "BRIGHAM, QC": 48,
                 "N MAINE JCT, ME": 11,
                 "WEST POINT, VA": 19,
                 "HAMPDEN, ME": 5,
                 "MILLINOCKET, ME": 0,
                 "PRESQUE ISLE, ME": 0,
                 "LORENZO, IL": 50,
                 "ROCHESTER, NH": 1,
                 "NORTH GRAFTON, MA": 16,
                 "DRAGON, MS": 0,
                 "AUBURN, ME": 7,
                 "DARTMOUTH, NS": 0,
                 "EDMUNDSTON, NB": 0,
                 "MONCTON, NB": 0,
                 "RUTLAND, VT": 0,
                 "WHITE RIVER JCT, VT": 0,
                 "WEST TOBYHANNA, PA": 1,
                 "MENTONE, IN": 14,
                 "MILFORD, VA": 49,
                 "HALLNOR, ON": 6,
                 "RIVERHEAD, NY": 5,
                 "MOBILE, AL": 0,
                 "SARNIA, ON": 30,
                 "PUTNAM, ON": 26,
                 "WEST LEBANON (GRAFTON), NH": 0,
                 "ELSMERE JCT, DE": 6,
                 "GEORGETOWN, DE": 0,
                 "STEELTON, PA": 5,
                 "SPARTA, TN": 0,
                 "CARTHAGE, TN": 0,
                 "MCMINNVILLE, TN": 0,
                 "ATHENS, TN": 0,
                 "ASHEVILLE, NC": 4,
                 "CLEARWATER, FL": 0,
                 "GAINESVILLE, VA": 0,
                 "MIAMI, FL": 0,
                 "ROCKVILLE, MD": 0,
                 "BURNHAM, PA": 0,
                 "WOODENSBURG, MD": 0,
                 "MARYSVILLE, MI": 55,
                 "TAMPA, FL": 8,
                 "TERRYVILLE, CT": 19,
                 "MINGO JCT, OH": 0,
                 "LANCASTER, SC": 40
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
                       route_cost_dict[(list(supply_increment_dict.keys())[list(supply_increment_dict.values()).index(min_cost_flow.Tail(i))] 
                       + " " + list(demand_increment_dict.keys())[list(demand_increment_dict.values()).index(min_cost_flow.Head(i))]
                       + ", " + str(min_cost_flow.UnitCost(i)))],                                                                                                  
                       min_cost_flow.UnitCost(i),                                                                                                    
                       min_cost_flow.Flow(i),                                                                                                                                                                                                         #6 Capacity
                       cost,
                       tariff_dict[(list(supply_increment_dict.keys())[list(supply_increment_dict.values()).index(min_cost_flow.Tail(i))] 
                       + " " + list(demand_increment_dict.keys())[list(demand_increment_dict.values()).index(min_cost_flow.Head(i))]
                       + ", " + str(min_cost_flow.UnitCost(i)))]
                        ]                                                                                                                        
                
                rows.append(row)

        
        df = pd.DataFrame(rows, columns = ["Supply","Demand","Route","Rate","Cars","Cost","Tariff"])
        df = df.groupby(['Supply', 'Demand']).sum()                                  
        df.to_csv(f'{commodity}_freight_min_cost.csv')                                  
        print(df)
        
    else:
        print('There was an issue with the min cost flow input.')

freight_min('Propane')
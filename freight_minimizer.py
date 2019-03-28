# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:24:37 2019

@author: Fbasham

"""

from __future__ import print_function
from ortools.graph import pywrapgraph
import pandas as pd


def main():
    """MinCostFlow simple interface example."""

    # Define four parallel arrays: start_nodes, end_nodes, capacities, and unit costs
    # between each pair. For instance, the arc from node 0 to node 1 has a
    # capacity of 15 and a unit cost of 4.
    df = pd.read_excel(r"H:\FBasham\Freight Minimizer test.xlsx")
    
    supply_list = list(df["Supply"])[:-1]
    supply_increment = [int(i) for i in range(len(set(supply_list)))]
    supply_increment_dict = dict(zip(set(supply_list), supply_increment))
    supply_nodes = [supply_increment_dict[v] for v in supply_list if v in supply_list]
    demand_list = list(df["Demand"])[:-1]
    demand_increment = [int(i+len(set(supply_nodes))) for i in range(len(set(demand_list)))]
    demand_increment_dict = dict(zip(set(demand_list), demand_increment))
    demand_nodes = [demand_increment_dict[v] for v in demand_list if v in demand_list]  
    capacities = [300 for i in range(len(supply_nodes))]
    u = list(df["USD Rate"])[:-1]
    unit_costs = [int(i) for i in u]
    routes = list(df["Route"])[:-1]
    route_keys = [(supply_list[i] + " " + demand_list[i] + ", " + str(unit_costs[i])) for i in range(len(unit_costs))] 
    route_cost_dict = dict(zip(route_keys,routes))
    tariff = [str(elem) for elem in list(df["Tariff"])][:-1]
    tariff_dict = dict(zip(route_keys, tariff))
    
    supply_data = {#     Node       Supply
                 "EAST MORRIS, IL": 0,
                 "HOUSTON/HOPEDALE (RULE 11), PA": 29,
                 "HYDROCARBON, KY": 0,
                 "GALMISH, WV": 0,
                 "MOUNDSVILLE, WV": 77,
                 "NATRIUM, WV": 22,
                 "LEMONT, IL": 0,
                 "BLUESTONE, PA": 160,
                 "SARNIA, ON": 0,
                 "BUFFALO, NY": 0,
                 "BIRMINGHAM, AL": 0,
                 "ST JOHN, NB": 0,
                 "NANTICOKE, ON": 0,
                 "PARADIS, LA": 0,
                 "SCIO, OH": 0,
                 "ST ROMUALD, QC": 20,
                 "CATLETTSBURG, KY": 0,
                 "MARYSVILLE, MI": 0,
                 "EAST EDMONTON, AB": 159,
                 }
    
    demand_data = {
                 "STEPHENS CITY, VA": 18,
                 "BRANCHVILLE, VA": 0,
                 "ATLANTA, GA": 13,
                 "BEAUHARNOIS, QC": 50,
                 "MACUNGIE, PA": 9,
                 "NEWPORT, VT": 4,
                 "BRIGHAM, QC": 56,
                 "N MAINE JCT, ME": 8,
                 "WEST POINT, VA": 5,
                 "HAMPDEN, ME": 6,
                 "MILLINOCKET, ME": 0,
                 "PRESQUE ISLE, ME": 0,
                 "ROCHESTER, NH": 3,
                "NORTH GRAFTON, MA": 11,
                "DRAGON, MS": 0,
                "DARTMOUTH, NS": 0,
                "EDMUNDSTON, NB": 0,
                "MONCTON, NB": 0,
                "RUTLAND, VT": 0,
                "WHITE RIVER JCT, VT": 0,
                "AUBURN, ME": 8,
                "WEST TOBYHANNA, PA": 3,
                "MENTONE, IN": 18,
                "MILFORD, VA": 51,
                "HALLNOR, ON": 10,
                "RIVERHEAD, NY": 5,
                "MOBILE, AL": 0,
                "SARNIA, ON": 30,
                "PUTNAM, ON": 60,
                "WEST LEBANON (GRAFTON), NH": 0,
                "ELSMERE JCT, DE": 0,
                "GEORGETOWN, DE": 6,
                "STEELTON, PA": 7,
                "SPARTA, TN": 0,
                "CARTHAGE, TN": 0,
                "MCMINNVILLE, TN": 0,
                "ATHENS, TN": 0,
                "ASHEVILLE, NC": 2,
                "CLEARWATER, FL": 2,
                "GAINESVILLE, VA": 0,
                "MIAMI, FL": 7,
                "ROCKVILLE, MD": 0,
                "BURNHAM, PA": 0,
                "WOODENSBURG, MD": 0,
                "MARYSVILLE, MI": 30,
                "TAMPA, FL": 20,
                "TERRYVILLE, CT": 20,
                "MINGO JCT, OH": 0
                }
    
    sc = [supply_data[k] if k in supply_data else 0 for k in supply_increment_dict]
    dc = [-demand_data[k] if k in demand_data else 0 for k in demand_increment_dict]
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

    # Find the minimum cost flow between node 0 and node 4.
  
    
    if min_cost_flow.SolveMaxFlowWithMinCost() == min_cost_flow.OPTIMAL:
        print('Minimum cost:', min_cost_flow.OptimalCost())
        print('')
        print("{:^40s}     {:^30s}   {:^40s}   {:^20s}   {:^20s}   {:^20s}   {:^20s}".format("Supply","Demand","Route","Unit Cost","# of Cars","Cost","Tariff"))
        print('')      
        
        
        row_storer = []
        for i in range(min_cost_flow.NumArcs()):
            cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)  
      
            
            if  cost != 0:
                
                
                row = [
                       list(supply_increment_dict.keys())[list(supply_increment_dict.values()).index(min_cost_flow.Tail(i))],                        #1 Supply
                       list(demand_increment_dict.keys())[list(demand_increment_dict.values()).index(min_cost_flow.Head(i))],                        #2 Demand
                       route_cost_dict[(list(supply_increment_dict.keys())[list(supply_increment_dict.values()).index(min_cost_flow.Tail(i))] 
                       + " " + list(demand_increment_dict.keys())[list(demand_increment_dict.values()).index(min_cost_flow.Head(i))]
                       + ", " + str(min_cost_flow.UnitCost(i)))],                                                                                    #3 Route              
                       min_cost_flow.UnitCost(i),                                                                                                    #4 Unit Cost
                       min_cost_flow.Flow(i),                                                                                                        #5 Flow
                       #min_cost_flow.Capacity(i),                                                                                                   #6 Capacity
                       cost,
                       tariff_dict[(list(supply_increment_dict.keys())[list(supply_increment_dict.values()).index(min_cost_flow.Tail(i))] 
                       + " " + list(demand_increment_dict.keys())[list(demand_increment_dict.values()).index(min_cost_flow.Head(i))]
                       + ", " + str(min_cost_flow.UnitCost(i)))]]                                                                                                                        #7 Cost
                
                row_storer.append(row)
      
                print("{:^40} --> {:^30} | {:^40} | ${:^20,} | {:^20} | ${:^20,} | {:^20s}".format(*row))       
        
        data = pd.DataFrame(row_storer, columns = ["Supply","Demand","Route","Unit Cost","# of Cars","Cost","Tariff"])
        data.to_excel('freight_min_cost.xlsx', index = False)                                  
      
    else:
        print('There was an issue with the min cost flow input.')

if __name__ == '__main__':
  main()
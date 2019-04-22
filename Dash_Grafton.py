# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 07:43:42 2019

@author: Fbasham
"""

import pandas as pd
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


df = pd.read_csv(r'H:\FBasham\Python (do not delete code please)\Grafton Inventory Report.csv', thousands=',')

all_suppliers = df['Supplier'].unique()
default = ['NGL Supply', 'Patriot']

                       
#Convert to useful units of measure and define dataframe of DateIndexes for current month, used for extending data to current day
df['Inventory'] = df['Inventory'].apply(pd.to_numeric)
df['End Time'] = pd.to_datetime(df['End Time'], yearfirst=True)
today = datetime.date.today()
period = pd.Period(today, freq='M')
dates = pd.date_range(start=period.start_time, end=today, freq='D')


def supplier_data(supplier):

    ''' returns x-axis cooridnates and grouped volumes by truck and rail respecitively'''
    day_inventory = df[df['Supplier'] == supplier][['Inventory']].groupby(df['End Time'].dt.date).last()
    sum_rail = df[(df['Supplier'] == supplier) & (df['Type'] == 'Rail')][['Net']].groupby(df['End Time'].dt.date).sum()
    sum_truck = df[(df['Supplier'] == supplier) & (df['Type'] == 'Truck')][['Net']].groupby(df['End Time'].dt.date).sum().abs()
  
    #Extend the above dataframes to current date and nornmalize to 0 if no liftings/offloads in report:
    day_inventory = day_inventory.reindex(dates).bfill().ffill()
    sum_rail = sum_rail.reindex(dates).fillna(0)
    sum_truck = sum_truck.reindex(dates).fillna(0)  
    return [day_inventory, sum_rail, sum_truck]


def inventory(arr):
    ''' Generate dataframe of supplier inventory, n defaults to all suppliers at the terminal if no kwargs passed.
        The 'dates' dataframe is created in order to increment current month's date if no inventory is reported from
        in the downloaded reports. Placeholder column needs to exist, but doesn't impact inventory calc '''
    inventories = [supplier_data(i)[0] for i in arr]
    combined_inventory = pd.concat(inventories, axis=1, sort=True)
    combined_inventory.columns = arr 
    combined_inventory['Inventory'] = combined_inventory.sum(axis=1)
    return combined_inventory


def rail_offloads(arr):
    offloads = [supplier_data(i)[1] for i in arr]
    combined_offloads = pd.concat(offloads, axis=1, sort=True)  
    combined_offloads.columns = arr    
    return combined_offloads


def truck_liftings(arr):
    liftings = [supplier_data(i)[2] for i in arr]
    combined_liftings = pd.concat(liftings, axis=1, sort=True)
    combined_liftings.columns = arr 
    return combined_liftings


##Dash setup:

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Grafton Inventory'),


    dcc.Graph(
        id='inventory-graph',
        figure={
            'data': [
                {'x': inventory(default).index, 'y': inventory(default)['Inventory'], 'type': 'bar', 'marker': {'color': 'crimson'}, 'name': f"{' & '.join(default)} Inventory"}
            ],
            'layout': {
                'title': f"{' & '.join(default)} Inventory"
            }
        }
    ),
    
        dcc.Graph(
        id='inventory-graph2',
        figure={
            'data': [
                {'x': inventory(all_suppliers).index, 'y': inventory(all_suppliers)['Inventory'], 'type': 'bar', 'name': 'Combined Inventory'}
            ],
            'layout': {
                'title': 'Combined Inventory'
            }
        }
    ),
             
        html.Div([
                dcc.Dropdown(
                    id='supplier_name_rail',
                    options=[{'label': i, 'value': i} for i in all_suppliers],
                    value= all_suppliers,
                    multi=True
                )]),
       
        dcc.Graph(
        id='rail_offloads-graph'),


        html.Div([
                dcc.Dropdown(
                    id='supplier_name_truck',
                    options=[{'label': i, 'value': i} for i in all_suppliers],
                    value= all_suppliers,
                    multi=True
                )]),
        
        dcc.Graph(
        id='truck_liftings-graph')
    
])
        
        
        
@app.callback(
        Output('rail_offloads-graph', 'figure'),
        [Input('supplier_name_rail', 'value')])
def update_rail(suppliers):
    
    return {'data': [{'x': rail_offloads(suppliers).index, 'y': rail_offloads(suppliers)[i], 'type': 'line','name': i} for i in suppliers],
            'layout': {'title': 'Rail Offloads', 'colorway': ['salmon', 'limegreen', 'dodgerblue', 'violet']}}


@app.callback(
         Output('truck_liftings-graph', 'figure'),
        [Input('supplier_name_truck', 'value')])
def update_truck(suppliers):
    
    return {'data': [{'x': truck_liftings(suppliers).index, 'y': truck_liftings(suppliers)[i], 'type': 'line', 'name': i} for i in suppliers],
            'layout': {'title': 'Truck Liftings'}}
                                 
                    
           
if __name__ == '__main__':
    app.run_server(debug=False)

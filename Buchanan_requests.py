# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:31:51 2019

@author: Fbasham
"""

import requests
import csv 


with requests.Session() as s:
    
    login = {'Id': 'E12V2', 'pwd': 'Legend11'}
    auth = s.post('https://accessns.nscorp.com/accessNS/rest/auth/login', json=login)
        
    headers = {'CSRFTOKEN': auth.json()['response']['token']}    
    payload = {'userId': 'E12V2', 'classCode"': 'B15', 'stationCode': 'CC332'}  
    
    inventory = s.post('https://accessns.nscorp.com/accessNS/rest/backend-v2/ServicesIndustrial/services/industrial2/v2/onsite/details', 
                 json=payload, headers=headers)  
    
    receiving = s.post('https://accessns.nscorp.com/accessNS/rest/backend-v2/ServicesIndustrial/services/industrial2/v2/receiving/details',
                       json=payload, headers=headers)

        
    with open('Buchanan_Daily_Report.csv', 'w', newline='') as csvfile:
        
        headers = ['Railcar', 'Status', 'Location', 'Origin', 'Destination', 'ETA', 'Class', 'Type', 'Commodity']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        
        for _id, record in enumerate([inventory.json(), receiving.json()]):
            
            details = record['result']['inventory']['inventoryDetail']       
            for item in details:
                #Car details:
                code, num = item['equipmentDisplay'].split()
                car = ''.join([code, num.lstrip('0')])
                commodity = item['inventoryRecord']['commodity']
                status = item['inventoryRecord']['webLoadEmptyIndicator']
                _class = item['inventoryRecord']['classCode']
                car_type = item['inventoryRecord']['carType']
                          
                #Loaction details:
                loc = item['inventoryRecord']['location']
                origin = item['originStation']
                destination = item['destinationStation'] if item['destinationStation'] is not None else 'BUCHANAN, GA'
                eta = item['etaTimestampDisplay']
                
                indicator = 'onsite' if _id is 0 else 'receiving'
            
                row = [indicator, car, status, loc, origin, destination, eta, _class, car_type, commodity]
                writer.writerow(dict(zip(headers, row)))
    
              
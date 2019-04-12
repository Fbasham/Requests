# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:11:43 2019

@author: Fbasham
"""

import requests
import csv


def meal_finder(*ingredients):
    
    rows = []
    for page in range(1,100):
        
        foods = ','.join(ingredients)
        url = f'http://www.recipepuppy.com/api/?i={foods}'

        try:      
            r = requests.get(url, params={'p': page})
            for recipe in r.json()['results']:
                title = recipe['title'].strip()
                ingr = ', '.join(i.strip() for i in sorted(recipe['ingredients'].split(',')))
                link = recipe['href']
                rows.append([title, ingr, link])
    
        except:
            break

    with open('Meal Finder.csv', 'w', newline='') as csvfile:
        headers = ['Meal', 'Ingredients', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(zip(headers, row)))

            
meal_finder('garlic','onion','beef')
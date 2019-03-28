# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:24:37 2019

@author: Fbasham

"""
import requests
from bs4 import BeautifulSoup

'''
page requests the URL 
soup parses the html
conc finds the class of the output result of CAD to USD
'''

page = requests.get('https://www.x-rates.com/calculator/?from=CAD&to=USD&amount=1')
soup = BeautifulSoup(page.text, 'html.parser')
conv = soup.find(class_ = 'ccOutputRslt')


'''
[0:8] returns slice of the string from 'conv' because 'conv' returns ('x.xxxxxxx USD').  
Float returns the string to a float value
''' 

rate = float(conv.get_text()[0:8])
print(rate)
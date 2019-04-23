# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:24:37 2019
@author: Fbasham
"""

import requests
from bs4 import BeautifulSoup


def convert_money(from_, to, amount):
    url = 'https://www.x-rates.com/calculator/'     
    payload = {'from': from_, 'to': to, 'amount': amount}    
    page = requests.get(url, params=payload)
    
    soup = BeautifulSoup(page.text, 'lxml')
    conv = soup.find(class_ = 'ccOutputRslt')
    
    rate = float(conv.text.split()[0])
    print(f'{amount} {from_} = {rate} {to}')

#Example function call    
convert_money('CAD', 'USD', 1000)

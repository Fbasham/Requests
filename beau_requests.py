import requests
import re
import pandas as pd
import os
import datetime

with requests.Session() as s:
    
    # regex is used because 'lWebIdx' appears to be dynamically generated upon login, thus,
    # it's found and inserted into the payload for the form data used to generate the report
    
    login = {'sWebNam': 'fbasham', 'sWebPwd': 'python92', 'Login': 'Login'}
    
    r = s.get('https://beauharnois.nglsupply.com/lognverf.htm?', params = login)
    m = re.findall('(lWebIdx=\d+)', r.text)
    m = m[0].split('=')
   
    day, month, year = datetime.datetime.today().strftime('%d/%m/%Y').split('/')
    
    payload = {'lWebIdx': m[1], 
               'iRepNum': '15', 
               'iRepDes': '0', 
               'dStrTim': f'{month}/1/{year} 12:00:00 AM',
               'dEndTim': f'{month}/{int(day)-1}/{year} 11:59:59 PM',
               'sDbsNam': 'TMSTRN.MDB'}
    
    report = s.get('https://beauharnois.nglsupply.com/reptprnt.htm?', params = payload)

       
    with open('Beau_Customer_Detail_Report.html', 'w') as f:
        f.write(report.text)
        dfs = pd.read_html('Beau_Customer_Detail_Report.html')
        df = pd.concat([dfs[1].iloc[7:]] + dfs[2:])
        df.to_csv('Beau_Customer_Detail_Report.csv', index=False)
        
    
    os.remove('Beau_Customer_Detail_Report.html')
    
    
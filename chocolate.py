from requests_html import HTMLSession
import pandas as pd
import io



with HTMLSession() as s:
    payload = {'sWebNam': 'fbasham',
               'sWebPwd': 'python92'}

    r = s.get('https://beauharnois.nglsupply.com/lognverf.htm', params=payload)
    webidx = r.html.search('webidx={}&')[0]


    payload = {
        'lWebIdx': webidx,
        'iRepNum': 15,
        'iRepDes': 1,
        'iRepExp': 19,
        'dStrTim': '9/1/2018 12:00:00 AM',
        'dEndTim': '9/15/2019 11:59:59 PM',
        'sDbsNam': 'TMSTRN.MDB'
        }

    r = s.get('https://beauharnois.nglsupply.com/reptprnt.htm', params=payload)
    r = s.get('https://beauharnois.nglsupply.com/zfbasham.xls')
    
    df = pd.read_excel(io.BytesIO(r.content), header=8)
    df = df[['Customer', 'Ticket', 'Date/Time', 'Net']]

    df = df.dropna(0, how='all')
    df['Customer'] = df['Customer'].ffill()
    df = df.dropna(0, how='any')
    df.to_csv('beau.csv', index=False)


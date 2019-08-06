from requests_html import HTML, HTMLSession
import pandas as pd
import aiohttp
import asyncio
import re
import time

t1 = time.time()

TERMINALS = ['putnam', 'milford', 'beauharnois', 'brigham']
URL = 'https://{}.nglsupply.com/reptcrit.htm?lWebIdx={}&iRepNum=1&iTckLst={}&sRepDat=TMSTRN.MDB'
USER = 'fbasham'
PASS = 'python92'


##with HTMLSession() as s:
##    dfs = []
##    for terminal in TERMINALS:
##        payload = {'sWebNam': USER,
##                   'sWebPwd': PASS,
##                   'Login': 'Login'}
##        r = s.get(f'https://{terminal}.nglsupply.com/lognverf.htm', params=payload)
##        webidx = re.findall('WebIdx=(\d+)', r.text)[0]
##        
##        for page in range(0,50,25):
##            r = s.get(f'https://{terminal}.nglsupply.com/reptcrit.htm?lWebIdx={webidx}&iRepNum=1&iTckLst={page}&sRepDat=TMSTRN.MDB')
##            table = r.html.find('table')[1].html
##            df = pd.read_html(table, header=2)[0].dropna(axis=1, how='all').assign(terminal=terminal)
##            dfs.append(df)
##    df = pd.concat(dfs)
##    print(df)
        



async def get_tickets(url, terminal, s):
    async with s.get(url) as resp:
        h = await resp.text()
        html = HTML(html=h)
        table = html.find('table')[1].html
        df = pd.read_html(table, header=2)[0].dropna(axis=1, how='all').assign(terminal=terminal)
        return df


async def main():
    async with aiohttp.ClientSession() as s:
        tasks = []
        for terminal in TERMINALS:
            payload = {'sWebNam': USER,
                       'sWebPwd': PASS,
                       'Login': 'Login'}
            async with s.get(f'https://{terminal}.nglsupply.com/lognverf.htm', params=payload) as resp:
                text = await resp.text()
                webidx = re.findall('WebIdx=(\d+)', text)[0]

            for page in range(0,50,25):
                url = f'https://{terminal}.nglsupply.com/reptcrit.htm?lWebIdx={webidx}&iRepNum=1&iTckLst={page}&sRepDat=TMSTRN.MDB'
                tasks.append(get_tickets(url,terminal, s))
    
        dfs = await asyncio.gather(*tasks)
        df = pd.concat(dfs)
        return df

  
df = asyncio.run(main())
print(df)

t2 = time.time()
print(t2-t1)


    
            

    

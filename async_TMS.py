from requests_html import HTML
import pandas as pd
import aiohttp
import asyncio
import re
import time

t1 = time.time()

TERMINALS = ['putnam', 'brigham', 'beauharnois', 'milford']
URL = 'https://{}.nglsupply.com/reptcrit.htm?lWebIdx={}&iRepNum=1&iTckLst={}&sRepDat=TMSTRN.MDB'
USER = 'fbasham'
PASS = 'python92'

async def get_session(terminal, s):
    payload = {'sWebNam': USER,
               'sWebPwd': PASS,
               'Login': 'Login'}
    async with s.get(f'https://{terminal}.nglsupply.com/lognverf.htm', params=payload) as resp:
        text = await resp.text()
        webidx = re.findall('WebIdx=(\d+)', text)[0]
    return (s, webidx, terminal)


async def get_tickets(page, session_params):
    s, webidx, terminal = session_params
    url = URL.format(terminal, webidx, page)
    async with s.get(url) as resp:
        h = await resp.text()
        html = HTML(html=h)
        table = html.find('table')[1].html
        df = pd.read_html(table, header=2)[0].dropna(axis=1, how='all').assign(terminal=terminal)
        return df


async def main():
    async with aiohttp.ClientSession() as s:
        sessions = [await get_session(terminal, s) for terminal in TERMINALS]
        dfs = await asyncio.gather(*[get_tickets(page, session) for session in sessions
                                       for page in range(0,100,25)])
        df = pd.concat(dfs)
        return df
            
    
df = asyncio.run(main())
print(df)

t2 = time.time()
print(t2-t1)


    
            

    

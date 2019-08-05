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


async def get_webidx(s, terminal):
    payload = {'sWebNam': USER,
               'sWebPwd': PASS,
               'Login': 'Login'}
    async with s.get(f'https://{terminal}.nglsupply.com/lognverf.htm', params=payload) as resp:
        text = await resp.text()
        webidx = re.findall('WebIdx=(\d+)', text)[0]
        return webidx


async def get_tickets(args, page):
    terminal, s, webidx = args    
    async with s.get(f'https://{terminal}.nglsupply.com/reptcrit.htm?lWebIdx={webidx}&iRepNum=1&iTckLst={page}&sRepDat=TMSTRN.MDB') as resp:
        h = await resp.text()
        html = HTML(html=h)
        table = html.find('table')[1].html
        df = pd.read_html(table, header=2)[0].dropna(axis=1, how='all').assign(terminal=terminal)
        return df


async def main():
    sessions = [aiohttp.ClientSession() for terminal in TERMINALS]
    args = [(terminal, session, await get_webidx(session, terminal)) for terminal, session in zip(TERMINALS, sessions)]

    dfs = await asyncio.gather(*[get_tickets(arg, page) for arg in args for page in range(0,50,25)])
    df = pd.concat(dfs)
    for s in sessions:
        await s.close()
    return df

  
df = asyncio.run(main())
print(df)

t2 = time.time()
print(t2-t1)


    
            

    

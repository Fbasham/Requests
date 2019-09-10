from requests_html import AsyncHTMLSession
from functools import wraps, partial
import asyncio


class Test:
    
    def async_run(func):
        def wrapper(*args, **kwargs):
            return asyncio.run(func(*args, **kwargs))
        return wrapper

    def tasker(func):
        def wrapper(*args, **kwargs):
            return partial(func, *args, **kwargs)
        return wrapper
    
    @tasker
    async def work(self, session, url, **kwargs):
        return await session.request(url=url,**kwargs)
    
    @async_run
    async def scrape(self, urls, session=None, **kwargs):  
        s = session or AsyncHTMLSession()
        s.loop= asyncio.get_event_loop()
        tasks = (self.work(url=url, **kwargs)(s) for url in urls)
        return await asyncio.gather(*tasks)
    


#Example of passing in own session:
async def get_session():
    s = AsyncHTMLSession()
    payload = {'sWebNam': 'username', 'sWebPwd': 'pass', 'Login': 'Login'}
    r = await s.get('https://company.website.com/lognverf.htm', params=payload)
    webidx = r.html.search('lWebIdx={}&')[0]
    return s, webidx

session, webidx = asyncio.run(get_session())

base = 'https://company.website.com/reptcrit.htm?lWebIdx={}&iRepNum=1&iTckLst={}&sRepDat=TMSTRN.MDB'
urls = (base.format(webidx, ticket) for ticket in range(0,200,25))
r = Test()

for r in r.scrape(urls, session=session, method='get', headers=None):
    print(r.content)

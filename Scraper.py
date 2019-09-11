from requests_html import AsyncHTMLSession
from functools import wraps, partial
import asyncio


class Test:
    
    def async_run(func):
        def wrapper(*args, **kwargs):
            return asyncio.run(func(*args, **kwargs))
        return wrapper

    def tasker(func):
        '''this function isn't necessary and might become deprecated in the future'''
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
    


#Example 1: Passing in created session:

@Test.async_run
async def get_session():
    s = AsyncHTMLSession()
    payload = {'sWebNam': 'username', 'sWebPwd': 'pass', 'Login': 'Login'}
    r = await s.get('https://company.website.com/lognverf.htm', params=payload)
    webidx = r.html.search('lWebIdx={}&')[0]
    return s, webidx

session, webidx = get_session()

base = 'https://company.website.com/reptcrit.htm?lWebIdx={}&iRepNum=1&iTckLst={}&sRepDat=TMSTRN.MDB'
urls = (base.format(webidx, ticket) for ticket in range(0,200,25))
r = Test()

for r in r.scrape(urls, session=session, method='get', headers=None):
    print(r.content)
    
    
   
#Example 2: 
r = Test()
urls = ['http://website.com/login']
payload = {'sUsrNam': 'username', 'sUsrPwd': 'password'}
s = r.scrape(urls, method='post', data=payload)[0]

base = 'http://website.com/ticket?iSchOrd=0&lSchMax=50&lSchCnt={}'
urls = (base.format(ticket) for ticket in range(0,200,50))
for r in r.scrape(urls, method='get', session=s.session):
    print(r.content)

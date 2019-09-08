from requests_html import AsyncHTMLSession
import asyncio
from functools import wraps, partial


class Test():

    def __init__(self, urls):
        self.urls = urls
        self.tasks = None
        
    def async_run(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = asyncio.run(func(self, *args, **kwargs))
            return result
        return wrapper    

    @async_run
    async def scrape(self):
        session = AsyncHTMLSession()
        tasks = (task(session) for task in self.tasks)
        return await asyncio.gather(*tasks)



def tasker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task = partial(func, *args, **kwargs)
        return task
    return wrapper

@tasker
async def work(session, method, url):
    return await session.request(method, url)



urls = ('https://www.google.com', 'https://www.reddit.com', 'https://www.python.org',
        'https://stackoverflow.com/questions', 'https://httpbin.org/')

r = Test(urls)
r.tasks = (work(method='get', url=url) for url in urls)
for r in r.scrape():
    print(r.content)
    



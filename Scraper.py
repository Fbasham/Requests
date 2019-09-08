from requests_html import AsyncHTMLSession
from functools import wraps, partial
import asyncio


class Test():

    def __init__(self, tasks=None):
        self.tasks = tasks
        
    def _async_run(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = asyncio.run(func(self, *args, **kwargs))
            return result
        return wrapper

    def _tasker(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            task = partial(func, *args, **kwargs)
            return task
        return wrapper

    @_tasker
    async def work(session, **kwargs):
        return await session.request(**kwargs)

    @_async_run
    async def scrape(self):
        session = AsyncHTMLSession()
        tasks = (task(session=session) for task in self.tasks)
        return await asyncio.gather(*tasks)


    
urls = ('https://www.google.com', 'https://www.reddit.com', 'https://www.python.org',
        'https://stackoverflow.com/questions', 'https://httpbin.org/')

tasks = (r.work(method='get', url=url) for url in urls)

r = Test(tasks)
print(r.scrape())

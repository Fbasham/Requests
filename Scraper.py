import asyncio
from requests_html import AsyncHTMLSession


class Scraper:
    
    def __init__(self, urls=None):
        self._urls = urls

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, new_urls):
        if not isinstance(new_urls, (list, set, tuple)):
            raise TypeError('urls need to be iterable')             
        self._urls = new_urls


    def async_scrape(self, method):
        
        async def work(session, method, url):
            r = await session.request(method, url)
            return r

        async def main():
            session = AsyncHTMLSession()
            tasks = (work(session, method, url) for url in self.urls)
            results = await asyncio.gather(*tasks)
            return results

        return asyncio.run(main())
        

    

urls = ('https://www.google.com', 'https://www.reddit.com', 'https://www.python.org')
s = Scraper(urls)
responses = s.async_scrape('get')
for r in responses:
    print(len(r.content))




from requests_html import HTML, AsyncHTMLSession

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from pyppeteer import launch

import time
from math import ceil
import asyncio
import csv


class Jobs:
    BASE = 'https://emploisfp-psjobs.cfp-psc.gc.ca'
    
    def __init__(self, driver='selenium', headless=True):
        self.driver = driver
        self.headless = headless

    @property
    def links(self):
        '''returns list of job urls'''
        assert hasattr(self, '_jobs'), 'must run get_all_jobs to access this atrribute'
        return self._jobs

    @property
    def responses(self):
        '''returns list of request response objects'''
        assert hasattr(self, '_responses'), 'must run get_all_jobs to access this atrribute'
        return self._responses
    
    def get_all_jobs(self):
        
        jobs = []
                 
        if self.driver == 'selenium':
            
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(f'{self.BASE}/psrs-srfp/applicant/page2440?requestedPage=1')
            time.sleep(5)

            wait = WebDriverWait(driver, 60)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Next")]')))
            content = driver.page_source
            html = HTML(html=content)
            total_jobs = int(html.search('Jobs open to the public ({})')[0])
            total_pages = ceil(total_jobs/20)

            for page_num in range(1, total_pages+1):
                print(f'getting page {page_num}')
                driver.get(f'{self.BASE}/psrs-srfp/applicant/page2440?requestedPage={page_num}')
                content = driver.page_source
                html = HTML(html=content)
                links = html.find('a[href*="poster"]')
                for link in links:
                    jobs.append(link)

            driver.close()

                 
        if self.driver == 'pyppeteer':
                 
            async def main():
                browser = await launch({'args': ['--no-sandbox'], 'headless': self.headless})
                page = await browser.newPage()
                await page.goto(f'{self.BASE}/psrs-srfp/applicant/page2440?requestedPage=1')
                await asyncio.sleep(3)

                content = await page.content()
                html = HTML(html=content)
                total_jobs = int(html.search('Jobs open to the public ({})')[0])
                total_pages = ceil(total_jobs/20)
                
                for page_num in range(1, total_pages+1):

                    if self.headless:
                        if page_num%10 == 0:
                            await page.close()
                            await browser.close()
                            browser = await launch({'args': ['--no-sandbox'], 'headless': self.headless})
                            page = await browser.newPage()
                            await page.goto(f'{self.BASE}/psrs-srfp/applicant/page2440?requestedPage=1')
                            await asyncio.sleep(3)
                    
                    print(f'getting page {page_num}')
                    target = f'{self.BASE}/psrs-srfp/applicant/page2440?requestedPage={page_num}'
                    await page.goto(target)     
                    content = await page.content()                    
                    html = HTML(html=content)
                    links = html.find('a[href*="poster"]')
                    for link in links:
                        jobs.append(link)
                        
                await browser.close()
            asyncio.run(main())
            

        if self.driver == 'requests':

            def main():
                def get_session():
                    s = HTMLSession()
                    r = s.get('https://emploisfp-psjobs.cfp-psc.gc.ca/psrs-srfp/applicant/page2440?requestedPage=1')
                    r.html.render(sleep=3)
                    return s, r
                _, r = get_session()
                total_jobs = int(r.html.search('Jobs open to the public ({})')[0])
                total_pages = ceil(total_jobs/20)

                for page_num in range(1, total_pages+1):
                    if page_num%10 == 0:
                        s, _ = get_session()
                    print(f'getting page {page_num}')              
                    target = f'https://emploisfp-psjobs.cfp-psc.gc.ca/psrs-srfp/applicant/page2440?requestedPage={page_num}'
                    r = s.get(target)
                    r.html.render()
                    links = r.html.find('a[href*="poster"]')
                    for link in links:
                        jobs.append(link)
                    print(len(links))

                return jobs
            main()

        self._jobs = jobs
        return jobs
                

    def scrape_jobs(self):
        assert hasattr(self, '_jobs'), 'must run get_all_jobs before this method'
        async def get_poster(s, poster):
            r = await s.get(f'{self.BASE}{poster}')
            return poster, r

        async def main():
            s = AsyncHTMLSession()
            tasks = (get_poster(s, poster.attrs.get('href')) for poster in self._jobs)
            return await asyncio.gather(*tasks)

        self._responses = asyncio.run(main())
        return self._responses


    def run(self):
        '''convienience method for running get_all_jobs and scrape_jobs syncronously'''
        self.get_all_jobs()
        self.scrape_jobs()
        return self
    

    def find(self, query):
        assert hasattr(self, '_responses'), 'must run scrape_jobs before this method'     
        matches = []
        for poster, response in self._responses:
            match = f'{self.BASE}{poster}'
            if '|' in query:
                queries = query.split('|')
                if any(q.lower() in response.text.lower() for q in queries):
                    matches.append(match)

            if '&' in query:
                queries = query.split('&')
                if all(q.lower() in response.text.lower() for q in queries):
                    matches.append(match)
           
            else:
                if query.lower() in response.text.lower():
                    matches.append(match)
                    
        self._matches = matches              
        return matches


    def to_csv(self, filepath):
        assert hasattr(self, '_matches'), 'must run find method before accessing this method'
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in self._matches:
                writer.writerow([row])
        return self
    

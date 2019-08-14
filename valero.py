from requests_html import AsyncHTMLSession
import asyncio
import PyPDF2
import io


async def main():
    s = AsyncHTMLSession()
    r = await s.get('https://ca.valero.com/en-ca/')

    payload = {'username': 'liz dennis',
               'password': 'kIckbutt71',
               'vhost': 'standard'}

    r = await s.post('https://login.valero.com/my.policy', data=payload)

    r = await s.get('https://ca.valero.com/en-ca/_layouts/15/appredirect.aspx?instance_id=%7BE41FAC78-A231-49D8-BAE7-F0D10F4CF11D%7D')

    url = r.html.find('form#frmRedirect', first=True).attrs.get('action')
    data = {elem.attrs.get('name'): elem.attrs.get('value') for elem in r.html.find('input[type=hidden]')}
    headers = {'Referer': r.url}
    r = await s.post(url, data=data, headers=headers)


    data = {'optionSelected': 'DateRange',
            'startDate': '13/07/2019',
            'endDate': '12/08/2019'}
    headers.update({'Referer': 'https://wpapps.valero.com/InvoicesWeb?SPHostUrl=https%3A%2F%2Fca%2Evalero%2Ecom%2Fen%2Dca'})
    r = await s.post('https://wpapps.valero.com/InvoicesWeb', data=data, headers=headers)

    links = [link for link in r.html.absolute_links if 'invoiceNum' in link]

    await asyncio.gather(*(get_pdf(url, headers, s) for url in links))


async def get_pdf(url, headers, s):
    r = await s.post(url, headers=headers)
    pdf = PyPDF2.PdfFileReader(io.BytesIO(r.content))
    text = pdf.getPage(0).extractText()
    

asyncio.run(main())


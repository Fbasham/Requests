from requests_html import HTMLSession

with HTMLSession() as s:

    r = s.get('https://ca.valero.com/en-ca/')
    
    payload = {'username': 'liz dennis',
               'password': 'kIckbutt71',
               'vhost': 'standard'}

    r = s.post('https://login.valero.com/my.policy', data=payload)

    r = s.get('https://ca.valero.com/en-ca/_layouts/15/appredirect.aspx?instance_id=%7BE41FAC78-A231-49D8-BAE7-F0D10F4CF11D%7D')

    url = r.html.find('form#frmRedirect', first=True).attrs.get('action')
    data = {elem.attrs.get('name'): elem.attrs.get('value') for elem in r.html.find('input[type=hidden]')}
    headers = {'Referer': r.url}
    r = s.post(url, data=data, headers=headers)


    data = {'optionSelected': 'DateRange',
            'startDate': '13/07/2019',
            'endDate': '12/08/2019'}
    headers.update({'Referer': 'https://wpapps.valero.com/InvoicesWeb?SPHostUrl=https%3A%2F%2Fca%2Evalero%2Ecom%2Fen%2Dca'})
    r = s.post('https://wpapps.valero.com/InvoicesWeb', data=data, headers=headers)

    #needs ansyncio for concurrent pdf text extraction
    links = list(r.html.absolute_links)
    for link in links:
        r = s.get(link, headers=headers)


from bs4 import BeautifulSoup
import csv

with open(r'C:\Users\Bash\Downloads\Grafton & Upton Railroad_files/reports.html', 'r') as file:

    soup = BeautifulSoup(file, 'lxml')
    div = soup.find_all('div')

    x = [i.span.text.replace('\xa0',' ') if i.span else None for i in div]

    # create a list of the indexes of all None types in x
    idx = [i for i, _ in enumerate(x) if _ is None]


    with open('test.csv', 'w', newline='') as csvfile:
        
        headers = ['Inventory', 'Net', 'End Time', 'Driver', 'Carrier', 'Consignee',
                   'BOL2', 'BOL', 'Supplier', 'Railcar']

        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        
        #create a list of lists using slices between the None type indexes
        for i in range(len(idx)-1):
            row = x[idx[i]+1:idx[i+1]]
            if len(row) in [7,9]:
                if len(row) is 7:
                    for j in range(3):
                        row.insert(3,'')
                else:
                    row.insert(-3,'')

                writer.writerow(dict(zip(headers,row)))


    
    

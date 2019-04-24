import pandas as pd
import os
import time
import csv

### instantiate a time (purely for performance checking - not at all necessary to work)
start = time.time()

### Grab newest file in directory
dirname = r'H:\E1 Uploads\Livingston\Raw Data'
filenames = os.listdir(dirname)
filepaths = [os.path.join(dirname, filename) for filename in filenames]
files = [f for f in filepaths if not os.path.isdir(f)]
newest_file = max(files, key=lambda x: os.stat(x).st_mtime)


### Reads file and cleans it up, filters out junk rows containing ('65071525-1784') and blank rows
df = pd.read_excel(newest_file,skiprows = 7)
df = df.iloc[:-10]
df['Rail Car #'] = df['Rail Car #'].shift(-1).str[:4]
df = df.drop(['Permit No', 'Tariff No', 'Description', 'Entry Value', 'Carrier', 'Duty', 'MPF', 'HMF','Other Charges'], axis = 1)
df = df.dropna(how = 'any')
df = df.drop(df[df['Reference '] == '65071525-17854'].index).reset_index(drop = True)


### Create a dataframe for all header rows in final output
df_header = pd.DataFrame({'Header - H' : ['H']*len(df),
                   'Invoice Type': ['Purchase']*len(df),
                   'Pay Rec Flag': ['P']*len(df),
                   'Invoice Reference Number': df['Invoice #'].tolist(),
                   'Issue Date': df['Date'].tolist(),
                   'Lock Issue Flag Date': ['Y']*len(df),
                   'Account': pd.to_numeric(['20001']*len(df)),
                   'Currency': ['USD']*len(df),
                   'BU': ['NGL Supply Co. Ltd.']*len(df),
                   'BU contact': '',
                   'BU Location': '',
                   'Stakeholder': ['Livingston International Inc.']*len(df),
                   'Stakeholder Contact': ['Account Receviable']*len(df),
                   'Remit Location': ['405 The West Mall Suite 400 Toronto, ON M9C 5K7 ']*len(df),
                   'Stakeholder Location': '',
                   'Invoice Mode': ['Hard Copy']*len(df),
                   'Payment Terms': ['On Receipt of Invoice']*len(df),
                   'Payment Mode': '',
                   'Due Date': time.strftime('%m/%d/%Y'),
                   'Lock Due Date Flag': ['Y']*len(df),
                   'Discount Date': '',
                   'Lock Discount Flag': ['Y']*len(df),
                   'Payment Attach Flag': ['Y']*len(df),
                   'Payment Seperated Cheque Flag': ['Y']*len(df),
                   'Payment Description': '',
                   'Voucher': '',
                   'Invoice Format': ['Standard Layout (P)']*len(df)
                   })


### Create a dataframe for all detail rows in final output

cost_type =    {'BNSF':	'Brokerage Fee Expense',
                'CMQQ':	'Transp. Freight Exp - Rail',
                'CNRU':	'Brokerage Fee Expense',
                'CPRS':	'Brokerage Fee Expense',
                'CSXR':	'Brokerage Fee Expense',
                'NOGT':	'3rd Party  Brokerage Exp',
                'NSRR':	'Brokerage Fee Expense',
                'UPRR':	'Brokerage Fee Expense'}
                
            
df_detail = pd.DataFrame({'Detail - D': ['D']*len(df),
                   'Account': pd.to_numeric(['12002']*len(df)),
                   'Amount': [-i for i in df['Pay To Livingston USD'].tolist()],
                   'Qty': '',
                   'UoM': '',
                   'BOL/Ticket': df['Reference '].tolist(),
                   'Effective Date': df['Import Date'].tolist(),
                   'Description': ['Customs Fee']*len(df),
                   'ACL': '',
                   'Inventory': '',
                   'Location': '',
                   'Cost Type': df['Rail Car #'].map(cost_type),
                   'Cost Center': '',
                   'Business Unit': '',
                   'Resp Center': '',
                   'Origin Location': '',
                   'Destination Location': '',
                   'Product': '',
                   'Invoice Reference Number': ''
                   })


timestamp = time.strftime('%Y.%m.%d.%H%M')
path = r'H:\E1 Uploads\Livingston\Outbox\csv\\'
rows = list(zip(df_header.values.tolist(), df_detail.values.tolist()))
with open(f'{path}{timestamp} - Livingston Upload.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    
    for row in rows:
        header, detail = row
        writer.writerow(header)
        writer.writerow(detail)


end = time.time()
print('Time to run: ' + "{0:.2f}".format(end-start) + ' seconds')
print('If you\'re lost, this file is located in: H:\E1 Uploads\Livingston\Outbox\csv')
time.sleep(5)
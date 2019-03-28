import pandas as pd
import numpy as np
import os
import time

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
                   'BU contact': np.nan,
                   'BU Location': np.nan,
                   'Stakeholder': ['Livingston International Inc.']*len(df),
                   'Stakeholder Contact': np.nan,
                   'Remit Location': ['405 The West Mall Suite 400 Toronto, ON M9C 5K7 ']*len(df),
                   'Stakeholder Location': np.nan,
                   'Invoice Mode': ['Hard Copy']*len(df),
                   'Payment Terms': ['On Receipt of Invoice']*len(df),
                   'Payment Mode': np.nan,
                   'Due Date': time.strftime('%m/%d/%Y'),
                   'Lock Due Date Flag': ['Y']*len(df),
                   'Discount Date': np.nan,
                   'Lock Discount Flag': ['Y']*len(df),
                   'Payment Attach Flag': ['Y']*len(df),
                   'Payment Seperated Cheque Flag': ['Y']*len(df),
                   'Payment Description': np.nan,
                   'Voucher': np.nan,
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
                   'Qty': np.nan,
                   'UoM': np.nan,
                   'BOL/Ticket': df['Reference '].tolist(),
                   'Effective Date': df['Import Date'].tolist(),
                   'Description': ['Customs Fee']*len(df),
                   'ACL': np.nan,
                   'Inventory': np.nan,
                   'Location': np.nan,
                   'Cost Type': df['Rail Car #'].map(cost_type),
                   'Cost Center': np.nan,
                   'Business Unit': np.nan,
                   'Resp Center': np.nan,
                   'Origin Location': np.nan,
                   'Destination Location': np.nan,
                   'Product': np.nan,
                   'Invoice Reference Number': np.nan
                   })


### Combines the two dataframes into an output file
writer = pd.ExcelWriter('Livingston_python.xlsx', engine = 'xlsxwriter')
dflist = []
for i in range(len(df)):
    
    df_header.loc[[i]].to_excel(writer, sheet_name = 'Header' + str(i), index = False, header = False)    
    df_detail.loc[[i]].to_excel(writer, sheet_name = 'Detail' + str(i), index = False, header = False)
    dflist.append(df_header.loc[[i]])
    dflist.append(df_detail.loc[[i]])
    
writer.save()


def multiple_dfs(DataFrameList, sheets, file_name, spaces):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
    row = 0
    
    for dataframe in DataFrameList:
            dataframe.to_excel(writer,sheet_name=sheets,startrow=row , startcol=0, index = False, header = False)   
            row = row + len(dataframe.index) + spaces
                       
    writer.save()

file_timestamp = time.strftime('%Y_%m_%d_%H%M')
filename_xlsx = r'H:\E1 Uploads\Livingston\Outbox\xlsx\Livingston Invoice Upload_' + file_timestamp + '.xlsx'
multiple_dfs(dflist, 'Validation', filename_xlsx, 0) 


### Convert .xlsx to .csv for upload (optional)
dirname_xlsx_uploads = r'H:\E1 Uploads\Livingston\Outbox\xlsx'
filenames = os.listdir(dirname_xlsx_uploads)
filepaths = [os.path.join(dirname_xlsx_uploads, filename) for filename in filenames]
files = [f for f in filepaths if not os.path.isdir(f)]
newest_xlsx_uploads = max(files, key=lambda x: os.stat(x).st_mtime)


filename_csv = r'H:\E1 Uploads\Livingston\Outbox\csv\Livingston Invoice Upload_' + file_timestamp + '.csv'
df_xlsxtocsv = pd.read_excel(newest_xlsx_uploads) 


############ When pandas reads excel files it assigns an index in the first column and any blank headers with a string  #####  
############ To avoid that for the uplod, we rename the assigned headers with blank ones in the following code: #############  

df_renamecols = df_xlsxtocsv.rename(columns={'Unnamed: 9' : '', 'Unnamed: 10': '', 'Unnamed: 12': '', 'Unnamed: 13': '',
                                             'Unnamed: 14': '', 'Unnamed: 17': '', 'Unnamed: 20': '', 'Unnamed: 24': '',
                                             'Unnamed: 25': '', 'Y.1': 'Y', 'Y.2': 'Y', 'Y.3': 'Y', 'Y.4': 'Y'})

csv_upload = df_renamecols.to_csv(filename_csv, index=False)


### clean up processes and performance printing
os.remove('Livingston_python.xlsx')
end = time.time()
print('Time to run: ' + "{0:.2f}".format(end-start) + ' seconds')
print('\n')
print('The converted raw data is saved as: Livingston Invoice Upload_' + file_timestamp + '.csv')
print('\n')
print('If you\'re lost, this file is located in: H:\E1 Uploads\Livingston\Outbox\csv')
time.sleep(10)
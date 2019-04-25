# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 08:30:15 2018

@author: fbasham
"""

import pandas as pd
import os
import time
import csv


date_today = time.strftime('%Y.%m.%d.%H%M')

#############################################################################################################################
#################  Grab newest file saved in 'raw data folder'  #############################################################
#############################################################################################################################

dirname = 'H:\FBasham\Raw Data'
filenames = os.listdir(dirname)
filepaths = [os.path.join(dirname, filename) for filename in filenames]
files = [f for f in filepaths if not os.path.isdir(f)]
newest = max(files, key=lambda x: os.stat(x).st_mtime)


start = time.time()

#############################################################################################################################
################# Top Half Code #############################################################################################
#############################################################################################################################

datafile_raw = pd.read_excel(newest)
sort_df = datafile_raw.sort_values(by=['Numbered','PickupTicket'])
cols = list(sort_df.columns.values)
count = len(sort_df)
invoiceref = sort_df['Numbered']
uniqueIR = invoiceref.unique()

index = range(count)
header = ['H']*len(sort_df)
invoicetype = ['Purchase']*len(sort_df)
payrecflag = ['P']*len(sort_df)
invoiceref = sort_df['Numbered'].tolist()
issuedate = sort_df['Dated'].dt.strftime('%m/%d/%Y').tolist()
lockissueflagdate = ['Y']*len(sort_df)
accounttop = pd.to_numeric(['20001']*len(sort_df))
currency = ['USD']*len(sort_df)
BU = ['NGL Supply Co. Ltd.']*len(sort_df)
BUcontact = ''
BUloc = ''
stakeholder = ['Legend LLC (New)']*len(sort_df)
stakecontact = ''
remitloc = ''
stakeloc = ''
invoicemode = ['Hard Copy']*len(sort_df)
payterms = ['On Receipt of Invoice']*len(sort_df)
paymode = ''
datedue = sort_df['DateDue'].dt.strftime('%m/%d/%Y').tolist()
lockduedateflag = ['Y']*len(sort_df)
discountdate = ''
lockdisflag = ['Y']*len(sort_df)
payattflag = ['Y']*len(sort_df)
paysepflag = ['Y']*len(sort_df)
paydesc = ''
voucher = ''
invoiceformat = ['Standard Layout (P)']*len(sort_df)

df = pd.DataFrame({'Header - H' : header,
                   'Invoice Type': invoicetype,
                   'Pay Rec Flag': payrecflag,
                   'Invoice Reference Number': invoiceref,
                   'Issue Date': issuedate,
                   'Lock Issue Flag Date': lockissueflagdate,
                   'Account': accounttop,
                   'Currency': currency,
                   'BU': BU,
                   'BU contact': BUcontact,
                   'BU Location': BUloc,
                   'Stakeholder': stakeholder,
                   'Stakeholder Contact': stakecontact,
                   'Remit Location': remitloc,
                   'Stakeholder Location': stakeloc,
                   'Invoice Mode': invoicemode,
                   'Payment Terms': payterms,
                   'Payment Mode': paymode,
                   'Due Date': datedue,
                   'Lock Due Date Flag': lockduedateflag,
                   'Discount Date': discountdate,
                   'Lock Discount Flag': lockdisflag,
                   'Payment Attach Flag': payattflag,
                   'Payment Seperated Cheque Flag': paysepflag,
                   'Payment Description': paydesc,
                   'Voucher': voucher,
                   'Invoice Format': invoiceformat
                   })


df_out = df.drop_duplicates('Invoice Reference Number').reset_index(drop=True)


#############################################################################################################################
################# Bottom Half Code ##########################################################################################
#############################################################################################################################

cost_type_dict = {"Delay- Unload": "Truck Demurrage - Offloading", 
                  "Delay- Load": "Truck Demurrage - Loading",
                  "Butane": "Transp. Freight Exp - Truck", 
                  "FUEL": "Transp. FuelS/CE", 
                  "ISO Butane": "Transp. Freight Exp - Truck", 
                  "Com Butane": "Transp. Freight Exp - Truck", 
                  "Load Min- NC4": "Transp. Freight Exp - Truck", 
                  "Propane": "Transp. Freight Exp - Truck",
                  "Butane Mix": "Transp. Freight Exp - Truck",
                  "Nat. Gasoline": "Transp. Freight Exp - Truck"
                  }


index = range(count)
detail = ['D']*len(sort_df)
accountbot = pd.to_numeric(['12008']*len(sort_df))
amount = [-1 * i for i in sort_df['DSalePrice'].tolist()]
qty = ''
uom = ''
BOLticket = sort_df['PickupTicket'].tolist()
effectivedate = sort_df['PickupDate'].dt.strftime('%m/%d/%Y').tolist()
description = sort_df['Product'].tolist()
acl = ''
inventory = ''
location = ''
costtype = sort_df['Product'].map(cost_type_dict)
costcenter = ''
busunit = ''
respcenter = ''
orgloc = ''
enduse = ''
destloc = ''
product = ''
invoiceref = sort_df['Numbered'].tolist()


df_out_init = pd.DataFrame({'Detail - D': detail,
                   'Account': accountbot,
                   'Amount': amount,
                   'Qty': qty,
                   'UoM': uom,
                   'BOL/Ticket': BOLticket,
                   'Effective Date': effectivedate,
                   'Description': description,
                   'ACL': acl,
                   'Inventory': inventory,
                   'Location': location,
                   'Cost Type': costtype,
                   'Cost Center': costcenter,
                   'Business Unit': busunit,
                   'Resp Center': respcenter,
                   'Origin Location': orgloc,
                   'Destination Location': destloc,
                   'Product': product,
                   'Invoice Reference Number': invoiceref
                   })

                
df_out_fin = df_out_init.sort_values(by=['Invoice Reference Number','BOL/Ticket']).reset_index(drop=True)

#Write to csv
with open(f'H:\FBasham\csv uploads\{date_today} - Legend Upload.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    
    rows = []
    for i in uniqueIR:
          
        dftopi = df_out[df_out['Invoice Reference Number'] == i]
        df2 = df_out_fin[df_out_fin['Invoice Reference Number'] == i]
        df3 = df2.drop(columns = ['Invoice Reference Number'])
        
        rows.append(dftopi.values.tolist()[0])
        for details in df3.values.tolist():
            rows.append(details)
        
    for row in rows:
        writer.writerow(row)
 

########  Create Additonal Accrual File ###############################################################################

sort_dfAA = datafile_raw.sort_values(by=['Numbered','PickupTicket'])
dfAA = sort_dfAA[(sort_dfAA["Product"]=="Delay- Unload") | (sort_dfAA["Product"]=="Delay- Load") | (sort_dfAA["DVolume"]== 1) & (sort_dfAA["Product"]=="Nat. Gasoline")]

instr = ['UPDATE']*len(dfAA)
trnsqtype = ['A']*len(dfAA)
existingtrns = dfAA['PickupTicket'].tolist()
trnslktype = ['BOL/Ticket Ref']*len(dfAA)
trnslkbuyer = ['NGL Supply Co. Ltd.']*len(dfAA)
srcdate = dfAA['PickupDate'].dt.strftime('%m/%d/%Y').tolist()
trnslkdate = dfAA['PickupDate'].dt.strftime('%m/%d/%Y').tolist()
accseq = ['Transportation']*len(dfAA)
accdir = ['Payable']*len(dfAA)
accstk = ['Legend LLC (New)']*len(dfAA)
accbusunit = ['NGL Supply Co. Ltd.']*len(dfAA)
costypeacc = dfAA['Product'].map(cost_type_dict)
unitcost = [-1 * i for i in dfAA['DSalePrice'].tolist()] 
accuom = ['Each']*len(dfAA)
acurr = ['USD']*len(dfAA)
accratetype = ['Daily Average']*len(dfAA)
accinvcntrl = ['Eligible']*len(dfAA)


addaccrual = pd.DataFrame({'Instruction Code': instr,
                           'Transaction Qty Type': trnsqtype,
                           'Existing Transaction': existingtrns,
                           'Trans Lookup Type': trnslktype,
                           'Trans Lookup Buyer': trnslkbuyer,
                           'Src Trans Date': srcdate,
                           'Trans Lookup Date': trnslkdate,
                           'Accrual{1}:Seq': accseq,
                           'Accrual{1}:Direction': accdir,
                           'Accrual{1}:Stakeholder': accstk,
                           'Accrual{1}:Business Unit': accbusunit,
                           'Accrual{1}:Cost Type': costypeacc,
                           'Accrual{1}:Unit Cost': unitcost,
                           'Accrual{1}:UoM': accuom,
                           'Accrual{1}:Currency': acurr,
                           'Accrual{1}:Rate Type': accratetype,
                           'Accrual{1}:Invoice Control': accinvcntrl
                           })


addacc_filename_csv = 'H:/FBasham/csv uploads/Additional Accrual Legend Upload_' + date_today + '.csv'
addacc_csv = addaccrual.to_csv(addacc_filename_csv, index=False)




stop = time.time()

print(f'Time to run: {stop-start:.2f} seconds')
print()
print('If you\'re lost, this file is located in: H:/FBasham/csv uploads')
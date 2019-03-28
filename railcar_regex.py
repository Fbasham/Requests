import PyPDF2
#import textract
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
import re
from tkinter import *
import os

# nltk.download('punkt')
# nltk.download('stopwords')

car_list = []
vol_list = []
for root, dirs, files in os.walk(os.path.abspath(r'H:\FBasham\Grafton PDFs')):
    for file in files:

        filename = os.path.join(root, file)
        pdfFileObj = open(filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        num_pages = pdfReader.numPages
        count = 0
        text = ""
        
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count += 1
            text += pageObj.extractText()

        if text != "":
            text = text
        else:
            text = textract.process(filename, method='tesseract', language='eng')
            
        cars = re.findall('([A-Z]{3}[X]\s?[0-9]{4,6})', text)
        vol1 = re.findall('([3][0-9],[0-9]{3}[R][R]|[USG][3][0-9],[0-9]{3}[L])', text)
        for car in cars:
            car_list.append(car)
        for v in vol1:
            vol_list.append(v)
      

#unique_cars = list(set(car_list))
#unique_cars.sort()

x_list = []
y_list = []
for c in car_list:
    x = c.replace(" ", "")
    x_list.append(x)

for a in vol_list:
    y = a.strip('RR').strip('L').strip('G')
    y_list.append(y)
       


master_list = []
for el in x_list:
    split = re.split('(\s?[0-9]{4,6})', el)
    pad = split[1].rjust(6,'0')
    pad = split[1].strip('0')
    ID = split[0]
    concat = ID + pad
    master_list.append(concat)

lst = [[],[]]
for elem in master_list:
    lst[0].append(elem)
for elem in y_list:
    lst[1].append(elem) 


master = Tk()
car_label = Label(master, text ="Car Identification")
t = Text(master)
t.insert('1.0' , 'Railcar ID:' + '\n' + '\n')
for car in master_list:
    t.insert(END, car + '\n')
car_label.pack()
t.pack()

root = Tk()
vol_label = Label(root, text ="Volumes")
text = Text(root)
text.insert('1.0' , 'Railcar Volume:' + '\n' + '\n')
for vol in y_list:
    text.insert(END, vol + '\n')
vol_label.pack()    
text.pack()   
mainloop()



# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#   For one file (rev 1)
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# filename = r'C:\Users\Bash\Downloads\rail\raillooptest.pdf'
# pdfFileObj = open(filename,'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# num_pages = pdfReader.numPages
# count = 0
# text = ""
#
# while count < num_pages:
#     pageObj = pdfReader.getPage(count)
#     count += 1
#     text += pageObj.extractText()
#
# if text != "":
#                 text = text
# else:
#     text = textract.process(filename, method='tesseract', language='eng')
#
# cars = re.findall('([A-Z]{4}\s?[0-9]{4,6})',text)
#
# for car in cars:
#     print(car)

# tokens = word_tokenize(text)
# punctuations = ['(',')',';',':','[',']',',']
# stop_words = stopwords.words('english')
# keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
# print(len(keywords))
# for kw in keywords:
#     print(kw)
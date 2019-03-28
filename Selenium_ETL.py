# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:05:34 2018

@author: Fbasham
"""
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.select import Select
import Beau_Transflo


while True:
   
    try:

        #  Delete files in the directory so we can download new files without errors
        dirname = 'H:\FBasham\Daily Downloads\Beauharnois\TMS'
        filenames = os.listdir(dirname)
        filepaths = [os.path.join(dirname, filename) for filename in filenames]
        files = [f for f in filepaths if not os.path.isdir(f)]
        for fls in files:
                os.remove(fls)


        #  Begin session and start process to download
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', 'H:\FBasham\Daily Downloads\Beauharnois\TMS')
        profile.set_preference("browser.download.panel.shown", False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk',"application/octet-stream,application/zip, application/forced-download, text/plain, text/anytext, application/excel, application/csv, text/csv, application/vnd.csv, application/x-csv, text/comma-separated-values, application/vnd.ms-excel, application/csv, text/comma-separated-values, text/x-comma-separated-values, text/tab-separated-values")
                               
                               
        binary = FirefoxBinary(r'C:\Users\Fbasham\AppData\Local\Mozilla Firefox\firefox.exe')
        driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)
        driver.get("http://beauharnois.nglsupply.com/mainpage.htm?lWebIdx=32588&")
        
        driver.find_element_by_name("sWebNam").send_keys("user")
        driver.find_element_by_name("sWebPwd").send_keys("password")
        driver.find_element_by_name("Login").click()
        
        driver.find_element_by_xpath("//a[contains(@href,'reptpage')]").click()
        
        s1 = Select(driver.find_element_by_name("sRepGrp"))
        s1.select_by_visible_text('Detail Report')
        
        s2 = Select(driver.find_element_by_name("iRepNum"))
        s2.select_by_visible_text('Contract Detail Report')
        
        
        driver.find_element_by_name("EXPT").click()
        
        
        s3 = Select(driver.find_element_by_name("iRepExp"))
        s3.select_by_value('4')
        
        
        driver.find_element_by_name("dStrTim").clear()
        driver.find_element_by_name("dStrTim").send_keys("10/01/2018 12:00:00 AM")
        driver.find_element_by_name("OKXX").click()
        
        #  Ensure driver can locate the save button
        time.sleep(10)
        driver.find_element_by_xpath("//a[contains(@href,'zfbasham')]").click()
        
        
        #  Wait 10 seconds to close driver
        time.sleep(15)
        driver.close()
        
        break
        
    except Exception as e:
        print("something went wrong: " + repr(e))
        driver.close()          
        
        

#  Rename and move TMS report to OneDrive
old_file = os.path.join("H:\FBasham\Daily Downloads\Beauharnois\TMS", "zfbasham.csv")
new_file = os.path.join(r"H:\FBasham\Daily Downloads\Beauharnois\TMS", "Beauharnois Inventory Report.csv")
os.rename(old_file, new_file)
shutil.move(new_file,r"C:\Users\Fbasham\NGL Supply Co. Ltd\Beauharnois - Documents\TMS Reports\Beauharnois Inventory Report.csv")


#  Copy, rename, and move Geometrix Trace Dump to OneDrive
shutil.copy(r"H:\Logistics\Trace\Geometrix Logistics Trace\Geometrix Trace Dump.xlsx", r"H:\FBasham\Daily Downloads\Beauharnois\Geometrix Trace.xlsx")
shutil.move(r"H:\FBasham\Daily Downloads\Beauharnois\Geometrix Trace.xlsx", r"C:\Users\Fbasham\NGL Supply Co. Ltd\Beauharnois - Documents\Geo Trace\Geometrix Trace Dump.xlsx")

#  Copy, rename, and move E1 Rail Receipt Report to OneDrive
shutil.copy(r"P:\E1Report\FB Reports\FB - Beauharnois Rail Receipts.csv", r"H:\FBasham\Daily Downloads\Beauharnois\Beauharnois Rail Receipts.csv")
shutil.move(r"H:\FBasham\Daily Downloads\Beauharnois\Beauharnois Rail Receipts.csv", r"C:\Users\Fbasham\NGL Supply Co. Ltd\Beauharnois - Documents\E1 Reports\Beauharnois Rail Receipts.csv")


#  Copy, rename, and move Working copy of inventory report to backup folder to OneDrive
shutil.copy(r"C:\Users\Fbasham\NGL Supply Co. Ltd\Beauharnois - Documents\Inventory\Beauharnois Inventory Sheet.xlsx", r"H:\FBasham\Beauharnois Backup\backup.xlsx")
shutil.copy(r"H:\FBasham\Beauharnois Backup\backup.xlsx", r"C:\Users\Fbasham\NGL Supply Co. Ltd\Beauharnois - Documents\Inventory\Backups\backup.xlsx")

#  Execute the Transflo module to get current offload report at Beauharnois for this month
Beau_Transflo.main()

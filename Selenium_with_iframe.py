# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 15:31:07 2019

@author: Fbasham
"""

import glob
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import datetime
from datetime import timedelta, date

#####  Today's date
month = datetime.datetime.today().strftime('%Y.%m')
start_of_month = datetime.datetime.today().strftime('%Y-%m')
today = datetime.datetime.today().strftime('%Y-%m-%d')

##### End of month logic so when new month rolls over, date keys are from prior month end
if today[-2:] == '01':
    today = str(date.today() - timedelta(1))
    start_of_month = (datetime.datetime.today() - timedelta(1)).strftime('%Y-%m')
    

####  File name which grabs based on Today's date (month and year)
inventory_file = r"H:\TDunlop\Terminals\North Grafton\\" + month + " - North Grafton Inventory.xlsx"

while True:
   
    try:
        
        ### Delete all files in download directory
        files = glob.glob(r'H:\FBasham\Daily Downloads\Grafton\*')
        for f in files:
            os.remove(f)
        
        #  Begin session and start process to download
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', 'H:\FBasham\Daily Downloads\Grafton')
        profile.set_preference("browser.download.panel.shown", False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "application/vnd.ms-excel")
        
        ####  Must have to work:
        binary = FirefoxBinary(r'C:\Users\Fbasham\AppData\Local\Mozilla Firefox\firefox.exe')
        driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)
        driver.get("http://graftonuptonrr.gvmintegration.com")
        
        
        ####  Lets Selenium work in the frame and login
        frame = driver.find_element_by_xpath('//frame[@name="GVMTASweb"]')
        driver.switch_to.frame(frame)
        time.sleep(1)
        driver.find_element_by_name("sUsrNam").send_keys("user")
        driver.find_element_by_name("sUsrPwd").send_keys("password")
        driver.find_element_by_xpath("//input[@class='stlbtn'][@type='submit']").click()
        
        
        ######   NGL Truck Load
        driver.find_element_by_xpath("//a[contains(@href,'reports')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//tr/td[contains(text(), 'Loading Report')]").click()
        driver.find_element_by_name("dStrTim").clear()
        driver.find_element_by_name("dStrTim").send_keys(start_of_month + '-01')
        driver.find_element_by_name("dEndTim").clear()
        driver.find_element_by_name("dEndTim").send_keys(today)
        driver.find_element_by_xpath("//select[@class='stlcbo'][@name='sParSup']").click()
        driver.find_element_by_xpath("//a[@class='stlbtn'][@name='EXC']").click()
        time.sleep(5)
        shutil.copy(r"H:\FBasham\Daily Downloads\Grafton\Loading", r"H:\FBasham\Daily Downloads\Grafton\Grafton NGL Trucks.xls")
        time.sleep(2)
        os.remove(r"H:\FBasham\Daily Downloads\Grafton\Loading")
        
        
        ######   NGL Railcar Unload
        driver.find_element_by_xpath("//a[contains(@href,'reports')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//tr/td[contains(text(), 'Railcar Unload Report')]").click()
        driver.find_element_by_name("dStrTim").clear()
        driver.find_element_by_name("dStrTim").send_keys(start_of_month + '-01')
        driver.find_element_by_name("dEndTim").clear()
        driver.find_element_by_name("dEndTim").send_keys(today)
        driver.find_element_by_xpath("//select[@class='stlcbo'][@name='sParSup']").click()
        driver.find_element_by_xpath("//a[@class='stlbtn'][@name='EXC']").click()
        time.sleep(5)
        shutil.copy(r"H:\FBasham\Daily Downloads\Grafton\Railcar", r"H:\FBasham\Daily Downloads\Grafton\Grafton NGL Rail.xls")
        os.remove(r"H:\FBasham\Daily Downloads\Grafton\Railcar")
        time.sleep(2)
        
        #####  Logout and login to Spicer
        driver.find_element_by_class_name("logout").click()
        driver.find_element_by_name("sUsrNam").send_keys("jholstein")
        driver.find_element_by_name("sUsrPwd").send_keys("whaler24")
        driver.find_element_by_xpath("//input[@class='stlbtn'][@type='submit']").click()
        
        
        ######   Spicer Truck Load
        driver.find_element_by_xpath("//a[contains(@href,'reports')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//tr/td[contains(text(), 'Loading Report')]").click()
        driver.find_element_by_name("dStrTim").clear()
        driver.find_element_by_name("dStrTim").send_keys(start_of_month + '-01')
        date_today = datetime.datetime.today().strftime(today)
        driver.find_element_by_name("dEndTim").clear()
        driver.find_element_by_name("dEndTim").send_keys(date_today)
        driver.find_element_by_xpath("//select[@class='stlcbo'][@name='sParSup']").click()
        driver.find_element_by_xpath("//a[@class='stlbtn'][@name='EXC']").click()
        time.sleep(5)
        shutil.copy(r"H:\FBasham\Daily Downloads\Grafton\Loading", r"H:\FBasham\Daily Downloads\Grafton\Grafton Spicer Trucks.xls")
        time.sleep(2)
        os.remove(r"H:\FBasham\Daily Downloads\Grafton\Loading")
        
        
        ######   Spicer Railcar Unload
        driver.find_element_by_xpath("//a[contains(@href,'reports')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//tr/td[contains(text(), 'Railcar Unload Report')]").click()
        driver.find_element_by_name("dStrTim").clear()
        driver.find_element_by_name("dStrTim").send_keys(start_of_month + '-01')
        date_today = datetime.datetime.today().strftime(today)
        driver.find_element_by_name("dEndTim").clear()
        driver.find_element_by_name("dEndTim").send_keys(date_today)
        driver.find_element_by_xpath("//select[@class='stlcbo'][@name='sParSup']").click()
        driver.find_element_by_xpath("//a[@class='stlbtn'][@name='EXC']").click()
        time.sleep(5)

        shutil.copy(r"H:\FBasham\Daily Downloads\Grafton\Railcar", r"H:\FBasham\Daily Downloads\Grafton\Grafton Spicer Rail.xls")
        time.sleep(1)
        os.remove(r"H:\FBasham\Daily Downloads\Grafton\Railcar")
        
        time.sleep(3)
        driver.close()              
        break
        
    except Exception as e:
        print("something went wrong: " + repr(e))
        driver.close()
        


####  Open the North Grafton Inventory File (Power Query should refresh tables)
os.startfile(r"H:\FBasham\Daily Downloads\Grafton\Grafton NGL Trucks.xls")
os.startfile(r"H:\FBasham\Daily Downloads\Grafton\Grafton NGL Rail.xls")
os.startfile(r"H:\FBasham\Daily Downloads\Grafton\Grafton Spicer Trucks.xls")
os.startfile(r"H:\FBasham\Daily Downloads\Grafton\Grafton Spicer Rail.xls")
os.startfile(r"P:\E1Report\FB Reports\Grafton E1 Transaction Detail by Origin Report.csv")
os.startfile(inventory_file)

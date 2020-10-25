# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 13:07:45 2020

@author: elabo

For initial running, make sure to create auth/upass.txt with username, password only 


"""

from selenium import webdriver
import pandas as pd
import time

url = 'https://online.erieri.com/Account/Login'
ar_url = 'https://online.erieri.com/SA/AdvancedReports/'


def eri_login(url):
    f=pd.read_csv('auth/upass.txt', sep=',', header=None, index_col=None)
    usr = f.iloc[0][0].strip()
    pword = f.iloc[0][1].strip()

    driver = webdriver.Chrome('driver/chromedriver.exe')
    driver.get(url)
    email_box = f_xpath(driver, '//*[@id="UserName"]')
    email_box.send_keys(usr)
    pass_box = f_xpath(driver, '//*[@id="Password"]')
    pass_box.send_keys(pword)
    
    f_xpath(driver, '//*[@id="LoginButton"]').click()
    return(driver)


def f_xpath(driver, xpath):
    loc = driver.find_element_by_xpath(xpath)
    return(loc)

def get_advanced_report(url, ar_url):

    driver = eri_login(url)
    driver.get(ar_url)
    time.sleep(3)
    f_xpath(driver, '//*[@id="Toolbar #btnExcelExport"]/i').click()
    time.sleep(3)
    f_xpath(driver, '//*[@id="btnOK_AdvancedReportsToExcelModal1"]').click()


get_advanced_report(url, ar_url)

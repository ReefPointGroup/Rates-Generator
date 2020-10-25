# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 13:07:45 2020

@author: elabo

For initial running, make sure to create auth/upass.txt with username, password only 


"""

from selenium import webdriver
import pandas as pd
import time, shutil, os

url = 'https://online.erieri.com/Account/Login'
ar_url = 'https://online.erieri.com/SA/AdvancedReports/'

if os.path.exists('auth/upass.txt'):
    with open('auth/upass.txt', 'r') as inf:
        upass = eval(inf.read())
else:
    uname = input('Please enter ERI Email:')
    pword = input('Please enter ERI password:')
    upass = {'username': uname, 
             'password': pword}
    f = open('auth/upass.txt', 'w')
    f.write(str(upass))
    f.close()


#Lazy find_element_by_xpath
def f_xpath(driver, xpath):
    loc = driver.find_element_by_xpath(xpath)
    return(loc)


#Reads the upass file created, starts driver, logs in 
def eri_login(url, upass):

    usr = upass['username']
    pword = upass['password']

    driver = webdriver.Chrome('driver/chromedriver.exe')
    driver.get(url)
    email_box = f_xpath(driver, '//*[@id="UserName"]')
    email_box.send_keys(usr)
    pass_box = f_xpath(driver, '//*[@id="Password"]')
    pass_box.send_keys(pword)
    
    f_xpath(driver, '//*[@id="LoginButton"]').click()
    return(driver)



#downoads advanced report for saved job titles
def get_advanced_report(url, ar_url, upass):

    driver = eri_login(url, upass)
    driver.get(ar_url)
    time.sleep(3)
    f_xpath(driver, '//*[@id="Toolbar #btnExcelExport"]/i').click()
    time.sleep(3)
    f_xpath(driver, '//*[@id="btnOK_AdvancedReportsToExcelModal1"]').click()
    time.sleep(2)
    driver.close()


def move_from_downloads(fname):
    dl_fold = os.path.join(os.path.expanduser('~'), 'downloads')
    fold_list = [x for x in os.listdir(dl_fold) if fname in x]
    max_mtime = 0 
    for file in fold_list:
        temp_path = os.path.join(dl_fold, file)
        mtime = os.stat(temp_path).st_mtime
        if mtime > max_mtime:
            max_mtime = mtime
            max_file = file
    
    source = os.path.join(dl_fold, max_file)
    dest = 'data/eri/raw/'
    
    if not os.path.exists(dest):
        os.makedirs(dest)
      

    dest_file = os.path.join(dest, fname+'.xlsx')
    
    if os.path.exists(dest_file):
        os.remove(dest_file)
    
    shutil.move(source, dest)
    os.rename(os.path.join(dest, max_file), dest_file)


def wrangle_eri():
    
    df = pd.read_excel('data/eri/raw/AdvancedJobReport.xlsx', 'Advanced Job Report', skiprows=7, usecols = 'A:L')
    
    
    
    eri_loc = 'data/eri/processed/'
    #saving space for wrangling
    if not os.path.exists(eri_loc):
        os.makedirs(eri_loc)
        
    df.to_csv('data/eri/processed/ERI_Rates.csv')


get_advanced_report(url, ar_url, upass)
move_from_downloads('AdvancedJobReport')
wrangle_eri()

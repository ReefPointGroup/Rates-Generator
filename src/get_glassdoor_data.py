# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:15:54 2020

@author: elabo
"""

from selenium import webdriver
import pandas as pd
import time, shutil, os

if os.path.exists('auth/gd_upass.txt'):
    with open('auth/gd_upass.txt', 'r') as inf:
        upass = eval(inf.read())
else:
    uname = input('Please enter Glassdoor Email:')
    pword = input('Please enter Glassdoor password:')
    upass = {'username': uname, 
             'password': pword}
    f = open('auth/gd_upass.txt', 'w')
    f.write(str(upass))
    f.close()


url = 'https://www.glassdoor.com/Salaries/index.htm'
job_list = ['Senior Data Architect', 
            'Data Architect', 
            'Senior Solutions Architect', 
            'Solutions Architect', 
            'Program Manager', 
            'Project Manager', 
            'Senior Database Manager', 
            'Senior Database Administrator', 
            'Database Manager', 
            'Database Administrator', 
            'Senior Systems Engineer', 
            'Senior System Integrator', 
            'Systems Engineer', 
            'Systems Integrator', 
            'Data Engineer', 
            'Data Science Consultant', 
            'Senior Data Scientist', 
            'Data Scientist', 
            'Subject Matter Expert 1', 
            'Subject Matter Expert 2', 
            'Subject Matter Expert 3']

#Lazy find_element_by_xpath
def f_xpath(driver, xpath):
    loc = driver.find_element_by_xpath(xpath)
    return(loc)

def gd_signin (driver, upass):
    driver.get('glassdoor.com/index.htm')
    f_xpath(driver, '//*[@id="TopNav"]/nav/div/div/div[4]/div[1]/a').click()
    f_xpath(driver, '//*[@id="userEmail"]').send_keys(upass['username'])
    f_xpath(driver, '//*[@id="userPassword"]').send_keys(upass['password'])
    f_xpath(driver, '//*[@id="LoginModal"]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/form/div[3]/div[1]/button').click()


driver = webdriver.Chrome('driver/chromedriver.exe')
driver.get(url)

job_loc = 'Washington, DC'

job_data = {}

for title in job_list:
    driver.get(url)
    f_xpath(driver, '//*[@id="KeywordSearch"]').send_keys(title)
    f_xpath(driver, '//*[@id="LocationSearch"]').clear()
    f_xpath(driver, '//*[@id="LocationSearch"]').send_keys(job_loc)
    f_xpath(driver, '//*[@id="HeroSearchButton"]').click()
    low = f_xpath(driver, '//*[@id="OccMedianChart"]/div[1]/div[2]/div/div[2]/div[1]').text
    avg = f_xpath(driver, '//*[@id="OccMedianChart"]/div[1]/div[2]/div/div[2]/div[4]').text
    high = f_xpath(driver, '//*[@id="OccMedianChart"]/div[1]/div[2]/div/div[2]/div[8]').text
    
    job_data[title] = {'low': low, 
                       'avg': avg, 
                       'high': high}
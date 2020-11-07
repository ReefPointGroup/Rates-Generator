# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:15:54 2020

@author: elabo
"""
def pull_gd_data():
    from selenium import webdriver
    import pandas as pd
    import time, os
    from datetime import datetime
    
    
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
                'Data Scientist']
    
    #Lazy find_element_by_xpath
    def f_xpath(driver, xpath):
        loc = driver.find_element_by_xpath(xpath)
        return(loc)
    
    def gd_signin (driver, upass):
        driver.get('https://www.glassdoor.com/index.htm')
        time.sleep(1)
        f_xpath(driver, '//*[@id="TopNav"]/nav/div/div/div[4]/div[1]/a').click()
        f_xpath(driver, '//*[@id="userEmail"]').send_keys(upass['username'])
        f_xpath(driver, '//*[@id="userPassword"]').send_keys(upass['password'])
        f_xpath(driver, '//*[@id="LoginModal"]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/form/div[3]/div[1]/button').click()
    
    
    driver = webdriver.Chrome('driver/chromedriver.exe')
    driver.implicitly_wait(10)
    gd_signin(driver, upass)
    time.sleep(2)
    driver.get(url)
    
    job_loc = 'Washington, DC'
    
    job_data = {}
    
    for title in job_list:
        driver.get(url)
        f_xpath(driver, '//*[@id="KeywordSearch"]').send_keys(title)
        f_xpath(driver, '//*[@id="LocationSearch"]').clear()
        f_xpath(driver, '//*[@id="LocationSearch"]').send_keys(job_loc)
        f_xpath(driver, '//*[@id="HeroSearchButton"]').click()
        time.sleep(3)
        
        price_list = driver.find_elements_by_class_name('common__HistogramStyle__labelWrapper')
        tier_dict = {}
    
        for tier in price_list:
    
            level = tier.text.split()
    
            tier_dict[level[1]] = level[0]
            
        job_data[title] = tier_dict
    
    driver.close()
    
    gd_data = pd.DataFrame.from_dict(job_data, orient='index')
    
    
    ##Processing


    def processing(col):
    
        col = col.str.replace(r'$', '')
        col = col.str.replace(r'K', '')
        col = col.astype(float)
        col = col.fillna(col.mean(axis=0))
        col = col*1000
        return(col)
    
    col_names = ['Low', 'Average', 'High']
    
    
    gd_data.loc[:, col_names] = gd_data.loc[:, col_names].apply(lambda x:processing(x), axis=1)
    
    gd_data['Pull_Date'] = datetime.today().strftime('%Y-%m-%d')
    gd_data = gd_data.reset_index()
    gd_data.columns = ['LCAT', 'Low', 'Average', 'High', 'Pull_Date']
    gd_data['25'] = (gd_data.Low+gd_data.Average)/2
    gd_data['75'] = (gd_data.Average+gd_data.High)/2
    gd_data.to_csv('data/Glass_Door/raw/GD_Rates.csv')

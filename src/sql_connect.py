# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:52:06 2020

@author: jleitzinger
"""
import pyodbc
import os

def sql_connection():
    
    if os.path.exists('auth/sql_cred.txt'):
        with open('auth/sql_cred.txt', 'r') as inf:
            cnxn_str = inf.read()
    else:
        cnxn_str = input('Please copy and paste SQL Connection String')
        f = open('auth/sql_cred.txt', 'w')
        f.write(str(cnxn_str))
        f.close()
    
    
    #make sure to update driver
    try:
        cnxn = pyodbc.connect(cnxn_str)
    except:
        driver = input('Your Driver is incorrect. Please input driver information:\n')
        cnxn_str = 'Driver='+driver+cnxn_str[cnxn_str.find(';'):]
        try: 
            cnxn = pyodbc.connect(cnxn_str)
            f = open('auth/sql_cred.txt', 'w')
            f.write(str(cnxn_str))
            f.close()
        except:
            print("Check your credentials and try again later")

    return(cnxn)
#cnxn.close()


               
               


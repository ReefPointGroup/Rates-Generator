# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:52:06 2020

@author: jleitzinger
"""
import pyodbc
import pandas as pd


server = '' 
database = 'ratecard' 
username = 'rc' 
password = '' 
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server='+server+';Database='+database+';Uid='+username+';Pwd='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()
cnxn.close()



#test query 
cursor.execute("Select @@version;")

                                     
cursor.execute('''
                DROP TABLE dbo.TEST                 
               ;
               ''')
               
cursor.execute('''
               select * from INFORMATION_SCHEMA.TABLES;''').fetchall()
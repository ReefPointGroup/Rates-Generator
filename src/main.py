# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 10:23:52 2020

@author: jleitzinger
"""
import src.get_eri_data as eri
import src.get_glassdoor_data as gd
import src.sql_commit as commit

eri_get = input('Get eri data? (Y/N)')
gd_get = input('Get Glass Door data? (Y/N)')

if eri_get == 'Y':
    eri.get_eri_data()

if gd_get == 'Y':
    gd.get_glassdoor_data()
    
commit.commit_data()

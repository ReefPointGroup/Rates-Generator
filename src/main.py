# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 10:23:52 2020

@author: jleitzinger
"""
import pandas as pd
import src.get_eri_data as eri
import src.get_glassdoor_data as gd
import src.sql_commit as commit
import src.comb_and_proc as comb

eri_get = input('Get eri data? (Y/N)')
gd_get = input('Get Glass Door data? (Y/N)')

# Pull Data from ERI and Glassdoor -------------------------------------------

if eri_get == 'Y':
    eri.get_eri_data()

if gd_get == 'Y':
    try:
        gd.pull_gd_data()
    except:
        gd.pull_gd_data()

# Combine and Proccess the data in a single table ----------------------------
# src1 - data/Glass_Door/raw/GD_Rates.csv
# src2 - data/eri/processed/ERI_Rates.csv

gd_df_raw = pd.read_csv('data/Glass_Door/raw/GD_Rates.csv')
eri_df_raw = pd.read_csv('data/eri/processed/ERI_Rates.csv')

comb_df = comb.bring_it_together(eri_df_raw, gd_df_raw)


# Commit data from local to the SQL server -----------------------------------
commit.commit_data(eri_df_raw, gd_df_raw, comb_df)

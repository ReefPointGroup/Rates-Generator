# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 11:04:34 2020

@author: jleitzinger
"""
import pandas as pd
import numpy as np
import os

pd.set_option('display.max_columns', None)

gd_df_raw = pd.read_csv('data/Glass_Door/raw/GD_Rates.csv')
eri_df_raw = pd.read_csv('data/eri/processed/ERI_Rates.csv')


def gd_processing(df):
    df = df.rename(columns={'Low': '10_Perc', 
                            '25': '25_Perc', 
                            'Average': '50_Perc', 
                            '75': '75_Perc', 
                            'High': '90_Perc'})
    df['Source'] = 'Glass_Door'
    del df['Unnamed: 0']
    return(df)
    
    
    
def eri_processing(df):
    df = df.rename(columns={'ERI Job Title': 'LCAT', 
                            '10th Percentile': '10_Perc',
                            '25th Percentile': '25_Perc', 
                            'ERI Survey Mean': '50_Perc' ,
                            '75th Percentile': '75_Perc', 
                            '90th Percentile': '90_Perc'})
    df['LCAT'][df['Level']==8] = 'Senior '+df['LCAT']
    df['LCAT'][df['Level']==15] = 'Principal '+df['LCAT']
    df['Source'] = 'ERI'
    del df['Geographic Area']
    del df['Values In']
    del df['Unnamed: 0']


    return(df)

def comb_direct_rate(df_nums):
    df_nums = df_nums/1920

def bring_it_together(eri_df, gd_df):
    
    eri_df = eri_processing(eri_df_raw)
    gd_df = gd_processing(gd_df_raw)
    
    lcat_table = eri_df[['eDOT', 'SOC', 'LCAT', 'Level']]
    
    gd_df = pd.merge(gd_df, lcat_table, how='inner', on='LCAT')
    
    combined = gd_df.append(eri_df)
    comb_dr = combined.select_dtypes(np.float64).apply(lambda x: x/1920)
    comb_dr.columns = comb_dr.columns+'_dr'
    test = pd.concat([combined, comb_dr], axis=1)
    
    combined.select_dtypes(np.float64)
    
    return(combined)










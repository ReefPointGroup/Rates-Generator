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


def bring_it_together(eri_df, gd_df):
    
    eri_df = eri_processing(eri_df_raw)
    gd_df = gd_processing(gd_df_raw)
    
    lcat_table = eri_df[['eDOT', 'SOC', 'LCAT', 'Level']]
    
    #Get the job numbers between eri and gd
    gd_df = pd.merge(gd_df, lcat_table, how='inner', on='LCAT')
    
    combined = gd_df.append(eri_df)
    common_col = combined.select_dtypes(np.float64).columns
    
    #Direct Rates
    comb_dr = combined.select_dtypes(np.float64).apply(lambda x: x/1920)
    comb_dr.columns = common_col+'_dr'

    
    #Indirect Rates
    fringe = 0.34
    overhead = 0.25
    g_a = 0.146
    profit = 0.18
    
    comb_ir = comb_dr.apply(lambda x: x*(1+fringe)*(1+overhead)*(1+g_a))
    comb_ir.columns = common_col+'_ir'
    
    #Fully Burdened
    
    comb_fb = comb_ir.apply(lambda x: x*(1+profit))
    comb_fb.columns = common_col+'_fb'
    
    combined = pd.concat([combined, comb_dr, comb_ir, comb_fb], axis = 1)
    combined.reset_index(inplace=True, drop=True)
    
    combined = combined.melt(id_vars = ['LCAT', 'Pull_Date', 'Source', 'eDOT', 'SOC', 'Level'])
    combined['Percentile'] = combined['variable'].map(lambda x: x[0:2])
    combined['Rate Type'] = combined['variable'].map(lambda x: x[-2:])
    combined['Rate Type'] = combined['Rate Type'].str.replace('rc', 'Annual Salary')
    combined['Rate Type'] = combined['Rate Type'].str.replace('fb', 'Fully Burdened')
    combined['Rate Type'] = combined['Rate Type'].str.replace('dr', 'Direct Rate')
    combined['Rate Type'] = combined['Rate Type'].str.replace('ir', 'Indirect Rate')
    
    
    return(combined)










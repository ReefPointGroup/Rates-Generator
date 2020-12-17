# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 10:12:57 2020

@author: jleitzinger
"""
## Continue here next time to load up the combined stuff


def commit_data(eri_data, gd_data, comb_data):
    from src.sql_connect import sql_connection
    
    cnxn = sql_connection()
    cursor = cnxn.cursor()
    
    for index, row in gd_data.iterrows():
        cursor.execute("INSERT INTO Glassdoor_Rates (LCAT,Low,Average,High, Pull_Date, Perc_25, Perc_75) values(?,?,?,?,?,?,?)", row.LCAT, row.Low, row.Average, row.High, row.Pull_Date, row['25'], row['75'])
    cnxn.commit()
    
    for index, row in eri_data.iterrows():
        cursor.execute("INSERT INTO ERI_Rates (LCAT,Perc_10,Perc_25, Perc_50, Perc_75, Perc_90, eDot, SOC,Location , Pull_Date, Years_Experience) values(?,?,?,?,?,?,?,?,?,?,?)", \
                       row['ERI Job Title'],row['10th Percentile'],row['25th Percentile'],row['ERI Survey Mean'],row['75th Percentile'],row['90th Percentile'], \
                       row['eDOT'],row['SOC'],row['Geographic Area'],row['Pull_Date'], row['Level'])
    

    
    cnxn.commit()
    
    cnxn.close()

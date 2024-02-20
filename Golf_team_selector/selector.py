# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 17:24:54 2023

@author: eric_
"""

""" Inputs:
    --Name (str)
    --Gender (str, "F" or "M")
    --Handicap (float)
    --Host(s) (boolean)
"""
""" Critera:
    --Groups of 4 (or less but more than 2)
    --Total group handicap "close" between groups
    --Mix of genders
    --Not same groups every week
    --Mom and Dad not in same group
    --
 """   
""" Adjustments:
    --
"""
""" Output:
    --Name (str)
    --Gender (str, "F" or "M")
    --Handicap (float)
    --Host(s) (boolean)
    --Group number (int)
    --Group Handicap (float)
    
    titta på spelhandicap inte faktiskt handicap
    justera ner alla M över 28 till 28 och alla F över 36 till 36
    ta bort 5% av gruppens spelhandicap (4 spelare) eller 10% om 3 spelare
"""

import random
import pandas as pd
import datetime as dt

#golfers_database = pd.read_excel('golfers_database.xlsx')

def new_importer(file_name,desc=False,gb='S'):
    if file_name[-1] == 'v':
        df = pd.read_csv(file_name)
    else: df = pd.read_excel(file_name)
    if desc:
        print(df.groupby(gb).describe())
    return df

def group_creator(df,hc='Hju'):
    df.loc[(df['S'] == 'M')&(df[hc] > 28), hc] = 28
    df.loc[(df['S'] == 'F')&(df[hc] > 36), hc] = 36
    gr_num = int(len(df)/4)+1
    rest = len(df) % 4
    if rest == 1:
        last_gr = [3,3,3]
    elif rest == 2:
        last_gr = [4,3,3]
    elif rest == 3:
        last_gr = [4,4,3]
    else:
        last_gr = [4,4,4]
    gr_list = [4]*(gr_num-3)+last_gr
    
    gr_num_list = sum([[count]*num for count,num in enumerate(gr_list)],[])
    reduced_handicap = [0.95 if gr_num_list.count(x)>3 else 0.9 for x in gr_num_list]
    
    # This give unfairly high handicap req to last groups
    # gr_hp_sum_mean = sum(golfers_df['Handicap'])/gr_num
    gr_list_hp_sum = [(x/len(df))*sum(df[hc]) for x in gr_list]
    return gr_list,gr_num_list,gr_list_hp_sum,reduced_handicap

##Forcing Gender split??
# f_per_gr = len(golfers_df.loc[golfers_df['Gender']=='F'])/gr_num

## Host split

def randomiser(df,gr_list,gr_list_hp_sum,nm='Nombre',hc='Hju',limit=0.1):
    print(f'Limit used: {limit}')
    rand_df = df
    rand_df = rand_df.sample(frac=1)
    
    fin_gr_names = []
    
    for count,num in enumerate(gr_list):
        while True:
            rand_df = rand_df.sample(frac=1)
            gr_hp = sum(rand_df[hc][:num])
            if gr_hp >= gr_list_hp_sum[count]*(1-limit) and gr_hp <= gr_list_hp_sum[count]*(1+limit):
                fin_gr_names.append(rand_df[nm][:num])
                rand_df.drop(rand_df.index[:num], inplace=True)
                break
            if count+1 == len(gr_list) and (gr_hp <= gr_list_hp_sum[count]*(1-limit) or gr_hp >= gr_list_hp_sum[count]*(1+limit)):
                return randomiser(df,gr_list,gr_list_hp_sum,nm,hc,limit=limit)
    return fin_gr_names

def df_merger(gr_names,df,reduced_handicap,nm='Nombre',hc='Hju'):
    concat_df = pd.DataFrame(pd.concat(gr_names))
    merged_df = concat_df.merge(df, on=nm)
    merged_df['Host'] = ['idermark' in n.lower() for n in merged_df['Nombre']]
    merged_df['Group'] = gr_num_list
    merged_df['Group Handicap'] = merged_df.groupby(
                                          merged_df['Group'].ne(
                                          merged_df['Group'].shift())
                                          .cumsum())[hc].transform('sum')
    merged_df['Handicap Multiplier'] = reduced_handicap
    merged_df['Reduced Handicap'] = merged_df['Group Handicap']*merged_df['Handicap Multiplier']
    s_df = merged_df.groupby('Group').mean(numeric_only=True)
    mn_df = merged_df.groupby('Group').min(numeric_only=True)
    mx_df = merged_df.groupby('Group').max(numeric_only=True)
    g_df = merged_df.groupby(['Group', 'S']).size().unstack()
    stats_df = s_df[[hc,'Host','Group Handicap']].merge(g_df,on='Group')
    stats_df = stats_df.merge(mn_df[[hc]],on='Group')
    stats_df = stats_df.merge(mx_df[[hc]],on='Group')
    stats_df['HC_Range'] = stats_df.iloc[:,-1]-stats_df.iloc[:,-2]
    stats_df.columns = ['Avg Handicap','Host','Total Handicap','Females','Males',
                        'Lowest Handicap','Highest Handicap','Handicap Range']
    stats_df = stats_df[['Total Handicap', 'Avg Handicap','Females','Males', 'Host',
                        'Lowest Handicap','Highest Handicap','Handicap Range']]
    print(stats_df)
    return merged_df,stats_df

def exporter(golfers_df,stats_df):
    with pd.ExcelWriter(f'{dt.datetime.now().strftime("%Y-%m-%d")}_Golf_groups.xlsx') as writer:
        golfers_df.to_excel(writer, sheet_name="Golfers")  
        stats_df.to_excel(writer, sheet_name="Stats")

golfers_df = new_importer('SCRAMBLE 12.xlsx')#'Golfers.csv')
gr_list,gr_num_list,gr_list_hp_sum,reduced_handicap = group_creator(golfers_df)
fin_gr_names = randomiser(golfers_df,gr_list,gr_list_hp_sum,limit=random.randrange(3,10)/100)
fin_golfers_df,stats_df = df_merger(fin_gr_names,golfers_df,reduced_handicap)
#exporter(fin_golfers_df,stats_df)

#fin_golfers_df_test1 = fin_golfers_df[['Nombre','Group']]
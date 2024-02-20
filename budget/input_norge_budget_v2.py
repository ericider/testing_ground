# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 20:43:49 2022

@author: eric_
"""
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
import numpy as np

acc = pd.read_csv('OversiktKonti-01.01.2023-31.12.2023_kortkonto.csv',sep=";",decimal=',')

acc['Dato'] = pd.to_datetime(acc['Dato'],format='%d.%m.%Y')

for i in acc.index:
    if np.isnan(acc.at[i, 'Ut']):
        acc.at[i, 'Ut'] = acc.at[i, 'Inn']

all_cate = pd.DataFrame.from_dict({'KLARNA NORGE AS': 'Inc - Salary',
                                   'Overføring': 'Transfer',
                                    'Fjordkraft AS': 'Exp - Household',
                                    'Eric Axel Idermark': 'Transfer',
                                    'GJENSIDIGE FORSIKRING ASA': 'Exp - Household',
                                    'RUTERAPPEN': 'Exp - Transport',
                                    'Utleiemegleren Lysaker AS': 'Exp - Rent',
                                    'Just Eat.no': 'Exp - EatOut'},
                                     orient='index',columns=['Category'])

acc = acc.merge(all_cate,left_on='Beskrivelse', right_index=True,how='left')

cate_list = pd.DataFrame.from_dict({1:'Inc - Assistance',
                                     2:'Inc - Dividends',
                                     3:'Inc - Other',
                                     4:'Inc - Pension',
                                     5:'Inc - Repayment',
                                     6:'Inc - Salary',
                                     7:'Exp - EatOut',
                                     8:'Exp - Entertainment',
                                     9:'Exp - Grocery',
                                     10:'Exp - Health',
                                     11:'Exp - Household',
                                     12:'Exp - Other',
                                     13:'Exp - Rent',
                                     14:'Exp - Shopping',
                                     15:'Exp - Transport',
                                     16:'Savings',
                                     17:'Transfer'},
                                     orient='index',columns=['Category'])

for i in acc.index:
    if type(acc.at[i, 'Category']) != str:
        print(str(acc.at[i, 'Dato']) + ' ' + acc.at[i, 'Beskrivelse'] + ': ' + str(acc.at[i, 'Ut']))
        print(cate_list)
        choice = input('Choose Category: ')
        acc.at[i, 'Category'] = cate_list.at[int(choice), 'Category']
        
out_acc = acc[['Dato','Category','Beskrivelse','Ut']]

wb = load_workbook(filename = 'norge_budget_v2.xlsx')
ws = wb["Core"]
for r in dataframe_to_rows(out_acc, index=False, header=False):
    ws.append(r)
wb.save('norge_budget_v2.xlsx')


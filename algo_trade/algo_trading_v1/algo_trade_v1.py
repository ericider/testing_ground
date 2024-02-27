#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 21:58:10 2020

@author: ericidermark
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf

def plotting(date,price,buy,sell,sma30=0,sma100=0):
    plt.style.use('seaborn-whitegrid')
    plt.title('Stock Price Changes')
    plt.xlabel(f'Date: {str(min(date))[:10]} to {str(max(date))[:10]}')
    plt.ylabel('Stock Price')

    plt.plot(buy,'g^',label='Buy')
    plt.plot(sell,'rv',label='Sell')
    plt.plot(price,label='Adj Close',alpha=0.3)
    plt.plot(sma30,label='SMA30',alpha=0.3)
    plt.plot(sma100,label='SMA100',alpha=0.3)

    
    plt.legend(loc='upper left')
    plt.show()
    
    return

def read_stock(data):
    stock_df = pd.read_csv(data)
    # stock_df['Date']=pd.to_datetime(stock_df['Date'],format='%Y-%m-%d')
    return stock_df

def sma_avg(stock_df,close='Close',s_sma=30,l_sma=100):
    avg_df = pd.DataFrame()
    avg_df['Date'] = stock_df.index
    avg_df[f'SMA{s_sma}'] = stock_df[close].rolling(window = s_sma).mean().values
    avg_df[f'SMA{l_sma}'] = stock_df[close].rolling(window = l_sma).mean().values
    
    buy_dict = {}
    val_buy = []
    for i in range(1,len(avg_df)):
        if (avg_df[f'SMA{s_sma}'][i-1]<avg_df[f'SMA{l_sma}'][i-1])&(avg_df[f'SMA{s_sma}'][i]>avg_df[f'SMA{l_sma}'][i]):
            val_buy.append(stock_df[close][i])
            buy_dict[i] = [avg_df.index[i],stock_df[close][i]]
        else:
            val_buy.append(np.nan)
    val_buy = [np.nan]+val_buy
    
    sell_dict = {}
    val_sell = []
    for i in range(1,len(avg_df)):
        if (avg_df[f'SMA{s_sma}'][i-1]>avg_df[f'SMA{l_sma}'][i-1])&(avg_df[f'SMA{s_sma}'][i]<avg_df[f'SMA{l_sma}'][i]):
            val_sell.append(stock_df[close][i]) 
            sell_dict[i] = [avg_df.index[i],stock_df[close][i]]
        else:
            val_sell.append(np.nan)
    val_sell = [np.nan]+val_sell
    
    return avg_df,buy_dict,val_buy,sell_dict,val_sell


def calc_prof(buy_dict,sell_dict):
    tot_prof = 0
    if list(buy_dict.keys())[0]>list(sell_dict.keys())[0]:
        for i in range(len(buy_dict)-1):
            prof = (list(sell_dict.values())[i+1][1])-(list(buy_dict.values())[i][1])
            tot_prof = tot_prof + prof
    else:
        for i in range(len(buy_dict)):
            prof = (list(sell_dict.values())[i][1])-(list(buy_dict.values())[i][1])
            tot_prof = tot_prof + prof
    return tot_prof


# avg_df,buy_dict,val_buy,sell_dict,val_sell = sma_avg(hist)

# for j in [i for i in d_buy if i is not np.nan]:
#     print(avg_df['Date'][int(j)])

    



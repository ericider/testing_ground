#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:03:51 2020

@author: ericidermark
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas_datareader as pdr

tickers_symbols = ['SPY' ,'AAPL' ,'MSFT']

def down(tickers_symbols):
    data = pdr.DataReader(tickers_symbols,
                          data_source='yahoo',
                          start='2017-01-01',
                          end='2020-09-28')
    return data

def sma_2avg(data,tickers_symbols,s_sma=30,l_sma=100):
    sma_df = pd.DataFrame()
    for i in tickers_symbols:
        sma_df[f'{i}_Close'] = data[i]['Close']
        sma_df.set_index(data.index)
        
        sma_df[f'{i}_SMA{s_sma}'] = data[i]['Close'].rolling(window = s_sma).mean().values
        sma_df[f'{i}_SMA{l_sma}'] = data[i]['Close'].rolling(window = l_sma).mean().values
        buy = [sma_df[f'{i}_Close'][j] 
               if (sma_df[f'{i}_SMA{s_sma}'][j-1]<sma_df[f'{i}_SMA{l_sma}'][j-1])&(sma_df[f'{i}_SMA{s_sma}'][j]>sma_df[f'{i}_SMA{l_sma}'][j])
               else np.nan for j in range(1,len(sma_df))]
        buy = [np.nan]+buy
        sma_df[f'{i}_SMA_buy'] = buy
        
        sell = [sma_df[f'{i}_Close'][j] 
               if (sma_df[f'{i}_SMA{s_sma}'][j-1]>sma_df[f'{i}_SMA{l_sma}'][j-1])&(sma_df[f'{i}_SMA{s_sma}'][j]<sma_df[f'{i}_SMA{l_sma}'][j])
               else np.nan for j in range(1,len(sma_df))]
        sell = [np.nan]+sell
        sma_df[f'{i}_SMA_sell'] = sell
    return sma_df

def plot_2avg(df,stock,s_sma=30,l_sma=100):
    ax = plt.gca()
    df.plot(y=f'{stock}_Close',ax=ax,alpha=0.3)
    df.plot(y=f'{stock}_SMA{s_sma}',ax=ax,alpha=0.3)
    df.plot(y=f'{stock}_SMA{l_sma}',ax=ax,alpha=0.3)
    df.plot(style='^',color='g',y=f'{stock}_SMA_buy',ax=ax)
    df.plot(style='v',y=f'{stock}_SMA_sell',ax=ax)
    plt.show()
    return

# for i in tickers_symbols:
#     plot(sma_df,i)

# sma_df[sma_df['SPY_SMA_buy'].notnull()]







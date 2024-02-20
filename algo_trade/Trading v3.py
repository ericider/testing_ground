#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:03:51 2020

@author: ericidermark
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pandas_datareader import data as pdr
import yfinance as yf
import time

# tickers_symbols = ['NFLX' ,'AMZN' ,'FB']

def read_tickers():
    ticker_data = pd.read_csv('nasdaq_screener_1645200876376.csv')
    return ticker_data

def down(tickers_symbols):
    dw_st = time.time()
    print('DOwnloading...')
    # stock = yf.Ticker('NFLX')
    # data = stock.history(period='5y')
    # data = yf.download("NFLX",
    #                    start=(datetime.now()-timedelta(days=5*365)).strftime('%Y-%m-%d'),
    #                    end=datetime.now().strftime('%Y-%m-%d'))
    # data = pdr.get_data_yahoo(tickers_symbols,
    #                       start=(datetime.now()-timedelta(days=5*365)).strftime('%Y-%m-%d'),
    #                       end=datetime.now().strftime('%Y-%m-%d'))
    stock_source_data = pdr.DataReader(tickers_symbols,
                          data_source='yahoo',
                          start=(datetime.now()-timedelta(days=5*365)).strftime('%Y-%m-%d'),
                          end=datetime.now().strftime('%Y-%m-%d'))
    print(f'Download took: {round(time.time()-dw_st,1)} secs')
    return stock_source_data

def sma_2avg(data,tickers_symbols,s_sma=30,l_sma=100):
    for i in tickers_symbols:
        data[f'SMA{s_sma}',f'{i}'] = data['Adj Close'][i].rolling(window = s_sma).mean().values
        data[f'SMA{l_sma}',f'{i}'] = data['Adj Close'][i].rolling(window = l_sma).mean().values
        buy = [data['Adj Close'][i][j] 
               if (data[f'SMA{s_sma}',f'{i}'][j-1]<data[f'SMA{l_sma}',f'{i}'][j-1])&(data[f'SMA{s_sma}',f'{i}'][j]>data[f'SMA{l_sma}',f'{i}'][j])
               else np.nan for j in range(1,len(data))]
        buy = [np.nan]+buy
        data['SMA_buy',f'{i}'] = buy
        
        sell = [data['Adj Close'][i][j] 
               if (data[f'SMA{s_sma}',f'{i}'][j-1]>data[f'SMA{l_sma}',f'{i}'][j-1])&(data[f'SMA{s_sma}',f'{i}'][j]<data[f'SMA{l_sma}',f'{i}'][j])
               else np.nan for j in range(1,len(data))]
        sell = [np.nan]+sell
        data['SMA_sell',f'{i}'] = sell
    return data,s_sma,l_sma

def boll(data,tickers_symbols,sma=20):
    for i in tickers_symbols:
        boll_mean = data['Adj Close'][i].rolling(window = sma).mean().values
        boll_std = data['Adj Close'][i].rolling(window = sma).std().values
        data['Boll_Upper',f'{i}'] = boll_mean+2*boll_std
        data['Boll_Lower',f'{i}'] = boll_mean-2*boll_std
        buy = [data['Adj Close'][i][j]
               if data['Adj Close'][i][j]<data['Boll_Lower',f'{i}'][j]
               else np.nan for j in range(1,len(data))]
        buy = [np.nan]+buy
        data['Boll_buy',f'{i}'] = buy
        sell = [data['Adj Close'][i][j]
               if data['Adj Close'][i][j]>data['Boll_Upper',f'{i}'][j]
               else np.nan for j in range(1,len(data))]
        sell = [np.nan]+sell
        data['Boll_sell',f'{i}'] = sell
    return data

def plot_boll(df,stock):
    df2 = df.copy()
    df2.columns = df2.columns.map('_'.join)
    ax = plt.gca()
    df2.plot(y=f'Adj Close_{stock}',ax=ax)
    ax.fill_between(df2.index,df2[f'Boll_Upper_{stock}'],df2[f'Boll_Lower_{stock}'],alpha=0.3)
    df2.plot(style='^',color='g',y=f'Boll_buy_{stock}',ax=ax)
    df2.plot(style='v',y=f'Boll_sell_{stock}',ax=ax)
    plt.show()
    return

def plot_2avg(df,stock,s_sma=30,l_sma=100):
    df2 = df.copy()
    df2.columns = df2.columns.map('_'.join)
    ax = plt.gca()
    df2.plot(y=f'Adj Close_{stock}',ax=ax,alpha=0.3)
    df2.plot(y=f'SMA{s_sma}_{stock}',ax=ax,alpha=0.3)
    df2.plot(y=f'SMA{l_sma}_{stock}',ax=ax,alpha=0.3)
    df2.plot(style='^',color='g',y=f'SMA_buy_{stock}',ax=ax)
    df2.plot(style='v',y=f'SMA_sell_{stock}',ax=ax)
    plt.show()
    return

def slope(metric='SMA100',ticker='SPY',period=100):
    x=data.index
    x_seq = np.arange(x.size)
    y= list(data[metric][ticker])
    fit = np.polyfit(x_seq[-period:], y[-period:], 1)
    return fit

ticker_df = read_tickers()
t = ticker_df.loc[ticker_df['Market Cap']>100_000_000_000]
t_l = list(t['Symbol'])
stock_source_data=down(t_l)
data,s_sma,l_sma=sma_2avg(stock_source_data,t_l)
data = boll(data,t_l)

# for i in tickers_symbols:
#     plot_2avg(data[-100:],i)
#     plot_boll(data[-100:],i)




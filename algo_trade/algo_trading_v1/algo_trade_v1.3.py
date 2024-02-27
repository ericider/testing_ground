# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 20:21:19 2022

@author: eric_
"""

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pandas_datareader import data as pdr
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
import yfinance as yfin

def download_stock_data(tickers_symbols):
    yfin.pdr_override()
    dw_st = time.time()
    print('Downloading...')
    # stock_source_data = pdr.DataReader(tickers_symbols,
    #                       data_source='stooq',
    #                       start=(datetime.now()-timedelta(days=5*365)).strftime('%Y-%m-%d'),
    #                       end=datetime.now().strftime('%Y-%m-%d'))
    stock_source_data = pdr.get_data_yahoo(tickers_symbols, 
                                           start=(datetime.now()-timedelta(days=5*365)).strftime('%Y-%m-%d'),
                                           end=datetime.now().strftime('%Y-%m-%d'))
    print(f'Download took: {time.time()-dw_st:,.1f} secs')
    return stock_source_data

def df_reset(df):
    df = df.drop(df.iloc[:,6:],axis = 1)
    return df  

def simple_ma(stock_data,t,short=20,mid=50,long=200):
    stock_data[f'SMA{short}',f'{t}'] = stock_data['Adj Close'][t].rolling(window = short).mean().values
    stock_data[f'SMA{mid}',f'{t}'] = stock_data['Adj Close'][t].rolling(window = mid).mean().values
    stock_data[f'SMA{long}',f'{t}'] = stock_data['Adj Close'][t].rolling(window = long).mean().values
    return stock_data

def exponential_ma(stock_data,t,short=20,mid=50,long=200):
    stock_data[f'EMA{short}',f'{t}'] = stock_data['Adj Close'][t].ewm(span=short).mean()
    stock_data[f'EMA{mid}',f'{t}'] = stock_data['Adj Close'][t].ewm(span=mid).mean()
    stock_data[f'EMA{long}',f'{t}'] = stock_data['Adj Close'][t].ewm(span=long).mean()
    return stock_data

def bollinger_bands(stock_data,t,period=20,std=2):
    boll_mean = stock_data['Adj Close'][t].rolling(window = period).mean().values
    boll_std = stock_data['Adj Close'][t].rolling(window = period).std().values
    stock_data['BB_Upper',f'{t}'] = boll_mean+std*boll_std
    stock_data['BB_Lower',f'{t}'] = boll_mean-std*boll_std
    return stock_data

def macd(stock_data,t,sig=9,short=12,long=26):
    macd_l = (stock_data['Close'][t].ewm(span=short).mean() -
              stock_data['Close'][t].ewm(span=long).mean())
    signal = macd_l.ewm(span=sig).mean()
    con_div = macd_l - signal
    macd_sig = pd.concat([macd_l, signal], axis=1)
    macd_long = ((macd_sig.iloc[:,0]<0)&
                (macd_sig.iloc[:,0].shift(1)<macd_sig.iloc[:,1].shift(1))&
                (macd_sig.iloc[:,0]>macd_sig.iloc[:,1]))*1
    macd_short = ((macd_sig.iloc[:,0]>0)&
                (macd_sig.iloc[:,0].shift(1)>macd_sig.iloc[:,1].shift(1))&
                (macd_sig.iloc[:,0]<macd_sig.iloc[:,1]))*-1
    stock_data[f'MACD{short}_{long}',f'{t}'] = stock_data.index.map(macd_l)
    stock_data[f'MACD_signal{sig}',f'{t}'] = stock_data.index.map(signal)
    stock_data['MACD_con_div',f'{t}'] = stock_data.index.map(con_div)
    stock_data['MACD_long',f'{t}'] = stock_data.index.map(macd_long)
    stock_data['MACD_short',f'{t}'] = stock_data.index.map(macd_short)
    return stock_data

def rsi(stock_data,t,period=14,drift=1,scalar=100):
    stock_delta = stock_data['Close'][t].diff(drift)
    delta_pos = stock_delta.clip(lower=0)
    delta_neg = stock_delta.clip(upper=0).abs()
    pos_avg = delta_pos.ewm(alpha=(1/period)).mean()
    neg_avg = delta_neg.ewm(alpha=(1/period)).mean()
    rsi = scalar-(scalar/(1+(pos_avg/neg_avg)))
    stock_data[f'RSI{period}',f'{t}'] = stock_data.index.map(rsi)
    return stock_data

def trading_signal(stock_data,sel_ind='sebmr'):
    for t in stock_data.unstack().index.unique(level=1):#'Symbols'):
        if 's' in sel_ind:
            stock_sma = simple_ma(stock_data,t)
        if 'e' in sel_ind:
            stock_ema = exponential_ma(stock_data,t)
        if 'b' in sel_ind:
            stock_bb = bollinger_bands(stock_data,t)
        if 'm' in sel_ind:
            stock_macd = macd(stock_data,t)
        if 'r' in sel_ind:
            stock_rsi = rsi(stock_data,t)
    return stock_data_indicators

# symbols = get_nasdaq_symbols()
raw_stock_data = download_stock_data(['AAPL','GOOGL'])


        
    
# plt.figure()
# stock[:200].plot(y=['MACD12_26','MACD_signal9','MACD_con_div','MACD_long','MACD_short'])      
# stock[:200].plot(y=['Close'],secondary_y=True)

# stock[:200].plot(y=['Close','MACD12_26','MACD_signal9'],subplots=True, layout=(3,1))

# fig, ax = plt.subplots() 
# stock[:200].plot(y=['MACD12_26','MACD_signal9','MACD_con_div','MACD_long','MACD_short'], ax = ax)      
# stock[:200].plot(y=['Close'], ax = ax,secondary_y=True)

# fig,(ax1,ax2,ax3) = plt.subplots(3,1)
# # ax2.axhline(30, c='b')
# stock[:200].plot(y=['Close'],ax = ax1)
# stock[:200].plot(y=['RSI14'],ax = ax2,color='r')
# stock[:200].plot(y=['MACD12_26','MACD_signal9','MACD_con_div','MACD_long','MACD_short'],
#                  ax = ax3,legend=False)


        
        
        
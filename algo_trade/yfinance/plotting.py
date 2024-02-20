# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:08:20 2021

@author: eric_
"""

import pandas as pd
import mplfinance as mpf
import numpy as np

def read_yfinance_file(YFINANCE_FILE='a.csv'):
    data = pd.read_csv(YFINANCE_FILE)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date')
    data['Ticker'] = YFINANCE_FILE[:-4]
    return data

def plotting(data,t='candle',sma=(50,200),time='mx'):
    mc = mpf.make_marketcolors(up='g',down='r')
    s  = mpf.make_mpf_style(marketcolors=mc)
    if time=='mx':
        dta = data[:]
    else: dta = data[time[0]:time[1]]
    mpf.plot(dta,type=t,title=f'{data.iloc[1,-1]} Stock',
             mav=sma,volume=True,tight_layout=True,style=s)
    return

cine = read_yfinance_file('CINE.L.csv')
plotting(cine,sma=(20,50),time=['2020-06','2099-12'])

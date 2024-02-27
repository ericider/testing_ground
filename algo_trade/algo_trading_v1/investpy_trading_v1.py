# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:52:24 2022

@author: eric_
"""

# https://medium.com/geekculture/a-simple-way-to-download-financial-data-from-investing-com-in-python-8262271c804f
# https://github.com/alvarobartt/investpy

import investpy

df = investpy.get_stock_historical_data(stock='AAPL',
                                        country='United States',
                                        from_date='01/01/2010',
                                        to_date='01/01/2020')
print(df.head())
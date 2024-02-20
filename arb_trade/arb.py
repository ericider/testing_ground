# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 21:12:16 2021

@author: eric_
"""

import pandas as pd

##IMPORTING???
##Finding same match across websites?

tot_bet_amt = 100_000

odds = {'Unibet - Bet A':1.48,
        'WillHill - Bet A':1.36,
        'Unibet - Bet B':2.75,
        'WillHill - Bet B':3.25}

pr = [(1/i) for i in odds.values()]

bookie = [pr[0]+pr[2],pr[1]+pr[3]]

arb_opps = [pr[0]+pr[3],pr[1]+pr[2]]


if arb_opps[0]<1:
    arb_bet = [list(odds.values())[0],list(odds.values())[3]]
    bet_amt = [(pr[0]*tot_bet_amt)/arb_opps[0],(pr[3]*tot_bet_amt)/arb_opps[0]]
    arb_res = (tot_bet_amt/arb_opps[0])-tot_bet_amt
elif arb_opps[1]<1:
    arb_bet = [list(odds.values())[1],list(odds.values())[2]]
    bet_amt = [(pr[1]*tot_bet_amt)/arb_opps[1],(pr[2]*tot_bet_amt)/arb_opps[1]]
    arb_res = (tot_bet_amt/arb_opps[1])-tot_bet_amt

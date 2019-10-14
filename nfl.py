# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 15:57:11 2019

@author: u365296
"""
import pandas as pd

nfl = pd.read_csv('nfl.csv')

a = nfl[['Week','VisTm','HomeTm']]
a.columns = ['Week','Team','Opponent']
b = nfl[['Week','HomeTm','VisTm']] 
b.columns = ['Week','Team','Opponent']

nfl2 = pd.concat([ a , b ])

teams = list(nfl2.loc[nfl2.Week == 1, 'Team'])

elos = pd.read_csv('teams.csv')

nfl3 = nfl2.merge(elos,left_on='Team',right_on='team')
nfl4 = nfl3.merge(elos,left_on='Opponent',right_on='team')

nfl5 = nfl4.drop(['Team','Opponent'],axis=1)

nfl5['win_prob'] = 1 / ( 1 + 10 ** ((nfl5['elo_y'] - nfl5['elo_x']) / 400) )

for a in teams:
    nfl5[a] = 0
    nfl5.loc[nfl5.team_x == a, a] = 1

weeks = []
for a in range(1,18):
    temp_week = 'week_' + str(a)
    weeks.append(temp_week)
    nfl5[temp_week] = 0
    nfl5.loc[nfl5.Week == a, temp_week] = 1
    
nfl5['week_weight'] = 1.0 ** (nfl5['Week']-1)
nfl5['points'] = nfl5['win_prob'] * nfl5['week_weight']


nfl6 = nfl5.loc[(nfl5.Week > 0) & (nfl5.Week <= 10)]

import openopt as opt

items = []
for i in range(len(nfl6.index)):
     dct = {}
     for j in nfl6.columns:
          dct[j] = nfl6[j].iloc[i]
     items.append(dct)
     
     
constraints = lambda values: (
#only pick a team at most once
values['Green Bay Packers'] <= 1
,values['Los Angeles Rams'] <= 1
,values['Tennessee Titans'] <= 1
,values['Kansas City Chiefs'] <= 1
,values['Baltimore Ravens'] <= 1
,values['Atlanta Falcons'] <= 1
,values['Buffalo Bills'] <= 1
,values['Washington Redskins'] <= 1
,values['Indianapolis Colts'] <= 1
,values['Cincinnati Bengals'] <= 1
,values['Detroit Lions'] <= 1
,values['New York Giants'] <= 1
,values['San Francisco 49ers'] <= 1
,values['Pittsburgh Steelers'] <= 1
,values['Houston Texans'] <= 1
,values['Denver Broncos'] <= 1
,values['Chicago Bears'] <= 1
,values['Carolina Panthers'] <= 1
,values['Cleveland Browns'] <= 1
,values['Jacksonville Jaguars'] <= 1
,values['Miami Dolphins'] <= 1
,values['Minnesota Vikings'] <= 1
,values['New York Jets'] <= 1
,values['Philadelphia Eagles'] <= 1
,values['Los Angeles Chargers'] <= 1
,values['Seattle Seahawks'] <= 1
,values['Arizona Cardinals'] <= 1
,values['Dallas Cowboys'] <= 1
,values['Tampa Bay Buccaneers'] <= 1
,values['New England Patriots'] <= 1
,values['New Orleans Saints'] <= 1
,values['Oakland Raiders'] <= 1
#each week must have only one pick
,values['week_1'] == 1
,values['week_2'] == 1
,values['week_3'] == 1
,values['week_4'] == 1
,values['week_5'] == 1
,values['week_6'] == 1
,values['week_7'] == 1
,values['week_8'] == 1
,values['week_9'] == 1
,values['week_10'] == 1
#,values['week_11'] == 1
#,values['week_12'] == 1
#,values['week_13'] == 1
#,values['week_14'] == 1
#,values['week_15'] == 1
#,values['week_16'] == 1
#,values['week_17'] == 1
)

objective = 'points'
knapsack = opt.KSP(objective, items, goal = 'max', constraints = constraints)
solution = knapsack.solve('glpk', iprint = 0)
print(nfl6.iloc[solution.xf,:][['Week','team_x','win_prob','week_weight','points']].sort_values(['Week']))


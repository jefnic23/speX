import pandas as pd
import numpy as np
import timeit
from scipy.stats import pearsonr
from operator import itemgetter
import matplotlib.pyplot as plt
import seaborn as sns

spex = pd.read_csv('speX_data.csv', index_col='Name')
sheets = ['2018', '2019', '2020', '2019+2020']
writer = pd.ExcelWriter('spex_leaderboards.xlsx')
    
# df1 = spex[(spex['game_year'] == 2018) & (spex['IP'] >= 75.0)][['SIERA', 'TBF', 'BB', 'IBB', 'SO', 'k-bb/ip', 'csw', 'O-Swing%', 'Zone%', 'pCRA', 'fstrike', 'hev']]
# df2 = spex[(spex['game_year'] == 2019) & (spex['IP'] >= 75.0)][['SIERA', 'ERA', 'FIP', 'woba', 'xwoba']]
# df = pd.merge(df1, df2, on='Name')
sheet1 = spex[(spex['game_year'] == 2018) & (spex['IP'] >= 75.0)]
sheet2 = spex[(spex['game_year'] == 2019) & (spex['IP'] >= 75.0)]
sheet3 = spex[(spex['game_year'] == 2020) & (spex['IP'] >= 30.0)]
sheet4 = pd.merge(spex[(spex['game_year'] == 2019) & (spex['IP'] >= 75.0)], 
                  spex[(spex['game_year'] == 2020) & (spex['IP'] >= 30.0)], 
                  on='Name'
                  )
dfs = [sheet1, sheet2, sheet3, sheet4]

for i, sheet in enumerate(sheets):
    if i == 3:    
        dfs[i]['SO'] = dfs[i]['SO_x'] + dfs[i]['SO_y']
        dfs[i]['BB'] = dfs[i]['BB_x'] + dfs[i]['BB_y']
        dfs[i]['IBB'] = dfs[i]['IBB_x'] + dfs[i]['IBB_y']
        dfs[i]['TBF'] = dfs[i]['TBF_x'] + dfs[i]['TBF_y']
        dfs[i]['IP'] = dfs[i]['IP_x'] + dfs[i]['IP_y']
        dfs[i]['csw'] = (dfs[i]['csw_x'] + dfs[i]['csw_y']) / 2
        dfs[i]['pCRA'] = (dfs[i]['pCRA_x'] + dfs[i]['pCRA_y']) / 2
        dfs[i]['O-Swing%'] = (dfs[i]['O-Swing%_x'] + dfs[i]['O-Swing%_y']) / 2
        dfs[i]['Zone%'] = (dfs[i]['Zone%_x'] + dfs[i]['Zone%_y']) / 2
        
        dfs[i]['K-BB%'] = ((dfs[i]['SO'] / dfs[i]['TBF']) - ((dfs[i]['BB'] + dfs[i]['IBB']) / dfs[i]['TBF'])) * 100
        dfs[i]['csw'] = dfs[i]['csw'] * 100
        dfs[i]['pCRA'] = dfs[i]['pCRA']
        dfs[i]['O-Swing + Zone%'] = dfs[i]['O-Swing%'] + dfs[i]['Zone%']
        dfs[i]['spex'] = (11 * dfs[i]['K-BB%'] + 165 * (10 - dfs[i]['pCRA']) + 7 * dfs[i]['csw'] + dfs[i]['O-Swing + Zone%']) * 0.049
    else:
        dfs[i]['K-BB%'] = ((dfs[i]['SO'] / dfs[i]['TBF']) - ((dfs[i]['BB'] + dfs[i]['IBB']) / dfs[i]['TBF'])) * 100
        dfs[i]['csw'] = dfs[i]['csw'] * 100
        dfs[i]['pCRA'] = dfs[i]['pCRA']
        dfs[i]['O-Swing + Zone%'] = dfs[i]['O-Swing%'] + dfs[i]['Zone%']
        dfs[i]['spex'] = (11 * dfs[i]['K-BB%'] + 165 * (10 - dfs[i]['pCRA']) + 7 * dfs[i]['csw'] + dfs[i]['O-Swing + Zone%']) * 0.049
    
    spex_leaderboard = dfs[i][['spex', 'IP', 'pCRA', 'K-BB%', 'csw', 'O-Swing + Zone%']]
    spex_leaderboard.to_excel(writer, sheet)
    
writer.save()

# df['spex'] = (11 * df['K-BB%'] + 165 * df['pCRA'] + 7 * df['csw'] + df['O-Swing + Zone%']) * 0.0506
# print(df['spex'].max())

# X = df['spex']
# y = df['SIERA_y']

# corr, _ = pearsonr(X, y)
# fig, ax = plt.subplots()
# sns.regplot(X, y)
# plt.text(0.8125, 0.8875,
#           'r2: {:01.3f}'.format(corr**2),
#           bbox=dict(facecolor='none', edgecolor='black', boxstyle='round'), 
#           transform=ax.transAxes
#           )

# spex = []
# for i in range(1, 1500):
#     df['spex'] = 11 * df['K-BB%'] + 165 * df['pCRA'] + 7 * df['csw'] + df['O-Swing + Zone%']
#     spex.append((i, pearsonr(df['spex'], df['SIERA_y'])[0]**2))
    
# high = max(spex, key=itemgetter(1))[:]
# print(high)

# plt.plot(*zip(*spex))
# plt.show()


# BEST FORMULA
# df['spex'] = (64 * df['k-bb/ip'] + 86 * (10 - df['pCRA']) + 4 * df['csw'] + df['O-Swing + Zone%']) * 0.1043
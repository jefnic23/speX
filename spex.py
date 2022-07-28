import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

df1 = pd.read_csv('E:/Documents/Pitcher List/statcast_data/savant_2018.csv')
df2 = pd.read_csv('E:/Documents/Pitcher List/statcast_data/savant_2019.csv')
df3 = pd.read_csv('E:/Documents/Pitcher List/statcast_data/savant_2020.csv')
fstrike_map = {'foul': 1, 
                'called_strike': 1, 
                'swinging_strike_blocked': 1, 
                'swinging_strike': 1, 
                'foul_tip': 1, 
                'foul_bunt': 1, 
                'missed_bunt': 1, 
                'bunt_foul_tip': 1,
                'hit_into_play': 0,
                'hit_into_play_no_out': 0,
                'ball': 0,
                'hit_into_play_score': 0,
                'blocked_ball': 0,
                'hit_by_pitch': 0,
                'pitchout': 0
                }
barrels_map = {1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 1
                }
def savant_filter(frame):
    frame['fstrike'] = frame['description'].map(fstrike_map)
    frame['launch_speed_angle'] = frame['launch_speed_angle'].map(barrels_map)
    frame['hev'] = frame['launch_speed'] * np.cos(np.radians(frame['launch_angle']-25))
    frame['csw'] = np.where(frame['description'].isin(['swinging_strike',
                                                        'called_strike',
                                                        'swinging_strike_blocked',
                                                        'foul_tip',
                                                        'foul_bunt',
                                                        'missed_bunt',
                                                        'bunt_foul_tip'
                                                        ]
                                                      ), 1, 0
                            )
    fstrike = frame[frame['pitch_number'] == 1].groupby('player_name')['fstrike'].mean()
    data = frame.groupby('player_name').agg(csw=('csw', 'mean'),
                                            barrels=('launch_speed_angle', 'sum'),
                                            bbe=('bb_type', 'count'),
                                            woba=('woba_value', 'mean'),
                                            xwoba=('estimated_woba_using_speedangle', 'mean'),
                                            hev=('hev', 'mean')
                                            )
    return pd.concat([data, fstrike], axis=1).rename_axis('player_name')

df1 = savant_filter(df1)
df2 = savant_filter(df2)
df3 = savant_filter(df3)

fg1 = pd.read_csv('E:/Documents/Pitcher List/colab/carlos-marcano/FanGraphs Leaderboard_2018.csv')
fg2 = pd.read_csv('E:/Documents/Pitcher List/colab/carlos-marcano/FanGraphs Leaderboard_2019.csv')
fg3 = pd.read_csv('E:/Documents/Pitcher List/colab/carlos-marcano/FanGraphs Leaderboard_2020.csv')
fg1['game_year'] = 2018
fg2['game_year'] = 2019
fg3['game_year'] = 2020

def fg_filter(frame): 
    so = frame['SO'].values
    bb = frame['BB'].values
    ibb = frame['IBB'].values
    ip = frame['IP'].values
    frame['k-bb/ip'] = (so - (bb+ibb)) / ip
    col_list = frame.columns.to_list()
    frame[col_list] = frame[col_list].replace({'%': ''}, regex=True)
    nums = ['O-Swing%', 'Z-Swing%', 'Swing%', 'O-Contact%', 'Z-Contact%', 'Contact%', 'Zone%', 'SwStr%']
    frame[nums] = frame[nums].apply(pd.to_numeric)
    return frame

fg1 = fg_filter(fg1)
fg2 = fg_filter(fg2)
fg3 = fg_filter(fg3)

spex1 = pd.merge(fg1, df1, left_on='Name', right_on='player_name')
spex2 = pd.merge(fg2, df2, left_on='Name', right_on='player_name')
spex3 = pd.merge(fg3, df3, left_on='Name', right_on='player_name')
spex = pd.concat([spex1, spex2, spex3])

pk = (spex['SO'] + 10.66) / (spex['TBF'] + 10.66 + 37.53)
pbb = (spex['BB'] + spex['IBB'] + 9.58) / (spex['TBF'] + 9.58 + 116.2)
pbrl = (spex['barrels'] + 13.33) / (spex['bbe'] + 13.33 + 191.5)
spex['pCRA'] = -(8.89*pk) + (8.03*pbb) + (5.54*pbrl) + (106*(pbrl**2)) + 4.55
spex.to_csv('speX_data.csv', index=False)
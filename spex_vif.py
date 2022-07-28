import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.decomposition import PCA
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

# load and clean data
df = pd.read_csv('speX_data.csv', index_col='Name')
df = df[(df['game_year'] == 2018) & (df['IP'] >= 75.0)]
df['csw'] = df['csw'] * 100
df['z+o'] = df['Zone%'] + df['O-Swing%']

def decompose(df, features):
    x = df.loc[:, features].values
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x)
    principal_df = pd.DataFrame(data=principal_components, columns=['comp_1', 'comp_2'], index=df.index)
    df['comp_1'] = principal_df['comp_1']
    df['comp_2'] = principal_df['comp_2']
    return df

features = ['k-bb/ip', 'pCRA', 'csw', 'z+o']
df = decompose(df, features)
X = df[['comp_1', 'comp_2']]

# X.to_csv('speX_pca.csv')

def calc_vif(X):
    vif = pd.DataFrame()
    vif['variables'] = X.columns
    vif['vif'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return vif

print(calc_vif(df[['k-bb/ip', 'pCRA', 'csw', 'z+o']]))
import pandas as pd, numpy as np

all_data = pd.read_csv('./cfb_data.csv', index_col=0)
print(all_data.head())

all_data.dropna(subset=['w_rank', 'l_rank'], inplace=True, how='all')
all_data.fillna(value={'w_rank': 1000, 'l_rank':1000}, inplace=True)
all_data['w_rank'] = all_data.w_rank.astype(int)
all_data['l_rank'] = all_data.l_rank.astype(int)

all_data.dropna(subset=['w_pts', 'l_pts'], inplace=True, how='any')

all_data = all_data.reset_index(drop=True)

all_data = all_data[all_data.w_rank != all_data.l_rank]
all_data = all_data[np.logical_not(all_data.w_pts == all_data.l_pts)]

all_data.to_csv('./ranked.csv')
print(all_data.head(20))

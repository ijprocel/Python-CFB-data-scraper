import pandas as pd
import numpy as np
from statsmodels.stats.weightstats import DescrStatsW 
import matplotlib.pyplot as plt
from seaborn import set as seaborn_set

def rank_differential(row):
    is_upset = False
    diff = abs(row['l_rank'] - row['w_rank'])

    if row['w_rank'] > row['l_rank']:
        is_upset = True

    return [is_upset, diff]

def calc_upset_percentages(all_data):
    up = all_data[['upset', 'rank_diff']].groupby('rank_diff').agg(['count', 'sum'])
    up.columns = up.columns.droplevel()

    up.rename(columns = {'count': 'games', 'sum': 'upsets'}, inplace=True)
    pct = up.apply(lambda row: (row['upsets']/row['games']) * 100, axis=1)
    up['upset_percentage'] = pct

    up.reset_index(inplace=True)
    up['upsets'] = up['upsets'].astype(int)
    return up

def test_linearity_hypothesis(upset_percentages):
    size = 100000
    pearson = DescrStatsW(upset_percentages[['rank_diff', 'upset_percentage']], weights=upset_percentages['games']).corrcoef[0][1]
    print(f'Actual Pearson correlation coefficient: {pearson: .3f}')

    replicates = np.empty(size)
    diffs = upset_percentages['rank_diff'].to_numpy()
    non_upsets = upset_percentages['upset_percentage'].to_numpy(copy=True)
    
    for i in range(size):
        non_upsets = np.random.permutation(non_upsets)
        stacked = np.column_stack((diffs, non_upsets))
        
        pearson_rep = DescrStatsW(stacked, weights=upset_percentages['games']).corrcoef[0][1]

        replicates[i] = pearson_rep
    
    nine_five_lower = np.percentile(replicates, 2.5)
    nine_five_upper = np.percentile(replicates, 97.5)

    print(f'Min: {np.min(replicates)}')
    print(f'2.5 percentile: {nine_five_lower}')
    print(f'97.5 percentile: {nine_five_upper}')
    print(f'Max: {np.max(replicates)}')

    seaborn_set()

    plt.hist(replicates, bins=20)
    plt.title('Distribution of Pearson coefficients in random permutations of data')
    plt.xlabel('Pearson Coefficient')
    plt.ylabel('Number of Permutations')
    plt.xlim(-1, 1)
    
    plt.axvline(pearson, linestyle='dashed')
    plt.axvline(np.percentile(replicates, 2.5), color='red')
    plt.axvline(np.percentile(replicates, 97.5), color='red')

    plt.annotate('Actual\ncoefficient',
            xy=(-0.78, 0.1*size),
            xycoords='data',
            xytext=(-0.70, 0.12*size),
            arrowprops=
                dict(facecolor='black', shrink=0.00, width=2, headwidth=8),
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=8)
    
    plt.annotate('95% of random\npermutations had\nPearson coefficients\nin this range',
            xy=(nine_five_lower, 0.10*size),
            xycoords='data',
            xytext=(-0.20, 0.10*size),
            arrowprops=
                dict(facecolor='black', shrink=0.00, width=2, headwidth=8),
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=10)
    
    plt.annotate('',
            xy=(nine_five_upper, 0.10*size),
            xycoords='data',
            xytext=(0.20, 0.10*size),
            arrowprops=
                dict(facecolor='black', shrink=0.00, width=2, headwidth=8),
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=10)

    plt.savefig('pearson_reps.png')

all_data = pd.read_csv('./ranked.csv', index_col=0)

diff = all_data.apply(lambda row: rank_differential(row), axis=1, result_type='expand')

all_data = all_data.assign(upset = diff[0], rank_diff = diff[1])

print(all_data.head(20))
print('\n\n')

upset_percentages = calc_upset_percentages(all_data)

print(upset_percentages)
print()

test_linearity_hypothesis(upset_percentages)

upset_percentages.plot(x='rank_diff', xlim=(0, 25), y='upset_percentage', ylim=(-5, 50), kind='scatter')
plt.title("Prevalence of ranked college football upsets\n(1989-2019)")
plt.xlabel("Difference in opponents' AP rank")
plt.ylabel('% of games that were upsets')

plt.savefig('raw_data.png')

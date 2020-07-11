import requests, pandas as pd, sys, time
from bs4 import BeautifulSoup

def get_data_for_season(year):
    #Create BS object from entire webpage
    url = f'https://www.sports-reference.com/cfb/years/{year}-schedule.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    
    #Create 2nd BS object from the header row of the table only
    row_text = str(soup.find('tr'))    
    soup2 = BeautifulSoup(row_text)

    #Use 2nd BS object to get a list of table headers
    headers_html = soup2.find_all('th')
    header_list = [h.get_text() for h in headers_html]
    header_list.remove('Rk')

    #Initialize a dictionary to store season data
    cfb_data = {k:[] for k in header_list}

    #Find all table data entries
    get_data = soup.find_all('td')

    #Loop through data entries. Assign them to a header based on their position in the row.
    x = 0
    for cell in get_data:
        cfb_data[header_list[x]].append(cell.get_text())  #Use header_list instead of dictionary keys directly due to duplicate "Pts" column headers
        x +=1
        if x == len(header_list):
            x = 0
    
    #Split "Pts" column into "w_pts" and "l_pts" by assigning alternating values to each one
    cfb_data['w_pts'] = cfb_data['Pts'][::2]
    cfb_data['l_pts'] = cfb_data['Pts'][1::2]
    cfb_data.pop('Pts', None)

    #Unlabeled column indicates if it was a home game for the losing team. Give column meaningful name.
    cfb_data['home_away'] = cfb_data.pop('')

    #Create DataFrame and filter unnecessary columns
    df = pd.DataFrame(cfb_data)
    df = df[['Winner', 'w_pts', 'home_away', 'l_pts', 'Loser', 'Wk']]
    
    df['season'] = year

    #Extract AP Poll rankings from team names and put them in their own columns.
    df['w_rank'] = df['Winner'].str.extract('(\d\d?)', expand=False)
    df['l_rank'] = df['Loser'].str.extract('(\d\d?)', expand=False)
    
    #Remove AP ranking from team names.	
    df['Winner'] = df['Winner'].str.replace('\s*\(\d\d?\)\s', '')
    df['Loser'] = df['Loser'].str.replace('\s*\(\d\d?\)\s', '')

    #Append new DataFrame to master list of DataFrames, give status update, increment counter, sleep
    dfs.append(df)
    print(str(year) + '  done!')

start = int(sys.argv[1])
end = int(sys.argv[2])

if start > end:
    raise ValueError('start year must be less than or equal to end year')

delay = 0
if len(sys.argv) == 4:
    delay = float(sys.argv[3])

#Initialize a list to hold sub-DataFrames for each individual year
dfs = []

for year in range(start, end+1, 1):
    get_data_for_season(year)
    time.sleep(delay)

final_df = pd.concat(dfs)

#Make column headers all-lowercase
final_df.rename(columns={'Wk':'week', 'Winner':'winner', 'Loser':'loser'}, inplace=True)

#Drop games that weren't actually played, convert scores to integers
final_df['w_pts'] = pd.to_numeric(final_df.w_pts, errors='coerce')
final_df['l_pts'] = pd.to_numeric(final_df.l_pts, errors='coerce')
final_df.dropna(subset=['w_pts', 'l_pts'], how='any', inplace=True)
final_df['w_pts'] = final_df.w_pts.astype(int)
final_df['l_pts'] = final_df.l_pts.astype(int)

#Fix index and reorder columns
final_df = final_df.reset_index(drop=True)
final_df = final_df[['season', 'week', 'winner', 'w_rank', 'w_pts', 'home_away', 'loser', 'l_rank', 'l_pts',]]

final_df.to_csv('./cfb_data.csv')
print(final_df.head())

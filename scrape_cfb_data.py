########################################################################
# Author: Ignacio Procel
# Date: July 11, 2020
# Purpose: To scrape college football data from sports-reference.com and
# save it to a comma-delimited table.
########################################################################

import requests, pandas as pd, sys, time
from bs4 import BeautifulSoup

class ScrapeCfbData:
    def __init__(self, start, end, delay):
        #Initialize a list of sub-DataFrames for each individual year
        self.dfs = []

        for year in range(start, end+1, 1):
            self.get_data_for_season(year)
            time.sleep(delay)

        final_df = pd.concat(self.dfs)

        self.format_and_write_csv(final_df)

    def get_data_for_season(self, year):
        self.create_bs_objects(year)

        #Get a list of table headers
        headers_html = self.header_soup.find_all('th')
        header_list = [h.get_text() for h in headers_html]
        header_list.remove('Rk')

        #Initialize a dictionary to store season data
        cfb_data = {k:[] for k in header_list}
        
        self.populate_season_dict(cfb_data, header_list)

        df = self.create_season_dataframe(cfb_data)
        df['season'] = year

        self.extract_ap_ranking(df)

        #Append new DataFrame to master list, give status update
        self.dfs.append(df)
        print(str(year) + '  done!')
    
    def create_bs_objects(self, year):
        url = f'https://www.sports-reference.com/cfb/years/{year}-schedule.html'
        r = requests.get(url)
        self.page_soup = BeautifulSoup(r.text)

        #Create BS object from the first header row of the table only
        row_text = str(self.page_soup.find('tr'))
        self.header_soup = BeautifulSoup(row_text)
    
    def populate_season_dict(self, season_dict, header_list):
        get_data = self.page_soup.find_all('td')

        #Loop through data entries. Assign them to appropriate header
        x = 0
        for cell in get_data:
            season_dict[header_list[x]].append(cell.get_text())
            x +=1
            if x == len(header_list):
                x = 0
    
    def create_season_dataframe(self, cfb_data):
        #Split "Pts" column into "w_pts" and "l_pts" by assigning alternating values to each one
        cfb_data['w_pts'] = cfb_data['Pts'][::2]
        cfb_data['l_pts'] = cfb_data['Pts'][1::2]
        cfb_data.pop('Pts', None)

        #Unlabeled column indicates if it was a home game for the losing team. Give column meaningful name.
        cfb_data['home_away'] = cfb_data.pop('')

        #Create DataFrame and filter unnecessary columns
        df = pd.DataFrame(cfb_data)
        df = df[['Winner', 'w_pts', 'home_away', 'l_pts', 'Loser', 'Wk']]

        return df

    def extract_ap_ranking(self, df):
        df['w_rank'] = df['Winner'].str.extract('(\d\d?)', expand=False)
        df['l_rank'] = df['Loser'].str.extract('(\d\d?)', expand=False)
        
        #Remove AP ranking from team names.	
        df['Winner'] = df['Winner'].str.replace('\s*\(\d\d?\)\s', '')
        df['Loser'] = df['Loser'].str.replace('\s*\(\d\d?\)\s', '')
    
    def format_and_write_csv(self, final_df):
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
        final_df = final_df[['season', 'week', 'winner', 'w_rank', 'w_pts', 
                    'home_away', 'loser', 'l_rank', 'l_pts',]]

        final_df.to_csv('./cfb_data.csv')
        print(f'\n{final_df.head()}')


start = int(sys.argv[1])
end = int(sys.argv[2])

if start > end:
    raise ValueError('start year must be less than or equal to end year')

delay = 0
if len(sys.argv) == 4:
    delay = float(sys.argv[3])

s = ScrapeCfbData(start, end, delay)
# Python-CFB-data-scraper
This is a program that scrapes Division 1 FBS/Division 1-A college football results from https://www.sports-reference.com/.  

## Usage  
The user gives 2 or 3 parameters as command-line arguments: a start and end year, inclusive (required parameters) and a time delay in seconds between requests (optional parameter). There will be one request made per season requested. Ex:  
```  
$ python3 request_practice.py 2008 2018 5  
```  
Will return 11 seasons of data with a 5 second delay between requests. Start year must be less than or equal to end year.  

## Output  
The program returns, and saves to a CSV, a DataFrame with 9 columns. Each row is an individual game and the columns are:  
![alt text](Python-CFB-data-scraper/Screenshot from 2019-01-15 20-08-06.png)  
-The winner  
-The loser  
-The winner's AP Poll rank (if applicable)  
-The loser's AP poll rank (if applicable)  
-The number of points scored by the winner  
-The number of points scored by the loser  
-A column indicating if the home team lost.†  
-Which season the game took place (January bowl games are grouped with the season that they followed)  
-The week of the season that the game took place (1st week, 2nd, etc.)  

†*The "home_away" flag only tells you if the home team lost. Games where the home team won and games played at a neutral site are not differentiated*  

## Libraries used  
Requests, Pandas, sys, BeautifulSoup, time

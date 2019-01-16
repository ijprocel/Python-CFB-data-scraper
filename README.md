# Python-CFB-data-scraper
This is a program that scrapes Division 1 FBS/Division 1-A college football results from https://www.sports-reference.com/.  

## Usage  
The user gives 2 or 3 parameters as command-line arguments: a start and end year, inclusive (required parameters) and a time delay in seconds between requests (optional parameter). There will be one request made per season requested. Ex:  
```  
$ python3 request_practice.py 2008 2017 5  
```  
Will return 10 seasons of data with a 5 second delay between requests. Start year must be less than or equal to end year.  

## Output  
![alt text](https://github.com/ijprocel/Python-CFB-data-scraper/blob/ijprocel-patch-1/output-example.png)  
  
The program returns, and saves to a CSV, a DataFrame with 9 columns. It contains the name, points scored, and AP rank (if applicable) for the teams involved, a flag indicating if the home team lost†, as well as the year (January bowl games are grouped with the season that they followed) and week of the season the game took place.    

†*The "home_away" flag only tells you if the home team lost. Games where the home team won and games played at a neutral site are not differentiated from each other*  

## Libraries used  
Requests, Pandas, sys, BeautifulSoup, time

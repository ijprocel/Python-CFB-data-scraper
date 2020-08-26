# Scrape college football data with Python!
This is a program that scrapes Division 1 FBS/Division 1-A college football results from https://www.sports-reference.com/.  

## Usage  
The user gives 2 or 3 parameters as command-line arguments: a start and end year, inclusive (required parameters), and a time delay in seconds between requests (optional parameter). There will be one request made per season requested. 

Ex:  
```  
$ python3 scrape_cfb_data.py 2008 2017 5  
```  
Will return 10 seasons of data with a 5 second delay between requests. Start year must be less than or equal to end year.  

## Output  
![alt text](https://github.com/ijprocel/Python-CFB-data-scraper/blob/master/output-example.png)  
  
The program returns, and saves to a CSV, a DataFrame where each row contains information about a single game. It contains the name, points scored, and AP rank (if applicable) for the teams involved, the year\* and week of the season the game took place, as well as a flag indicating if the home team lost†.    

\**January bowl games are grouped with the season that they followed*    

†*The "home_away" flag only tells you if the home team lost. Games where the home team won and games played at a neutral site are not differentiated from each other*  

## Libraries used  
Requests, Pandas, sys, BeautifulSoup, time

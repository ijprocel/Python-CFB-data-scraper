# Python-CFB-data-scraper
This is a program that scrapes college football results from https://www.sports-reference.com/. The user gives a start and end year (inclusive)\* as command-line arguments and the program returns a DataFrame with 9 columns. Each row is an individual game and the columns are:  
-The winner  
-The loser  
-The winner's AP Poll rank and loser's AP poll rank (if applicable)  
-The number of points scored by the winner and by the loser  
-A column indicating if the home team lost.†  
-Which season the game took place (January bowl games are grouped with the season that they followed)  
-The week of the season that the game took place (1st week, 2nd, etc.)  

\**python3 request_practice.py start end. Start year is lower/earlier*

†*The "home_away" flag only tells you if the home team lost. Games where the home team won and games played at a neutral site are not differentiated*

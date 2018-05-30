# Lineup Optimizer for ESPN Fantasy Basketball

### Running the optimizer
In the file directory, run analysis.py

```bash
python analysis.py
```

You will be prompted for some info. Keep your ESPN information handy by navigating to your fantasy team page. The information required should be in the URL. For example, given the following URL:
[http://games.espn.com/fba/clubhouse?leagueId=445514&teamId=1&seasonId=2018]( http://games.espn.com/fba/clubhouse?leagueId=445514&teamId=1&seasonId=2018 ), you should input the following when prompted:  

```
Please enter your league ID: 445514
Please enter your team ID: 1
Please enter the week number: 10
Please enter the opposing team name (e.g. 'TEAM YAO'): TEAM YAO
```

Note: week number depends on which week of the season you want to look at. Probably just enter the latest week. 

#### Top 2 lineups for Dec. 20, 2017

TEAM 2:  (score: 10.910064304011993)

James Harden <br />
Chris Paul <br />
DeMarcus Cousins <br />
Kyle Lowry <br />
Kevin Love <br />
Khris Middleton <br />
Gary Harris <br />
Donovan Mitchell <br />
Trevor Ariza <br />
Hassan Whiteside <br />
Kent Bazemore <br />
Evan Fournier <br />
Tyreke Evans <br />

=============================


TEAM 1:  (score: 11.00582258452509)

James Harden <br />
Chris Paul <br />
DeMarcus Cousins <br />
Kyle Lowry <br />
Kevin Love <br />
Khris Middleton <br />
Gary Harris <br />
Donovan Mitchell <br />
Trevor Ariza <br />
Hassan Whiteside <br />
Kent Bazemore <br />
Evan Fournier <br />
Andre Drummond <br />

=============================

### Backtest
It may be interesting to see how your team performs against other teams historically. 


#### Setting up
First we will create a few csv tables by scraping ESPN and BBM online webpages. In the main directory, run the following script:

```python
python get_historic_data.py
```

You will be prompted for starting and ending years. This range should overlap the range of dates where you plan to backtest over. For example, if you plan to backtest over Dec 2017 through Feb 2018, then you would enter the following: 

```
Enter starting year: 2017
Enter ending year: 2018
```

#### Stored Data
You can access historic data after running the script in the `historicData` directory. These files should be arranged by type and year. 

#### Running backtest
Once historic data has been stored, we can create a backtest instance by running the following script in the main directory: 

```python
python backtest.py
```

You will be initially prompted for information similar the `analysis.py` script. Enter the relevant information. From there, you should see the following: 

```
Collecting data...
Create team to test by entering players' names, separated by comma: 
```

Here, you should enter 13 players separated by commas. You can either use the recommended teams from running `analysis.py` or pick your own 13 players.

Next, you will be prompted for the range of dates where you plan to backtest over: 

```
Enter start date: (e.g. 2017-10-17)
Enter end date: (e.g. 2017-11-26)
```

Based on the list of players you previously inputed and the other teams in the fanstasy league, time series plots for each of the stat categories, where each plot compares the performances of each team, should appear. For example:

Note: x-axis format is YEAR-WEEK

![Alt text](/images/2018_comparison.png)<br />



## NOTES: 
11/27 
Look at prvious years' performances for all players on all teams and compare 

10/11
Added backtesting data (every players stats for each game/date) - still needs some development 

10/3:
Added ESPN stats for each team in league for hypothetical matchups
Return best lineup based on available player universe - this is calculated by finding the combination of players which maximizes the sum of the weighted zscores in each stat category

SIDE NOTE: Zscores are weighted by the "predicting power" zscore (aka. what BBM calls stat value, e.g. toV, pV,...) and the equivalent actual score. If teamA's assists zscore is much higher than teamB's assists zscore and if teamA's actual assist count is much higher than teamB's assist count, then the assists zscore is considered more predictive. Essentially I think there is too much noise is some of the stat categories (there is very little variance in FG% and FT% across all the players), 

10/2:
Started analysis by comparing all teams in league with BBM ranking system

9/30: 
Created setup for data extraction from ESPN Fantasy site and BBM (basketball monster)
Got data from free agency, current roster
Got opposition rosters

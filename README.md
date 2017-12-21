# Lineup Optimizer for ESPN Fantasy Basketball

### Running the optimizer
In the file directory, run analysis.py

```py
python analysis.py
```

You will be prompted for some info. Keep your ESPN information handy by navigating to your fantasy team page. The information required should be in the URL. For example, given the following URL:
[http://games.espn.com/fba/clubhouse?leagueId=445514&teamId=1&seasonId=2018]( http://games.espn.com/fba/clubhouse?leagueId=445514&teamId=1&seasonId=2018 ), input the following when prompted:  

```
Please enter your league ID: 445514
Please enter your team ID: 1
Please enter the week number: 10
```


### Top 5 lineups for Dec. 20, 2017

TEAM 5:  (score: 10.708079315080555)

James Harden
Chris Paul
DeMarcus Cousins
Kyle Lowry
Kevin Love
Khris Middleton
Gary Harris
Donovan Mitchell
Trevor Ariza
Hassan Whiteside
Kent Bazemore
Andre Drummond
Tyreke Evans

=============================


TEAM 4:  (score: 10.840894516019457)

James Harden
Chris Paul
DeMarcus Cousins
Kyle Lowry
Kevin Love
Khris Middleton
Gary Harris
Donovan Mitchell
Trevor Ariza
Hassan Whiteside
Kent Bazemore
Evan Fournier
Tobias Harris

=============================


TEAM 3:  (score: 10.88625247856297)

James Harden
Chris Paul
DeMarcus Cousins
Kyle Lowry
Kevin Love
Khris Middleton
Gary Harris
Donovan Mitchell
Trevor Ariza
Hassan Whiteside
Kent Bazemore
Evan Fournier
Kentavious Caldwell-Pope

=============================


TEAM 2:  (score: 10.910064304011993)

James Harden
Chris Paul
DeMarcus Cousins
Kyle Lowry
Kevin Love
Khris Middleton
Gary Harris
Donovan Mitchell
Trevor Ariza
Hassan Whiteside
Kent Bazemore
Evan Fournier
Tyreke Evans

=============================


TEAM 1:  (score: 11.00582258452509)

James Harden
Chris Paul
DeMarcus Cousins
Kyle Lowry
Kevin Love
Khris Middleton
Gary Harris
Donovan Mitchell
Trevor Ariza
Hassan Whiteside
Kent Bazemore
Evan Fournier
Andre Drummond

=============================

## TODO: 
Given backtest data, generate backtesting platform

## Progress: 
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

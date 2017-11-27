import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from get_data import LeagueData
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
matplotlib.style.use('fivethirtyeight')
months = mdates.MonthLocator()  # every month


startyear = 2016 
endyear = 2017

Data = LeagueData(leagueID='445514', teamID='1', week=5)
directory = 'data/historicData/PlayerGames/'

all_data = []
for year in range(startyear, endyear+1):
    file_loc = directory + 'stats_{}_player_stats_by_game.csv'.format( year )

    dtype_map = {'MIN': np.float64, 
                'REB': np.float64, 
                'AST': np.float64, 
                'STL': np.float64, 
                'BLK': np.float64,
                'TO': np.float64, 
                'PF': np.float64, 
                'PTS': np.float64 }

    # data = pd.read_csv(file_loc, index_col=[0], na_values='--', dtype=dtype_map ).set_index('date')
    data = pd.read_csv(file_loc, index_col=[0], na_values='--', dtype=dtype_map )
    all_data.append(data)

data = pd.concat( all_data )
# data['Date'] = pd.to_datetime(data['Date'])
data['Week'] = data['Date'].apply( lambda x: pd.to_datetime(x).isocalendar()[1] )
data['Week'] = data.apply( lambda row: row['Week']+52 if pd.to_datetime(row['Date']).year==2017 else row['Week'], axis=1 )
data = data.set_index('Date')

team1 = {'DeMarcus Cousins', 'Andre Drummond', 'Chris Paul', 'James Harden', 'Hassan Whiteside', 
        'Steven Adams', 'James Johnson', 'Kevin Love', 'Elfrid Payton', 'Pau Gasol', 'Enes Kanter', 
        'Evan Fournier', 'Rondae Hollis-Jefferson' }

my_team_data = data.loc[ data.player.isin([player.title().replace('-', ' ') for player in team1]) ]
# my_team_data.groupby('player').sum()

teams = Data.get_all_teams()

teams['OPT_TEAM'] = team1  # add in optimal team from calcBestTeam()

startdate = '2017-10-17'
enddate = '2017-11-26'
dates = [date.strftime("%Y-%m-%d") for date in pd.date_range(startdate, enddate).tolist()]

# start_date = datetime(2016,10,25)
# end_date = datetime(2017,4,1)

categories = {'REB', 'AST', 'STL', 'BLK',
       'TO', 'PF', 'PTS', '3PTsMade'}


fig, axes = plt.subplots(4, 2, sharex=True, figsize=(15,20))

axes = axes.ravel()

for i, category in enumerate(categories):
    for team, players in teams.items():
        player_stats = data.loc[ data.player.isin([player.title().replace('-', ' ') for player in players]) ]
        # player_stats = player_stats.loc[ (player_stats.Date > start_date) & (player_stats.Date <= end_date) ]
        player_stats = player_stats.loc[ dates ]
        player_stats.index = pd.to_datetime(player_stats.index)

        kw = lambda x: pd_to_datetime(x).isocalendar()[1]; 
        kw_year = lambda x: str(pd.to_datetime(x).year) + ' - ' + str(pd.to_datetime(x).isocalendar()[1])

        player_stats_sum = player_stats.groupby([player_stats.index.map(kw_year)]).sum()

        # player_stats_sum = player_stats.groupby('Date').sum()
        axes[i] = player_stats_sum[category].plot( ax=axes[i], marker = 'o',
                                     linestyle='--', label=team )
        axes[i].set_title(category)
        axes[i].legend()
        # axes[i].xaxis.set_major_locator(months)
# plt.figlegend( axes, teams.keys(), loc = 'lower center', ncol=5, labelspacing=0. )

plt.savefig('images/2017_comparison.pdf', format='pdf')
plt.show()

import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from get_data import LeagueData
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
months = mdates.MonthLocator()  # every month

import pdb

class Backtest():
    '''
    Compare team's performance against other teams for 
    entire year
    '''
    def __init__(self, year, leagueID, teamID, week):
        # super(Backtest, self).__init__()
        self.leagueID = leagueID
        self.teamID = teamID
        self.week = week
        self.startyear = year
        self.endyear = year+1
        self.leagueData = None
        self.historicData = None
        self.directory = 'data/historicData/PlayerGames/'
        self.getData()

    def getData(self):
        '''
        This function is called during the class instantiation
        This creates pandas dataframes holding stats for the fantasy league
        as well as all historic player stats for every game in the time frame
        '''

        print("Collecting data...")

        # get league data specific to fantasy league
        self.leagueData = LeagueData(str(self.leagueID), str(self.teamID), self.week)

        # get historic data from espn csvs
        all_data = []
        for year in range(self.startyear, self.endyear+1):
            file_loc = self.directory + 'stats_{}_player_stats_by_game.csv'.format( year )

            dtype_map = {'MIN': np.float64, 
                        'REB': np.float64, 
                        'AST': np.float64, 
                        'STL': np.float64, 
                        'BLK': np.float64,
                        'TO': np.float64, 
                        'PF': np.float64, 
                        'PTS': np.float64 }

            # data = pd.read_csv(file_loc, index_col=[0], na_values='--', dtype=dtype_map ).set_index('date')
            _data = pd.read_csv(file_loc, index_col=[0], na_values='--', dtype=dtype_map )
            all_data.append(_data)

        self.historicData = pd.concat( all_data )

        # we will record data by week number (total 52 weeks in year one, year two's first week starts at week 53)
        self.historicData['Week'] = self.historicData['Date'].apply( lambda x: pd.to_datetime(x).isocalendar()[1] )
        self.historicData['Week'] = self.historicData.apply( lambda row: row['Week']+52 
                                                            if pd.to_datetime(row['Date']).year==self.endyear 
                                                            else row['Week'], axis=1 )

        self.historicData = self.historicData.set_index('Date')


    def run(self, test=False):
        '''
        Main function of Backtest class
        This function allows the user to input a list of players to be 'backtested' against the other teams in 
        the fanstasy league historically. The results should be displayed in time series plots for each of the 
        stat categories, where each plot compares the performances of each team.
        '''
        if test:
            input_team = {'DeMarcus Cousins', 'Andre Drummond', 'Chris Paul', 'James Harden', 'Hassan Whiteside', 
                        'Steven Adams', 'James Johnson', 'Kevin Love', 'Elfrid Payton', 'Pau Gasol', 'Enes Kanter', 
                        'Evan Fournier', 'Rondae Hollis-Jefferson' }
        else:
            print("Create team to test by entering players' names, separated by comma: ")
            input_team = {player for player in input().split(',')}
            print(input_team)

        # get input team stats
        my_team_data = self.historicData.loc[ self.historicData.player.isin([player.title().replace('-', ' ') for player in input_team]) ]
        
        # get all teams and stats
        teams = self.leagueData.get_all_teams()
        teams['OPTIMAL_TEAM'] = input_team 

        print("Enter start date: (e.g. 2017-10-17)")
        startdate = input()
        
        print("Enter end date: (e.g. 2017-11-26)")
        enddate = input()

        dates = [date.strftime("%Y-%m-%d") for date in pd.date_range(startdate, enddate).tolist()]

        categories = {'REB', 'AST', 'STL', 'BLK',
               'TO', 'PF', 'PTS', '3PTsMade'}


        def plot():
            # pdb.set_trace()

            fig, axes = plt.subplots(4, 2, sharex=True, figsize=(15,25))

            axes = axes.ravel()

            for i, category in enumerate(categories):
                for team, players in teams.items():
                    player_stats = self.historicData.loc[ self.historicData.player.isin([player.title().replace('-', ' ') for player in players]) ]
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

            plt.savefig('images/{}_comparison.pdf'.format(self.endyear), format='pdf')
            plt.show()

        plot()


if __name__ == '__main__':
    test = Backtest(2017, 445514, 1, 5)
    test.run(test=True)
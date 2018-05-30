import pandas as pd
from get_data import LeagueData
import numpy as np
import itertools
import argparse

'''
Combine datasets from ESPN and BBM to 'grade' teams in league
We need to come up with a combination of players in the available player 
universe (consists of FAs and current team) that has a better grade than 
the opposing team(s)
'''


def player_universe():
    '''
    Given the available player universe, create 
    dataset combining BBM and ESPN data 
    '''
    all_avail_players = Data.get_player_universe()
    bbm_raw_data, bb_zscores_data = Data.get_bbm_data()
    result = pd.concat([bb_zscores_data, all_avail_players], axis=1, join='inner')
    return result
    # result.sort_values('Rank').iloc[:13]  # gets top 13 available players according to bbm ranking

def compare_stats(table):
    '''
    helper function to compare stats for DF of teams
    '''
    games = []
    titles = []
    for team1, stats1 in table.iterrows():
        for team2, stats2 in table.iterrows():
            # print( '\n{} vs. {}'.format(team1, team2) )
            # print( stats1-stats2 )
            # print( '====================')
            title = [team1, team2]
            titles.append(title)
            games.append(stats1-stats2)
    games = pd.DataFrame(games)
    games['TEAM1'], games['TEAM2'] = [t[0] for t in titles], [t[1] for t in titles]
    games = games.reset_index(drop=True)
    return games

def rankingMatchups():
    '''
    Using BBM grades (zscore), compare all teams in league on each 
    of the categories: bbm rank, fg%, ft%, 3pm, reb, ast, stl, blk, pts, tos

    Based on BBM rankings, compare the 
    average rank of players for each team against
    for MY team ('YAO')
    '''
    teams = Data.get_all_teams()
    raw, zscores = Data.get_bbm_data()
    scores = []
    for team_name, players in teams.items():
        scores.append(zscores.loc[players,:].sum())
    scores = pd.DataFrame(scores,index=teams)
    scores.Rank = scores.Rank/13 # get average rank
    scores.toV = -scores.toV  # match sign with ESPN
    games = compare_stats(scores)
    return games
    # return games.loc[ games['TEAM1'].str.contains('YAO') & ~games['TEAM2'].str.contains('YAO')]


def actualMatchups():
    '''
    Look at ACTUAL matchups (real and hypothetical) for the week 
    Get data from ESPN using get_all_teams_stats() from get_data module
    '''
    teams, categories = Data.get_all_teams_stats()
    teams = pd.DataFrame([t[2:] for t in teams], index=[t[0] for t in teams], columns=categories)
    teams = teams.apply(pd.to_numeric)
    games = compare_stats(teams)
    return games
    # return games.loc[ games['TEAM1'].str.contains('Yao') & ~games['TEAM2'].str.contains('Yao')]

def compareRankActual():
    '''
    How good of a predictor is BBM ranking in terms
    of winning categories? Compare rank and actual results 
    from all hypothetical games played
    '''

    rank, actual = rankingMatchups(), actualMatchups()

    # create join column
    rank['matchup'] = rank['TEAM1'].map(str) + ',' + rank['TEAM2']
    actual['matchup'] = actual['TEAM1'].map(str) + ',' + actual['TEAM2']
    rank, actual = rank.sort_values('matchup'), actual.sort_values('matchup')

    # Map for categories from ESPN to BBM
    stat_groups = {
        'FG%' : 'fg%V', 
        'FT%' : 'ft%V', 
        '3PM' : '3V', 
        'REB' : 'rV', 
        'AST' : 'aV', 
        'STL' : 'sV', 
        'BLK' : 'bV', 
         'TO' : 'toV',
         # 'PF' : None,
         # 'DD' : None,
        'PTS' : 'pV'
    }

        
    correlations = {}
    for actual_stat, rank_stat in stat_groups.items():
        # print( 'Correlation {}  and  {}'.format(actual_stat, rank_stat) )
        # print( np.corrcoef(rank[rank_stat], actual[actual_stat])[0][1] )
        try:
            correlations[rank_stat] = np.corrcoef(rank[rank_stat], actual[actual_stat])[0][1]
        except KeyError:
            correlations[rank_stat] = 0
    return correlations

def sortPlayerUniv(num_players=20):
    '''
    Try a new, derived ranking system using correlations and 
    specific statistics relevant to the league scoring
    Return the top 20 by default -- change var num_players
    '''
    correlations = compareRankActual()
    player_univ = player_universe()
    player_univ['new_rank'] = 0
    for cat, corr in correlations.items():
        player_univ['new_rank'] += player_univ[cat]*corr

    # return the top 20 guys
    return player_univ.sort_values('new_rank', ascending=False)[:num_players] 

def compareTeams(opp=None, team=None):
    '''
    compare hypothetical team with opponent team (opp)
    input name (ex. 'TEAM YAO')
    '''
    teams = Data.get_all_teams()
    raw, zscores = Data.get_bbm_data()
    scores = []
    for team_name, players in teams.items():
        scores.append(zscores.loc[players,:].sum())
    scores = pd.DataFrame(scores,index=teams)
    scores.Rank = scores.Rank/13 # get average rank
    scores.toV = -scores.toV

    # opp = scores.loc[opp]
    if team:
        hyp = zscores.loc[[i for i in team]]
    else:
        hyp = sortPlayerUniv(num_players=13)

    hyp_stats = hyp.sum()[ scores.columns ]
    hyp_stats['Rank'] = hyp_stats['Rank']/13
    hyp_stats.name = 'TEMP'
    scores = scores.append(hyp_stats)
    games = compare_stats(scores)
    return list(hyp.index), games.loc[ games['TEAM1'].str.contains('TEMP') & ~games['TEAM2'].str.contains('TEMP')]

def calcBestTeam(num_players=20, oppteam=None):
    '''
    Calculate the best lineup based on BBM stats and correlations between 
    BBM stats and actual performance
    '''

    pool = sortPlayerUniv(num_players=num_players)
    all_teams = list(itertools.combinations(pool.index, 13))
    teams = Data.get_all_teams()
    raw, zscores = Data.get_bbm_data()
    scores = []
    for team_name, players in teams.items():
        scores.append(zscores.loc[players,:].sum())
    scores = pd.DataFrame(scores,index=teams)
    scores.Rank = scores.Rank/13 # get average rank
    # scores.toV = -scores.toV

    # search team names for user input team name
    opp = None
    for team_name in teams.keys():
        if oppteam in team_name:
            opp = team_name
        
    if opp is None:
        print("Entered team ", oppteam, " not found.")
        return

    # optimize wrt current opponent for the week
    opp_stats = scores.loc[opp]

    # get correlations -- make it in the order of opp_stats
    corr = compareRankActual()
    correlation_vector = [ corr[cat] for cat in opp_stats.index[1:] ]
    print( corr )

    teams_stats = []
    for team in all_teams:
        hyp = zscores.loc[[i for i in team]]
        hyp_stats = hyp.sum()[ scores.columns ]
        hyp_stats['Rank'] = hyp_stats['Rank']/13
        hyp_stats.name = 'TEMP'
        teams_stats.append(hyp_stats)

    teams_stats = np.array(teams_stats)
    opp_stats = np.array(opp_stats)
    value_vector = np.dot( (teams_stats-opp_stats)[:,1:] , correlation_vector )  # cutting out ranking for now

    suggestions = [all_teams[i] for i in value_vector.argsort()[-5:] ]  # suggested lineups (top 5)
    score = np.sort(value_vector)[-5:]

    team, best_performance = compareTeams(team=suggestions[-1])

    for i,suggest in enumerate(suggestions):
        print('\nTEAM {}:  (score: {})\n'.format(5-i, score[i]))
        for player in suggest:
            print(player)
        print('\n=============================\n')

    return all_teams[value_vector.argmax()]



if __name__ == '__main__':
    # print( compareTeams()[0] )
    # compareTeams()[1].to_csv('results.csv')
    # print ( compareRankActual() )
  
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()

    if args.t:
        Data = LeagueData(leagueID='445514', teamID='1', week=10)
        opponent = "LIU"
        calcBestTeam(oppteam=opponent)

    elif ~args.t:    
        leagueID = input("Please enter your league ID: ")
        teamID = input("Please enter your team ID: ")
        week = input("Please enter the week number: ")
        opponent = input("Please enter the opposing team name (e.g. 'TEAM YU'): ")
        # Data = LeagueData(leagueID='445514', teamID='1', week=10)
        Data = LeagueData(leagueID=leagueID, teamID=teamID, week=int(week))
        calcBestTeam(oppteam=opponent)

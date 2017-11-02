import pandas
import get_data

'''
Combine datasets from ESPN and BBM to 'grade' teams in league
We need to come up with a combination of players in the available player 
universe (consists of FAs and current team) that has better grades than 
the other teams
'''

def player_univ_analysis():
    '''
    Given the available player universe, find the 
    best lineup for beating the other teams
    '''
    all_avail_players = get_data.get_player_universe()
    bbm_raw_data, bb_zscores_data = get_data.get_bbm_data()
    result = pd.concat([bb_zscores_data, all_avail_players], axis=1, join='inner')
    return result
    # result.sort_values('Rank').iloc[:13]  # gets top 13 available players according to bbm ranking


def compare_all_teams():
    '''
    Using BBM grades (zscore), compare all teams in league on each 
    of the categories: bbm rank, fg%, ft%, 3pm, reb, ast, stl, blk, pts, tos
    '''
    teams = get_data.get_all_teams()
    scores = []
    for team_name, players in teams.items():
        print ( team_name, zscores.loc[players,:].sum() )
        scores.append(zscores.loc[players,:].sum())
    scores = pd.DataFrame(scores,index=teams)
    return scores
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import random
import calendar
from datetime import datetime, date
from tqdm import tqdm
import time 

def getPlayerStats(startyear=2017, endyear=2017):
    '''
    Given a range of years, this function will output player stats for 
    each of the years into respective dataframes / csv files
    '''
    url = 'http://espn.go.com/nba/teams'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "lxml")
    tables = soup.find_all('ul', class_='medium-logos')
    teams = []
    prefix_1 = []
    prefix_2 = []
    teams_urls = []
    for table in tables:
        lis = table.find_all('li')
        for li in lis:
            info = li.h5.a
            teams.append(info.text)
            url = info['href']
            teams_urls.append(url)
            prefix_1.append(url.split('/')[-2])
            prefix_2.append(url.split('/')[-1])

    team_prefixes_bbal_ref = ['BOS', 'BRK', 'NYK', 'PHI', 'TOR', 'GSW', 'LAC', 'LAL', 'PHO', 'SAC', 
                              'CHI', 'CLE', 'DET', 'IND', 'MIL', 'DAL', 'HOU', 'MEM', 'NOP', 'SAS', 'ATL',
                              'CHO', 'MIA', 'ORL', 'WAS', 'DEN', 'MIN', 'OKC', 'POR', 'UTA' ]

    dic = {'team': teams, 'url': teams_urls, 'prefix_2': prefix_2, 'prefix_1': prefix_1, 'bball_ref_prefix': team_prefixes_bbal_ref }
    # teams = pd.DataFrame(dic, index=teams)
    teams = pd.DataFrame(dic)


    BASE_URL_BBALL_REF = 'http://www.basketball-reference.com/teams/{0}/{1}.html'
    # r = requests.get(BASE_URL_BBALL_REF)
    column_headers = [u'Name', u'Age', u'G', u'GS', u'MP', u'FG', 
                    u'FGA', u'FG%', u'3P', u'3PA', u'3P%', u'2P', 
                    u'2PA', u'2P%', u'eFG%', u'FT', u'FTA', u'FT%', 
                    u'ORB', u'DRB', u'TRB', u'AST', u'STL', u'BLK', 
                    u'TOV', u'PF', u'PTS']

    for year in range(startyear, endyear+1):
        player_data = []
        for index, row in teams.iterrows():
            # print (row)
            # print(BASE_URL_BBALL_REF.format(row['bball_ref_prefix'].upper(), year))
            source_code = requests.get(BASE_URL_BBALL_REF.format(row['bball_ref_prefix'].upper(), year))
            plain_text = source_code.text
            html = str(BeautifulSoup(plain_text, "lxml").find(id="all_totals"))
            formatted_html = html.replace("<!--", "")
            table = BeautifulSoup(formatted_html, "lxml").find(id="totals")
            table = table.find_all('tr')
    #         player_data_per_team = []
            for row in table[1:]:
                data = [td.getText() for td in row.findAll('td')]
                player_data.append(data)
    #         without_totals = player_data_per_team[:-1]
    #         print(without_totals)
    #         formatted_data = [[data[0].encode('utf-8')] + [float(x) for x in data[1:]] for data in without_totals]
    #         player_data.append(without_totals)
        player_stats = pd.DataFrame(player_data, columns=column_headers)
        # print( df.head)

    return teams, player_stats
        # df.to_csv("player_stats_bball_ref" + str(year) + ".csv")

def getGames(teams, startyear=2017, endyear=2017):    
    '''
    Given range of years, this function will output games results for 
    each of the years into respective dataframes / csv files
    '''
    teams = pd.read_csv('../fantasy-basketball/teams.csv')
    BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/{2}'

    for year in range(startyear, endyear+1):
        match_id = []
        dates = []
        home_team = []
        home_team_score = []
        visit_team = []
        visit_team_score = []
        for index, row in teams.iterrows():
            # _team, url = row['bball_ref_prefix'], row['url']
            _team, url = row['team'], row['url']
            source_code = requests.get(BASE_URL.format(row['prefix_1'], year, row['prefix_2']))
            plain_text = source_code.text
            table = BeautifulSoup(plain_text, "lxml").table
            for row in table.find_all('tr')[1:]: # Remove header
                columns = row.find_all('td')
                try:
                    _home = True if columns[1].li.text == 'vs' else False
                    _other_team = columns[1].find_all('a')[1].text
                    _score = columns[2].a.text.split(' ')[0].split('-')
                    _won = True if columns[2].span.text == 'W' else False
                    _match_id = columns[2].a['href'].split('id/')[1]
                    d = datetime.strptime(columns[0].text, '%a, %b %d')
                    # print(columns)
                    # raise Exception('I know Python!')
                    dates.append(date(year, d.month, d.day))
                    match_id.append(_match_id)
                    home_team.append(_team if _home else _other_team)
                    visit_team.append(_team if not _home else _other_team)
                    
                    if _home:
                        if _won:
                            home_team_score.append(_score[0])
                            visit_team_score.append(_score[1])
                        else:
                            home_team_score.append(_score[1])
                            visit_team_score.append(_score[0])
                    else:
                        if _won:
                            home_team_score.append(_score[1])
                            visit_team_score.append(_score[0])
                        else:
                            home_team_score.append(_score[0])
                            visit_team_score.append(_score[1])
                except Exception as e:
                    pass # Not all columns row are a match, is OK
                    # print(e)

        dic = {'id': match_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team,
                'home_team_score': home_team_score, 'visit_team_score': visit_team_score}

        games = pd.DataFrame(dic).drop_duplicates().set_index('id')

        print( 'Saving games_{}.csv at /data/historicData/'.format(year) )
        games.to_csv('data/historicData/Games/games_{}.csv'.format(year))
    

    return games


def getPlayerGames(year):
    '''
    Given csv file with all games and unique id per game, get every players' 
    stats for each game they played
    '''

    games = pd.read_csv('data/historicData/Games/games_{}.csv'.format( year )).drop_duplicates('id').set_index('id')
    BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'
    columns = ['id', 'Date', 'player', u'MIN', u'FG', u'3PT', u'FT', u'REB', u'AST', u'STL', u'BLK', u'TO', u'PF', u'PTS']

    players = []

    # def get_players(players, team_name):
    #     array = np.zeros((len(players), len(headers)+1), dtype=object)
    #     array[:] = np.nan
    #     for i, player in enumerate(players):
    #         cols = player.find_all('td')
    #         array[i, 0] = cols[0].text.split(',')[0]
    #         for j in range(1, len(headers) + 1):
    #             if not cols[1].text.startswith('DNP'):
    #                 array[i, j] = cols[j].text

    #     frame = pd.DataFrame(columns=columns)
    #     for x in array:
    #         line = np.concatenate(([index, team_name], x)).reshape(1,len(columns))
    #         new = pd.DataFrame(line, columns=frame.columns)
    #         frame = frame.append(new)
    #     return frame

    length = len(games)
    print( "Getting Player stats from every game in {}...".format(year) )
    for index, row in tqdm(games.iterrows(), desc='Progress Bar:', total=length):
        # print(index)
        time.sleep(0.1)
        date = row[0]
        source_code = requests.get(BASE_URL.format(index))
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
        table = soup.find('table', class_='mod-data')
        for c in range (1,5):
            for x in BeautifulSoup(plain_text, "lxml").find_all('tbody')[c].find_all('tr'):
                try:
                    if not x.find(class_="dnp"):
                        full_name = x.find('a')['href'].split('/')[-1].replace('-', ' ').title()
                        position = x.find(class_="position").getText()
                        name = x.find(class_="abbr").getText()
                        _min = x.find(class_="min").getText()
                        threePt = x.find(class_="3pt").getText()
                        ft = x.find(class_="ft").getText()
                        fg = x.find(class_="fg").getText()
                        reb = x.find(class_="reb").getText()
                        ast = x.find(class_="ast").getText()        
                        stl = x.find(class_="stl").getText() 
                        blk = x.find(class_="blk").getText()
                        to = x.find(class_="to").getText() 
                        pf = x.find(class_="pf").getText()
                        pts = x.find(class_="pts").getText()
                        data = [index, date, full_name, _min, fg, ft, threePt, reb, ast, stl, blk, to, pf, pts]
                        players.append(data)
                    # print(players.shape)
                except (IndexError, AttributeError, TypeError):
                    pass

    stats_ = pd.DataFrame(data = players, columns=columns)

    def convert(x):
        try:
            return float(x)
        except Exception as e:
            return 0.0

    #split makes and attempts
    ts = stats_['3PT']
    t = np.array([[convert(x) for x in threes.split('-')] for threes in ts])
    stats_['3PTsMade'] = [x[0] for x in t]
    stats_['3PTsAttempted'] = [x[1] for x in t]

    ts = stats_['FT']
    t = np.array([[convert(x) for x in threes.split('-')] for threes in ts])
    stats_['FTsMade'] = [x[0] for x in t]
    stats_['FTsAttempted'] = [x[1] for x in t]

    ts = stats_['FG']
    t = np.array([[convert(x) for x in threes.split('-')] for threes in ts])
    stats_['FGsMade'] = [x[0] for x in t]
    stats_['FGsAttempted'] = [x[1] for x in t]

    stats_.to_csv( 'data/historicData/PlayerGames/stats_{}_player_stats_by_game.csv'.format(year) )
    return stats_



def test(year):
    # retrieve all player stats for all games in 2017 year
    data = pd.read_csv('stats_2016_player_stats_by_game.csv', index_col=[0]).set_index('id')
    return data

if __name__ == '__main__':
    # startyear = 2016
    # endyear   = 2017
    # teams, player_stats = getPlayerStats(startyear, endyear)
    # games = getGames(teams, startyear, endyear)
    stats = getPlayerGames(2017)
    
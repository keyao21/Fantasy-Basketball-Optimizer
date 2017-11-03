from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

'''
Get the player universe --
this consists of 1.players on my team and 2.(most of) the free agents
This will be done by parsing ESPN's website
'''


def get_players_data(page):
    '''
    Get players from ESPN with stats depending on page (url)
    page: {clubhouse, freeagency}
    '''
    url = 'http://games.espn.com/fba/{}?leagueId=204515&teamId=12&seasonId=2018'.format(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    # get stat categories 
    tableSubHead = soup.find_all('tr', class_='playerTableBgRowSubhead tableSubHead')
    tableSubHead = tableSubHead[0]
    categories = []
    for td in tableSubHead.findAll('td', class_='playertableStat'):
        stat_category = td.find('span')['title']
        categories.append(stat_category)
    categories.extend(['Name', 'Positions'])

    # get stats for each free agent -- populate 2-d matrix
    players = soup.find_all('tr', class_ =re.compile("pncPlayerRow"))
    stat_values = []
    for player in players:
        try:
            # for now we assume no one is injured            
            raw_player_name = player.find('td', class_='playertablePlayerName').get_text()
            player_info = (''.join([i if ord(i) < 128 else ', ' for i in raw_player_name])).split(', ')
            name = player_info[0].replace('.', '').replace('*','')
            team = player_info[1]
            positions = ' '.join([pos for pos in player_info[2:]]) 
            raw_player_stat_values = [td.get_text() if td.get_text() != '--' else '' for td in player.findAll('td', class_='playertableStat')]
            raw_player_stat_values = [stat[:stat.find('/')] if stat.find('/') != -1 else stat for stat in raw_player_stat_values]
            raw_player_stat_values.extend([name, positions])
            stat_values.append(raw_player_stat_values)
        except AttributeError:
            print( "Warning: You haven't completely filled out your current roster!")

    players_data = pd.DataFrame(stat_values, columns=categories)
    players_data = players_data.apply(pd.to_numeric, errors='ignore')
    players_data = players_data.set_index('Name')
    return players_data



def get_bbm_data():
    '''
    Get recent data from basketball monster -- this is currently manually downloaded
    '''
    bbmonsterdata = pd.read_excel('BBM_PlayerRankings.xls').set_index('Name')
    bbmonsterdata_raw = bbmonsterdata[ ['Rank','fg%', 'ft%', '3/g', 'r/g', 'a/g', 's/g', 'b/g', 'p/g', 'to/g'] ]
    bbmonsterdata_zscores = bbmonsterdata[ ['Rank', 'fg%V', 'ft%V', '3V', 'rV', 'aV', 'sV', 'bV', 'pV', 'toV'] ]
    return bbmonsterdata_raw, bbmonsterdata_zscores
    

def get_all_teams():
    '''
    Get dictionary of { teamname : [players] } of all teams
    '''
    url = 'http://games.espn.com/fba/leaguerosters?leagueId=204515'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    tableSubHead = soup.find_all('table', class_='playerTableTable tableBody')
    teams = dict()
    for table in tableSubHead:
        team_name = table.find('tr', class_=re.compile("playerTableBgRowHead")).get_text()
        players = [stuff.get_text()[:stuff.get_text().find(',')].replace('.', '').replace('*','') for stuff in table.find_all('td', class_=re.compile('playertablePlayerName')) ]
        teams[team_name] = players
    return teams

def get_all_teams_stats():
    '''
    Get team stats for each team from ESPN
    '''
    url = 'http://games.espn.com/fba/scoreboard?leagueId=204515&seasonId=2018'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    teams = []
    tableSubHead = soup.find_all('tr', class_='tableSubHead')
    tableSubHead = tableSubHead[0]
    listCats = tableSubHead.find_all('th')
    categories = []
    for cat in listCats:
        if 'title' in cat.attrs:
            categories.append(cat.string)
    rows = soup.findAll('tr', {'class': 'linescoreTeamRow'})

    # Creates a 2-D matrix which resembles the Season Stats table.
    for row in range(len(rows)):
        team_row = []
        columns = rows[row].findAll('td')[:(2 + len(categories))]
        for column in columns:
            team_row.append(column.getText())
        teams.append(team_row)
    return teams, categories

def get_player_universe():
    '''
    Get players on my team and free agents 
    with relevant stats for fantasy league scoring
    '''
    free_agents = get_players_data('freeagency')
    my_team = get_players_data('clubhouse')
    all_avail_players = free_agents.append(my_team)
    return all_avail_players




# weekly_rankings, weekly_matchups, weekly_analysis = computeStats(teams, categories, seasonData)
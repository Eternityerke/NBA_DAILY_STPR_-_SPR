import time

import numpy as np
import pandas as pd

from dateutil.rrule import rrule, DAILY
from datetime import datetime

from nba_stats_tracking import tracking
from nba_stats_tracking import utils

def get_boxscore_response_json_for_stat_measure(measure_type, season, season_type, **kwargs):
    """    
    season - string, ex '2019-20'
    season_type - string, 'Regular Season' or 'Playoffs'

    possible kwargs:
    date_from - string, optional, format - MM/DD/YYYY
    date_to - string, optional, format - MM/DD/YYYY

    returns dict
    """
    url = 'https://stats.nba.com/stats/leaguedashplayerstats'

    parameters = {
        'College' : '', 
        'Conference': '',
        'Country' : '',
        'DateFrom': kwargs.get('date_from', ''),
        'DateTo': kwargs.get('date_to', ''),
        'Division' : '',
        'DraftPick' : '',
        'DraftYear' : '',
        'GameScope' : '',
        'GameSegment' : '',
        'Height' : '',
        'LastNGames' : 0,
        'LeagueID' : '00',
        'Location' : '',
        'MeasureType' : measure_type,
        'Month' : 0,
        'OpponentTeamID' : 0,
        'Outcome' : '' ,
        'PORound' : 0,
        'PaceAdjust' : 'N',
        'PerMode' : 'Totals',
        'Period' : 0,
        'PlayerExperience' : '',
        'PlayerPosition' : '',
        'PlusMinus' : 'N',
        'Rank' : 'N',
        'Season': season,
        'SeasonSegment': '',
        'SeasonType': season_type,
        'ShotClockRange' : '',
        'StarterBench' : '',
        'TeamID' : 0,
        'TwoWay' : 0,
        'VsConference': '',
        'VsDivision': '',
        'Weight' : '',
    }

    return utils.get_json_response(url, parameters)



def generate_boxscore_game_logs(measure_type, date_from, date_to):
    """
    date_from - string, format - MM/DD/YYYY
    date_to - string, format - MM/DD/YYYY

    returns list of dicts
    """
    start_date = datetime.strptime(date_from, '%m/%d/%Y')
    end_date = datetime.strptime(date_to, '%m/%d/%Y')
    game_logs = []
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        date = dt.strftime('%m/%d/%Y')
        team_id_game_id_map, team_id_opponent_team_id_map = utils.get_team_id_maps_for_date(date)
        if len(team_id_game_id_map.values()) == 0:
            return game_logs

        date_game_id = list(team_id_game_id_map.values())[0]

        season = utils.get_season_from_game_id(date_game_id)
        season_type = utils.get_season_type_from_game_id(date_game_id)

        boxscore_game_logs = get_boxscore_stats(measure_type, [season], [season_type], date_from=date, date_to=date)

        player_id_team_id_map = utils.get_player_team_map_for_date(date)
        for game_log in boxscore_game_logs:
            game_log['TEAM_ID'] = player_id_team_id_map[game_log['PLAYER_ID']]
        game_logs += boxscore_game_logs
    return game_logs


def get_boxscore_stats(measure_type, seasons, season_types, **kwargs):
    """    
    seasons - list, ex season '2019-20'
    season_types - list, season types are 'Regular Season' or 'Playoffs'

    possible kwargs:
    date_from - string, optional, format - MM/DD/YYYY
    date_to - string, optional, format - MM/DD/YYYY

    returns list of dicts
    """
    all_season_stats = []
    for season in seasons:
        for season_type in season_types:
            time.sleep(2)
            response_json = get_boxscore_response_json_for_stat_measure(measure_type, season, season_type, **kwargs)
            stats = utils.make_array_of_dicts_from_response_json(response_json, 0)
            for stat in stats:
                stat['SEASON'] = f'{season} {season_type}'
            all_season_stats += stats
    return all_season_stats


def get_hustle_response_json_for_stat_measure(season, season_type, **kwargs):
    """    
    season - string, ex '2019-20'
    season_type - string, 'Regular Season' or 'Playoffs'

    possible kwargs:
    date_from - string, optional, format - MM/DD/YYYY
    date_to - string, optional, format - MM/DD/YYYY

    returns dict
    """
    url = 'https://stats.nba.com/stats/leaguehustlestatsplayer'

    parameters = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': kwargs.get('date_from', ''),
        'DateTo': kwargs.get('date_to', ''),
        'GameScope': '',
        'LastNGames': 0,
        'LeagueID': '00',
        'Location': '',
        'Month': 0,
        'OpponentTeamID': 0,
        'Outcome': '',
        'PerMode': 'Totals',
        'PlayerExperience': '',
        'PlayerPosition': '',
        'SeasonSegment': '',
        'StarterBench': '',
        'VsConference': '',
        'VsDivision': '',
    }

    return utils.get_json_response(url, parameters)


def generate_hustle_game_logs(date_from, date_to):
    """
    date_from - string, format - MM/DD/YYYY
    date_to - string, format - MM/DD/YYYY

    returns list of dicts
    """
    start_date = datetime.strptime(date_from, '%m/%d/%Y')
    end_date = datetime.strptime(date_to, '%m/%d/%Y')
    game_logs = []
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        date = dt.strftime('%m/%d/%Y')
        team_id_game_id_map, team_id_opponent_team_id_map = utils.get_team_id_maps_for_date(date)
        if len(team_id_game_id_map.values()) == 0:
            return game_logs

        date_game_id = list(team_id_game_id_map.values())[0]

        season = utils.get_season_from_game_id(date_game_id)
        season_type = utils.get_season_type_from_game_id(date_game_id)

        hustle_game_logs = get_hustle_stats([season], [season_type], date_from=date, date_to=date)

        player_id_team_id_map = utils.get_player_team_map_for_date(date)
        for game_log in hustle_game_logs:
            game_log['TEAM_ID'] = player_id_team_id_map[game_log['PLAYER_ID']]
        game_logs += hustle_game_logs
    return game_logs


def get_hustle_stats(seasons, season_types, **kwargs):
    """    
    seasons - list, ex season '2019-20'
    season_types - list, season types are 'Regular Season' or 'Playoffs'

    possible kwargs:
    date_from - string, optional, format - MM/DD/YYYY
    date_to - string, optional, format - MM/DD/YYYY

    returns list of dicts
    """
    all_season_stats = []
    for season in seasons:
        for season_type in season_types:
            time.sleep(2)
            response_json = get_hustle_response_json_for_stat_measure(season, season_type, **kwargs)
            stats = utils.make_array_of_dicts_from_response_json(response_json, 0)
            for stat in stats:
                stat['SEASON'] = f'{season} {season_type}'
            all_season_stats += stats
    return all_season_stats


"""
Above are all functions.
Please input the date at below.

"""

entity_type = 'player'
date_from = '03/07/2020'
date_to = '03/07/2020'
Drives = Defense = CatchShoot = Passing = Possessions = PullUpShot = Efficiency = Hustle = Base = Advanced = pd.DataFrame()

"""
Mad to design the loop,
so the process will be an easy linear step.

"""

stat_measure = 'Drives'
game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
for game_log in game_logs:
    Drives = Drives.append(game_log, ignore_index = True)

stat_measure = 'Defense'
game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
for game_log in game_logs:
    Defense = Defense.append(game_log, ignore_index = True)

stat_measure = 'CatchShoot'
game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
for game_log in game_logs:
    CatchShoot = CatchShoot.append(game_log, ignore_index = True)

stat_measure = 'Passing'
game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
for game_log in game_logs:
    Passing = Passing.append(game_log, ignore_index = True)

stat_measure = 'Possessions'
game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
for game_log in game_logs:
    Possessions = Possessions.append(game_log, ignore_index = True)

stat_measure = 'PullUpShot'
game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
for game_log in game_logs:
    PullUpShot = PullUpShot.append(game_log, ignore_index = True)

stat_measure = 'Efficiency'
game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
for game_log in game_logs:
    Efficiency = Efficiency.append(game_log, ignore_index = True)

game_logs = generate_hustle_game_logs(date_from, date_to)
for game_log in game_logs:
    Hustle = Hustle.append(game_log, ignore_index = True)

measure_type = 'Base'
game_logs = generate_boxscore_game_logs(measure_type, date_from, date_to)
for game_log in game_logs:
    Base = Base.append(game_log, ignore_index = True)

measure_type = 'Advanced'
game_logs = generate_boxscore_game_logs(measure_type, date_from, date_to)
for game_log in game_logs:
    Advanced = Advanced.append(game_log, ignore_index = True)
    
m = ['PLAYER_ID','PLAYER_NAME','SEASON','TEAM_ABBREVIATION','TEAM_ID','GAME_ID','OPPONENT_TEAM_ID']
n = ['PLAYER_ID','PLAYER_NAME','SEASON','TEAM_ABBREVIATION','TEAM_ID']
a = pd.merge(Drives, Defense, how='left', on= m , suffixes = ('_x','_y'))
b = pd.merge(a, CatchShoot, how='left', on= m , suffixes = ('_x','_y'))
c = pd.merge(b, Passing, how='left', on= m , suffixes = ('_x','_y'))
d = pd.merge(c, Possessions, how='left', on= m , suffixes = ('_x','_y'))
e = pd.merge(d, PullUpShot, how='left', on= m , suffixes = ('_x','_y'))
f = pd.merge(e, Efficiency, how='left', on= m , suffixes = ('_x','_y'))
g = pd.merge(f, Hustle, how='left', on= n , suffixes = ('_x','_y'))
h = pd.merge(Base, Advanced, how='left', on= n , suffixes = ('_ic','_c'))
df = pd.merge(g, h, how='left', on= n , suffixes = ('_x','_y'))
df.to_csv('1.csv',index = True)

staff = ['PLAYER_NAME',
     'TEAM_ABBREVIATION',
     'DRIVES',
     'DRIVE_PASSES',
     'PULL_UP_FGA',
     'CATCH_SHOOT_FGA',
     'ELBOW_TOUCHES',
     'POST_TOUCHES',
     'PAINT_TOUCHES',
     'POTENTIAL_AST',
     'PULL_UP_PTS_y',
     'CATCH_SHOOT_PTS_y',
     'DRIVE_PTS_y',
     'PAINT_TOUCH_PTS',
     'POST_TOUCH_PTS',
     'ELBOW_TOUCH_PTS',
     'DEFLECTIONS',
     'SCREEN_ASSISTS',
     'OFF_BOXOUTS',
     'DEF_BOXOUTS' ,
     'FGM_ic',
     'FGA_ic',
     'FTM',
     'FTA',
     'OREB',
     'TOV',
     'PF',
     'PTS',
     'STL_y',
     'BLK_y',
     'DREB_y',
     'DEF_RIM_FGM',
     'DEF_RIM_FGA',
     'FG3A',
     'AST_y',
     'TS_PCT',
     'USG_PCT',
     'PACE',
     'MIN_ic',
     'W_c']

stats = pd.read_csv("./1.csv", usecols=staff)

result = pd.DataFrame()
result['Name'] = stats['PLAYER_NAME']
result['Team'] = stats['TEAM_ABBREVIATION']

stats['rawSTPR'] = stats.apply(lambda x:  0.24 * x['DRIVE_PASSES'] - 0.24 * x['DRIVES']
                                - 0.24 * x['PULL_UP_FGA'] - 0.24 * x['CATCH_SHOOT_FGA']
                                - 0.32 * x['ELBOW_TOUCHES'] - 0.08 * x['POST_TOUCHES']
                                + 0.08 * x['PAINT_TOUCHES'] + 0.32 * x['POTENTIAL_AST']
                                + 0.16 * x['PULL_UP_PTS_y'] - 0.08 * x['CATCH_SHOOT_PTS_y']
                                + 0.16 * x['DRIVE_PTS_y'] - 0.08 * x['PAINT_TOUCH_PTS']
                                + 0.40 * x['POST_TOUCH_PTS'] - 0.32 * x['ELBOW_TOUCH_PTS']
                                + 0.72 * x['DEFLECTIONS'] + 0.16 * x['SCREEN_ASSISTS']
                                + 0.08 * x['OFF_BOXOUTS'] + 0.12 * x['DEF_BOXOUTS']
                                - 0.56 * x['FGM_ic'] - 0.48 * x['FGA_ic']
                                + 2.00 * x['FTM'] - 1.36 * x['FTA']
                                + 0.40 * x['OREB'] - 0.96 * x['TOV']
                                - 0.72 * x['PF'] + 0.80 * x['PTS']
                                + 1.44 * x['STL_y'] + 0.08 * x['BLK_y']
                                + 0.40 * x['DREB_y'] - 2.00 * x['DEF_RIM_FGM'] + 1.04 * x['DEF_RIM_FGA'], axis = 1)

stats['STPR'] = stats.apply(lambda x: x['rawSTPR'] / (x['PACE'] * x['MIN_ic'] / 48) * 100 - 5, axis = 1)

stats['SPR'] = stats.apply(lambda x: x['PTS'] - x['FGA_ic'] + 0.2 * x['FG3A'] - 0.3 * x['FTA']
                            + 0.3 * x['OREB'] + 0.2 * x['DREB_y'] + 0.5 * x['AST_y']
                            + 1.5 * x['STL_y'] + 0.7 * x['BLK_y'] - 1.2 * x['TOV'], axis = 1)

result['MIN'] = stats['MIN_ic']
result['TS'] = stats['TS_PCT']
result['USG'] = stats['USG_PCT']
result['SPR'] = stats['SPR']
result['STPR'] = stats['STPR']
result['w'] = stats['W_c']

cols = ['Name', 'Team', 'MIN', 'TS', 'USG', 'SPR', 'STPR', 'w']
print(result)

result.to_csv("./2.csv", index = False)

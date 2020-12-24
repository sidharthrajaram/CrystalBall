import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
from utils import get_team_data, generate_dataframe


def getTeamDf(team_id, year):
    df_header = get_team_data(team_id, year, header=True)
    df_row = [get_team_data(team_id, year)]
    return generate_dataframe(df_row, df_header)

def team_score(team_id, year):
    df = getTeamDf(team_id, year)
    score = float(0.76*df['ORtg'] - 0.87*df['DRtg'] + df['MOV'] + 10.0*df['2P%'] + 0.66*df['DRB'] + df['SOS'])
    return score

def simulate_game(t1_year, t2_year, t1_id, t2_id, epochs=100000, home_variation_max=100, away_variation_max=100, display_info=False):
    
    if display_info:
        print("Simulation Presets:")
        print("Epochs: {}".format(epochs))
        print("Home Team Variation Range Max: {}".format(home_variation_max))
        print("Away Team Variation Range Max: {}".format(away_variation_max))
        print()

    t1_metric = team_score(t1_id, t1_year)
    t2_metric = team_score(t2_id, t2_year)

    if display_info:
        print('{} has a CORWIN score of {}'.format(t1_id, t1_metric))
        print('{} has a CORWIN score of {}'.format(t2_id, t2_metric))
        print()
    t1_wins = 0
    t2_wins = 0

    for i in range(epochs):
        t1_random_variation = random.randint(0, home_variation_max) / 10  # parameter these
        t2_random_variation = random.randint(0, away_variation_max) / 10   # parameter these
        t1_final_metric = t1_metric + t1_random_variation
        t2_final_metric = t2_metric + t2_random_variation

        if t1_final_metric > t2_final_metric:
            t1_wins +=1
        else:
            t2_wins +=1

    if display_info:
        print('In {} simulated games, {}: {} wins, {}: {} wins'.format(epochs, t1_id, t1_wins, t2_id, t2_wins))
    if t1_wins > t2_wins:
        return t1_year, t1_id, float(t1_wins)/float(epochs/100), t2_year, t2_id
    else:
        return t2_year, t2_id, float(t2_wins)/float(epochs/100), t1_year, t1_id


def simulate(games, year, epochs=100000):
    for game in games:
        win_team_year, win_team_id, win_team_percent, lose_team_year, lose_team_id = simulate_game(year, year, game[0], game[1], epochs=epochs)
        print("{} {} has a {}% chance of beating {} {}.".format(win_team_year, win_team_id, win_team_percent, lose_team_year, lose_team_id))

def test(games, year, results, epochs=100000):
    correct = 0
    for i in range(len(games)):
        game = games[i]
        result = results[i]
        win_team_year, win_team_id, win_team_percent, lose_team_year, lose_team_id = simulate_game(year, year, game[0], game[1], epochs=epochs)
        print("{} {} has a {}% chance of beating {} {}.".format(win_team_year, win_team_id, win_team_percent, lose_team_year, lose_team_id))
        if win_team_id == result:
            correct += 1
    print("Accuracy: {}%".format(100*correct/len(games)))
    return correct/len(games)

if __name__ == "__main__":

    # CORWIN discovery 
    # year = "2020"
    # years = ["2015", "2017", "2020"]
    # teams = ["ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN",
    #             "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
    #             "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO",
    #             "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]
    # frames = []
    # for year in years:
    #     print()
    #     print(year)
    #     for team in teams:
    #         print(team)
    #         frames.append(getTeamDf(team, year))
    # teams = pd.concat(frames, ignore_index=True)
    # teams['PREDICT'] = 0.76*teams['ORtg'] - 0.87*teams['DRtg'] + teams['MOV'] + 0.68*teams['2P%'] + 0.66*teams['DRB'] + teams['SOS']
    # teams = (teams-teams.min())/(teams.max()-teams.min())
    # teams['WINS'] = teams['W']
    # teams = teams.drop('W', 1)
    # teams = teams.drop('L', 1)
    # teams = teams.drop('PW', 1)
    # teams = teams.drop('PL', 1)
    # teams = teams.drop('SRS', 1)
    # teams = teams.drop('MOV', 1)
    # teams = teams.sort_values(by=['WINS'])
    # print(teams)
    # ax = sns.heatmap(teams.corr(), annot=True, vmin=0, vmax=1)
    # plt.show()

    games = [['TOR', 'NOP'], 
            ['LAC', 'LAL'],
            ['CHO', 'CHI'],
            ['IND', 'DET'],
            ['ORL', 'CLE'],
            ['BRK', 'MIN'],
            ['MIA', 'MEM'],
            ['PHI', 'BOS'],
            ['DAL', 'WAS'],
            ['SAS', 'NYK'],
            ['UTA', 'OKC'],
            ['POR', 'DEN'],
            ['PHO', 'SAC'],
            ['DET', 'ATL'],
            ['HOU', 'MIL'],
            ['GSW', 'LAC'],
            ['BOS', 'TOR'],
            ['CHO', 'MIN'],
            ['BRK', 'NYK'],
            ['MEM', 'CHI'],
            ['NOP', 'DAL'],
            ['OKC', 'WAS'],
            ['DEN', 'PHO'],
            ['SAC', 'POR'],
            ['LAL', 'UTA'],]

    results = ['TOR', 'LAC', 'CHO', 'DET', 'ORL', 
                'MIN', 'MIA', 'PHI', 'DAL', 'SAS', 
                'UTA', 'DEN', 'PHO', 'ATL', 'MIL', 
                'LAC', 'BOS', 'MIN', 'BRK', 'CHI',
                'DAL', 'WAS', 'DEN', 'POR', 'LAL']

    # simulate(games, '2020')
    test(games, "2020", results)







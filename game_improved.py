# more efficient, better version of game_basic.py
# will be used to predict game results each day

import random
from playground import get_team_data, generate_dataframe, clean_up_df


def getTeamDf(team_id, year):
    df_header = get_team_data(team_id, year, header=True)
    df_row = [get_team_data(team_id, year)]
    return generate_dataframe(df_row, df_header)


def calculate_metric(team_df):
    team_df = clean_up_df(team_df)

    # scaling, im sure there's a better way to do this, later...
    pts = team_df['PTS'][0] / 120.0
    tov = team_df['TOV'][0] / 17.0
    efg = 2 * team_df['eFG%_0'][0] / 0.570  # key
    efg_opp = 2 * team_df['eFG%_1'][0] / 0.570  # key
    ftr = team_df['FTr'][0] / 0.315
    orb = team_df['ORB'][0] / 13.0
    drb = team_df['DRB'][0] / 40.0
    mov = 2 * team_df['MOV'][0] / 9.0   # key
    ast = team_df['AST'][0] / 30.0
    blk = team_df['BLK'][0] / 7.0
    ortg = 2 * team_df['ORtg'][0] / 116.0   # key
    drtg = team_df['DRtg'][0] / 116.0

    team_metric = pts - tov + efg - efg_opp + ftr + orb + drb + mov + ast + blk + ortg - drtg
    return team_metric


def get_team_metric(team_id, year):
    return calculate_metric(getTeamDf(team_id, year))


# t1 is home team, t2 is away team, year parameters are strings
def simulate(t1_year, t2_year, t1_id, t2_id, epochs=1000, home_variation_max=100, away_variation_max=85):
    print("Simulation Presets:")
    print("Epochs: {}".format(epochs))
    print("Home Team Variation Range Max: {}".format(home_variation_max))
    print("Away Team Variation Range Max: {}".format(away_variation_max))
    print()

    t1_metric = get_team_metric(t1_id, t1_year)
    t2_metric = get_team_metric(t2_id, t2_year)

    print('{} has a pure game metric of {}'.format(t1_id, t1_metric))
    print('{} has a pure game metric of {}'.format(t2_id, t2_metric))
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

    print('In {} simulated games, {}: {} wins, {}: {} wins'.format(epochs, t1_id, t1_wins, t2_id, t2_wins))
    if t1_wins > t2_wins:
        return t1_year, t1_id, float(t1_wins)/float(epochs/100)
    else:
        return t2_year, t2_id, float(t2_wins)/float(epochs/100)


if __name__ == '__main__':

    t1_year = input("Year of Home Team: ")
    t1_id = input("ID of Home Team: ")
    t2_year = input("Year of Away Team: ")
    t2_id = input("ID of Away Team: ")
    print()
    win_team_year, win_team_id, win_team_percent = simulate(t1_year, t2_year, t1_id, t2_id)
    print()
    print("The {} {} team has a {}% chance of winning.".format(win_team_year, win_team_id, win_team_percent))





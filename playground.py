import pandas as pd
import numpy as np

from team_scraper import getTeamStats


# return arrays of length 42
def get_team_data(team_id, header=False):
    team_stats_tuple = getTeamStats(team_id)

    regular_stats_raw = np.array(team_stats_tuple[0].iloc[1,2:])
    regular_stats = list(map(lambda value: float(value), regular_stats_raw))
    regular_stats_header = team_stats_tuple[1][2:]

    advanced_stats = np.array(team_stats_tuple[2].iloc[0, 1:-2])
    advanced_stats_header_raw = team_stats_tuple[3][1:-2]
    advanced_stats_header = list(map(lambda tuple: tuple[1], advanced_stats_header_raw))

    stats_full = np.concatenate((regular_stats, advanced_stats), axis=None)
    header_full = np.concatenate((regular_stats_header, advanced_stats_header), axis=None)

    if header == True:
        return header_full
    else:
        return stats_full


def get_all_teams_data(teams):
    team_stats_array = []
    for team in teams:
        team_stats = get_team_data(team)
        team_stats_array.append(team_stats)
        # print(team_stats)
        # print(len(team_stats))
        # print()
    return team_stats_array


def generate_dataframe(rows, header):
    df = pd.DataFrame(rows, columns=header)
    return df


def generate_teams_training_data(teams, header):
    all_teams_data = get_all_teams_data(teams)
    training_df = generate_dataframe(all_teams_data, header)
    return training_df


def feature_scaled_df(df):
    for column in df:
        print(df[column])
        # df[column] = df[column].apply(lambda x: x/df[column].max())
        # print("Max {}: {}".format(column, df[column].max()))
    # return df


def predict(X, W):
    return np.dot(X, W.T)


def train(X, Y, epochs, l_rate):
    W = np.zeros(X.shape[1])
    m = X.shape[0]
    for epoch in range(epochs):
        h = predict(X, W)
        loss = h - Y
        error = np.sum(loss ** 2) / (2*m)
        print("Epoch {}, Error: {}".format(epoch, error))
        gradient = np.dot(X.T, loss) / m
        W_delta = l_rate * gradient
        W -= W_delta
    return W




if __name__ == '__main__':

    # set up
    FORECAST_FILE = 'data/teams_test.csv'
    teams_df = pd.read_csv(FORECAST_FILE)
    teams = np.array(teams_df["Team"])
    stat_header = get_team_data('POR', header=True)

    training_df = generate_teams_training_data(teams, stat_header)
    # print(training_df)
    # print()

    # clean df's
    Y_df = training_df['W']
    X_df = training_df[['PTS','TOV','eFG%','FTr','ORB','DRB','MOV','ORtg','DRtg','AST','BLK']]
    X_df.drop(X_df.columns[[3]], axis=1, inplace=True)

    print(X_df)
    print()
    print(Y_df)
    print()
    feature_scaled_df(X_df)


    # weights = train(X, Y, 1000, 0.01)



    # FORECAST_FILE = 'data/teams.csv'
    # teams_df = pd.read_csv(FORECAST_FILE)
    # teams_df['EFG'] = (teams_df['FG'] + 0.5 * teams_df['3P']) / teams_df['FGA']
    # teams_df['ASTOV'] = teams_df['AST'] / teams_df['TOV'] / 2
    # teams_df['BLK2'] = teams_df['BLK'] / 400
    #
    # print(teams_df)
    #
    # X = np.array(teams_df.iloc[:, 25:])
    # Y = np.array(teams_df['WINS'])
    #
    # weights = train(X, 50000, 0.1)
    # print()
    # #
    # milwaukee = np.array([0.53805422, 0.86008065, 1.2075])
    # washington = np.array([0.53079735, 0.93327556, 0.9475])
    #
    # print(predict(milwaukee, weights))
    # print(predict(washington, weights))


# this was done to play around with regression ...
# helped me determine which stats have great correlation with wins
# ill tweak it a bit once the season starts, think i can predict total season wins based on a few games of performance.
import pandas as pd
import numpy as np

from team_scraper import getTeamStats


# return arrays of length 42
def get_team_data(team_id, year, header=False):
    team_stats_tuple = getTeamStats(team_id, year)

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


def get_all_teams_data(teams, year):
    team_stats_array = []
    for team in teams:
        team_stats = get_team_data(team, year)
        team_stats_array.append(team_stats)
    return team_stats_array


def generate_dataframe(rows, header):
    df = pd.DataFrame(rows, columns=header)
    return df


def generate_teams_training_data(teams, header, year):
    all_teams_data = get_all_teams_data(teams, year)
    training_df = generate_dataframe(all_teams_data, header)
    return training_df


def clean_up_df(df):
    cols = []
    efg_count = 0
    tov_count = 0
    ftfga_count = 0
    for column in df.columns:
        if column == 'eFG%':
            cols.append('eFG%_' + str(efg_count))
            efg_count += 1
            continue
        if column == 'TOV%':
            cols.append('TOV%_' + str(tov_count))
            tov_count += 1
            continue
        if column == 'FT/FGA':
            cols.append('FT/FGA_' + str(ftfga_count))
            ftfga_count += 1
            continue
        cols.append(column)
    df.columns = cols
    return df


def feature_scaled_df(df):
    for column in df:
        df[column] = df[column].apply(lambda x: x/df[column].max())
    return df


def predict(X, W):
    return np.dot(X, W.T)


def train(X, Y, epochs, l_rate):
    W = np.zeros(X.shape[1])
    m = X.shape[0]
    for epoch in range(epochs):
        h = predict(X, W)
        loss = h - Y
        error = np.sum(loss ** 2) / (2*m)
        if epoch%1000 == 0 or epoch+1 == epochs:
            print("Epoch {}, Error: {}".format(epoch, error))
        gradient = np.dot(X.T, loss) / m
        W_delta = l_rate * gradient
        W -= W_delta
    return W


def predictWins(weights, X):
    predictions = predict(X, weights)
    # print(predictions)
    return predictions


if __name__ == '__main__':

    # set up
    FORECAST_FILE = 'data/teams_test.csv'
    teams_df = pd.read_csv(FORECAST_FILE)
    all_teams = np.array(teams_df["Team"])
    stat_header = get_team_data('POR', '2019', header=True)

    train_test_division = 70

    full_df_2019 = generate_teams_training_data(all_teams, stat_header, '2019')
    full_df_2018 = generate_teams_training_data(all_teams, stat_header, '2018')
    full_df_2017 = generate_teams_training_data(all_teams, stat_header, '2017')

    years_dfs = [full_df_2019, full_df_2018, full_df_2017]
    full_df = pd.concat(years_dfs, ignore_index=True)
    # print(full_df)
    # print()

    Y_df = full_df[['W']]
    max_wins = np.amax(np.array(Y_df))
    X_df = full_df[['PTS','TOV','eFG%','FTr','ORB','DRB','MOV','ORtg','DRtg','AST','BLK']]
    X_df = clean_up_df(X_df)

    # print(X_df)
    # print()
    # print(Y_df)

    # everything scaled
    scaled_X_df = feature_scaled_df(X_df)
    scaled_Y_df = feature_scaled_df(Y_df)


    training_X_data = scaled_X_df.iloc[:train_test_division,:]
    training_Y_data = scaled_Y_df.iloc[:train_test_division,:]
    # training_team_names = all_teams[:train_test_division]

    test_X_data = scaled_X_df.iloc[train_test_division:,:]
    test_Y_data = scaled_Y_df.iloc[train_test_division:,:]
    # test_team_names = all_teams[train_test_division:]

    print("TRAINING DATA")
    print(training_X_data)
    print()
    print(training_Y_data)
    print()
    #
    # print("TESTING DATA")
    # print(test_X_data)
    # print()
    # print(test_Y_data)
    # print()

    X = np.array(training_X_data)
    Y = np.ravel(np.array(training_Y_data))

    input("Press enter to train weights")
    print()

    # training
    alpha = 0.20
    epochs = 200000
    weights = train(X, Y, epochs, alpha)


    # testing
    print()
    print(weights)
    print()

    test_X = np.array(test_X_data)
    test_Y = np.ravel(np.array(test_Y_data))

    predictions = predictWins(weights, test_X)
    for i in range(len(predictions)):
        print("{} wins".format(predictions[i]*max_wins))


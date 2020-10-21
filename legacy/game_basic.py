from team_scraper import getTeamStats
import random

def getTeamMetric(team_1_df):
    t1_ft_ratio = float(team_1_df['FT'][0]) / float(team_1_df['FGA'][0])
    t1_efg = (float(team_1_df['FG'][0]) + 0.5 * float(team_1_df['3P'][0])) / float(team_1_df['FGA'][0])
    t1_orbpg = float(team_1_df['ORB'][1]) / 100  # per game
    t1_apg = float(team_1_df['AST'][1]) / 300  # per game
    t1_metric = t1_ft_ratio + t1_efg + t1_orbpg + t1_apg
    return t1_metric

# home team, away team
# returns winning team's info
def simulate(t1_name, t2_name, t1_metric, t2_metric):
    t1_wins = 0
    t2_wins = 0
    count = 0

    while count <= 1000:

        t1_randomness = random.randint(0, 100) / 400  # home team
        t2_randomness = random.randint(0, 75) / 400  # away team

        t1_final = t1_metric + t1_randomness
        t2_final = t2_metric + t2_randomness

        if t1_final > t2_final:
            t1_wins +=1
            # print('{} beats {}'.format(team_1, team_2))
        else:
            t2_wins +=1
            # print('{} beats {}'.format(team_2, team_1))

        # print('{}: {}, {}: {}'.format(t1_name, t1_wins, t2_name, t2_wins))
        count += 1

    if t1_wins > t2_wins:
        return t1_name, t1_wins
    else:
        return t2_name, t2_wins

if __name__ == "__main__":

    team_1 = input('Home Team: ')
    team_2 = input('Away Team: ')

    team_1_stats = getTeamStats(team_1)
    team_2_stats = getTeamStats(team_2)

    team_1_df = team_1_stats[0]
    team_2_df = team_2_stats[0]

    t1_metric = getTeamMetric(team_1_df)
    t2_metric = getTeamMetric(team_2_df)

    # print('{} has the following four factors: FT/FTA: {}, eFG%: {}, ORPG(scaled): {}, APG(scaled): {}'.format(
    #     team_2, t2_ft_ratio, t2_efg, t2_orbpg, t2_apg))
    # print()

    print('{} has a pure game metric of {}'.format(team_1, t1_metric))
    print('{} has a pure game metric of {}'.format(team_2, t2_metric))
    print()

    winning_team_info = simulate(team_1, team_2, t1_metric, t2_metric)
    winning_team = winning_team_info[0]
    winning_prob = float(winning_team_info[1])/10.0
    print('{}% chance of {} winning.'.format(winning_prob, winning_team))





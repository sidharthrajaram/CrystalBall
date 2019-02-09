from team_scraper import getTeamStats
import random


team_1 = 'BOS'
team_2 = 'PHI'

team_1_stats = getTeamStats(team_1)
team_2_stats = getTeamStats(team_2)

team_1_df = team_1_stats[0]
team_2_df = team_2_stats[0]

#team 1
t1_ft_ratio = float(team_1_df['FT'][0])/float(team_1_df['FGA'][0])
t1_efg = ( float(team_1_df['FG'][0]) + 0.5*float(team_1_df['3P'][0]) ) / float(team_1_df['FGA'][0])
t1_orbpg = float(team_1_df['ORB'][1])/100  # per game
t1_apg = float(team_1_df['AST'][1])/300  # per game
t1_metric = t1_ft_ratio + t1_efg + t1_orbpg + t1_apg

# print('{} has the following four factors: FT/FTA: {}, eFG%: {}, ORPG(scaled): {}, APG(scaled): {}'.format(
#     team_1, t1_ft_ratio, t1_efg, t1_orbpg, t1_apg))
# print()

#team 1
t2_ft_ratio = float(team_2_df['FT'][0])/float(team_2_df['FGA'][0])
t2_efg = ( float(team_2_df['FG'][0]) + 0.5*float(team_2_df['3P'][0]) ) / float(team_2_df['FGA'][0])
t2_orbpg = float(team_2_df['ORB'][1])/100  # per game
t2_apg = float(team_2_df['AST'][1])/300  # per game
t2_metric = t2_ft_ratio + t2_efg + t2_orbpg + t2_apg

# print('{} has the following four factors: FT/FTA: {}, eFG%: {}, ORPG(scaled): {}, APG(scaled): {}'.format(
#     team_2, t2_ft_ratio, t2_efg, t2_orbpg, t2_apg))
# print()

# print('{} has a pure game metric of {}'.format(team_1, t1_metric))
# print('{} has a pure game metric of {}'.format(team_2, t2_metric))
# print()

t1_randomness = random.randint(0,100)/400  # home team
t2_randomness = random.randint(0,75)/400  # away team

t1_final = t1_metric + t1_randomness
t2_final = t2_metric + t2_randomness

print('{} is the home team and has a game metric of {}.'.format(team_1, t1_final))
print('{} is the away team and has a game metric of {}'.format(team_2, t2_final))
print()

if t1_final > t2_final:
    print('{} beats {}'.format(team_1, team_2))
else:
    print('{} beats {}'.format(team_2, team_1))

print()



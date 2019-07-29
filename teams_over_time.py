import matplotlib.pyplot as plt
import numpy as np
from game_improved import get_team_metric


# has to be equal/over 1980
def get_years(year, year_range=2):
    year_int = int(year)
    year_array = [year]

    #0,1,2
    for i in range(1, year_range+1):
        year_array.append(str(year_int+i))
        year_array.insert(0, str(year_int-i))
    return year_array


def pure_game_metric(team_id, year, year_range=2):
    years = get_years(year, year_range)
    yearly_pgms = []
    for year_i in years:
        pgm = get_team_metric(team_id, year_i)
        yearly_pgms.append([int(year_i), pgm])
        print("{} {}: {}".format(year_i, team_id, pgm))
    return yearly_pgms  # [[year(int), pgm], ...]


def get_x_y(tuple):
    x = list(map(lambda x_and_y: x_and_y[0], tuple))
    y = list(map(lambda x_and_y: x_and_y[1], tuple))
    return x, y


# team_tuple = [['GSW','2016'], ['GSW','2016'], ['GSW','2016'], ... ]
def plot_multiple_teams(team_tuples, same_range=False, year_range=2):
    multiple_teams_pgms = []

    # tuple = [team_id, year(str)]
    for tuple in team_tuples:
        multiple_teams_pgms.append([pure_game_metric(tuple[0], tuple[1], year_range), tuple])
        print()

    # team_pgms = [ [tuples of year(int) and corresponding pgm], [team_id, year(str)] ]
    for team_pgms in multiple_teams_pgms:
        x = []
        x, y = get_x_y(team_pgms[0])

        if same_range:
            x = np.arange(1,2*year_range+2)
        legend_years = "{} - {}".format(int(team_pgms[1][1])-year_range, int(team_pgms[1][1])+year_range)
        plt.plot(x, y, marker='o', markerfacecolor='purple', markersize=4, linewidth=2, label="{} {}".format(legend_years, team_pgms[1][0]))

    if same_range:
        plt.axis([0, 2*year_range+2, 0, 100])
    else:
        plt.axis([1980, 2020, 0, 100])

    plt.title("Teams' Pure Game Rating (PGR) Over {} Years".format(2*year_range+1))
    plt.legend()
    plt.show()


if __name__ == '__main__':

    the_goat_teams = [ ['GSW','2016'], ['CHI','1996'], ['LAL','1987'], ['BOS','1986'], ['LAL','2002'] ]
    top_three_teams = [ ['GSW','2017'], ['CHI','1996'], ['LAL','1987'] ]
    interesting_teams = [ ['CHI','1996'], ['CLE', '2016'] ]


    plot_multiple_teams(top_three_teams, same_range=True, year_range=2)

    # print(get_years('2016',year_range=3))

    # all advanced stats become fully available 1980 onwards
    # print("THE BEST:")
    # print("2001 LAL: {}".format(get_team_metric('LAL','2001')))
    # print("1996 CHI: {}".format(get_team_metric('CHI','1996')))
    # print("1986 BOS: {}".format(get_team_metric('BOS','1986')))
    # print("1987 LAL: {}".format(get_team_metric('LAL','1987')))
    # print("1997 CHI: {}".format(get_team_metric('CHI', '1997')))
    # print()
    # print("THE WORST:")
    # print("2005 ATL: {}".format(get_team_metric('ATL', '2005')))
    # print("1987 LAC: {}".format(get_team_metric('LAC', '1987')))
    # print("1998 DEN: {}".format(get_team_metric('DEN', '1998')))
    # print("2012 CHA: {}".format(get_team_metric('CHA', '2012')))

    #
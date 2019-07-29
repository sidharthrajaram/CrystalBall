import matplotlib.pyplot as plt
from game_improved import get_team_metric


if __name__ == '__main__':


    # all advanced stats become fully available 1980 onwards
    print()
    print("THE BEST:")
    print("2017 GSW: {}".format(get_team_metric('GSW','2017')))
    print("1996 CHI: {}".format(get_team_metric('CHI','1996')))
    print("1986 BOS: {}".format(get_team_metric('BOS','1986')))
    print("1987 LAL: {}".format(get_team_metric('LAL','1987')))
    print("1997 CHI: {}".format(get_team_metric('CHI', '1997')))
    print()
    print("THE WORST:")
    print("2005 ATL: {}".format(get_team_metric('ATL', '2005')))
    print("1987 LAC: {}".format(get_team_metric('LAC', '1987')))
    print("1998 DEN: {}".format(get_team_metric('DEN', '1998')))
    print("2012 CHA: {}".format(get_team_metric('CHA', '2012')))


    # plt.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 10], 'ro')
    #
    # plt.axis([0, 6, 0, 10])
    # plt.show()
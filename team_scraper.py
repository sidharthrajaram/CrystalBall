import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib.request



def getTeamStats(team_id):
    team = team_id.upper()
    url = "https://www.basketball-reference.com/teams/" + team + "/2019.html"
    # print(url)
    # print()

    with urllib.request.urlopen(url) as response:
        # UTF-8 doesn't support some initial character on the websites for some reason!
        r = response.read().decode('latin-1')

    content = re.sub(r'(?m)^\<!--.*\n?', '', r)
    content = re.sub(r'(?m)^\-->.*\n?', '', content)

    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.findAll('table')

    test_df = pd.read_html(str(tables[3]))[0]

    if len(test_df.index) != 8:
        stats_table = tables[2]
        misc_table = tables[3]
    else:
        stats_table = tables[3]
        misc_table = tables[4]

    stats_df = pd.read_html(str(stats_table))[0]
    misc_df = pd.read_html(str(misc_table))[0]

    stats_header = stats_df.columns.values.tolist()
    misc_header = misc_df.columns.values.tolist()

    return stats_df, stats_header, misc_df, misc_header

if __name__ == "__main__":
    stuff = getTeamStats('POR')
    print(stuff[0])



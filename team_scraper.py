import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib.request

# retrieves table data and headers for a given nba team for a given year
def getTeamStats(team_id, year):
    team = team_id.upper()
    url = "https://www.basketball-reference.com/teams/" + team + "/" + year + ".html"
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

    if len(test_df.index) == 2:
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
    stuff = getTeamStats('GSW', '2020')
    print(stuff[2])



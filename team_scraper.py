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
    
    stats_index = 2
    misc_index = 3
    for i in range(len(tables)):
        if len(pd.read_html(str(tables[i]))[0].index) == 8:
            stats_index = i
            misc_index = i+1
    
    print(len(pd.read_html(str(tables[stats_index]))[0].index))
    stats_table = tables[stats_index]
    misc_table = tables[misc_index]

    stats_df = pd.read_html(str(stats_table))[0]
    misc_df = pd.read_html(str(misc_table))[0]

    stats_header = stats_df.columns.values.tolist()
    misc_header = misc_df.columns.values.tolist()

    return stats_df, stats_header, misc_df, misc_header

if __name__ == "__main__":
    stuff = getTeamStats('GSW', '2020')
    print(stuff[2])



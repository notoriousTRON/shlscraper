import requests
from bs4 import BeautifulSoup
import json

def get_smjhl_players(url_file):
    """use the urls provided in the json to get each player's information"""
    url_list = get_roster_url(url_file, 'SMJHL')
    for team in url_list:
        print(team)

def get_roster_url(url_file, league):
    """Get the roster URLs for the specified league"""
    return_list = []
    with open(url_file, 'r') as rf:
        data = json.load(rf)
        for team in data['Team Roster URLs'][league]:  # go through the json and get the urls for each roster
            return_list.append((team, data['Team Roster URLs'][league][team]))  # add tuple of team name and url to list
    return return_list

def main():
    """main"""
    url_file = "roster_urls.json"
    get_smjhl_players(url_file)

main()

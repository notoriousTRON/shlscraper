import requests, json, csv
from bs4 import BeautifulSoup


def get_smjhl_players(url_file, smjhl_players_csv):
    """use the urls provided in the json to get each player's information"""
    team_url_list = get_roster_url(url_file, 'SMJHL')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in team_url_list:  # For each team in the list
        pass
        # get each player page URL
        # for each player in player_url_list
        #     player_dict_list = get_player_stats(player)
    # look into using csv dictwriter.writerows() to write the list of dictionaries into the csv file


def get_roster_url(url_file, league):
    """Get the roster URLs for the specified league"""
    return_list = []
    with open(url_file, 'r') as rf:
        data = json.load(rf)
        for team in data['Team Roster URLs'][league]:  # go through the json and get the urls for each roster
            return_list.append((team, data['Team Roster URLs'][league][team]))  # add tuple of team name and url to list
    return return_list


def get_player_urls(team_roster_url):
    """Returns a list of player page URLs from the team roster page"""
    pass


def get_player_stats(name_url):
    """Use the given url to find and get all of the stats. Returns a dictionary"""
    pass


def main():
    """main"""
    url_file = "roster_urls.json"
    smjhl_players_csv = "smjhl_players.csv"
    shl_players_csv = "shl_players.csv"
    get_smjhl_players(url_file, smjhl_players_csv)


main()

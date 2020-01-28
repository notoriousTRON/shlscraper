import requests, json, csv
from bs4 import BeautifulSoup


def get_smjhl_players(url_file, smjhl_players_csv):
    """use the urls provided in the json to get each player's information"""
    team_url_list = get_roster_url(url_file, 'SMJHL')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in team_url_list:  # For each team in the list
        player_url_list = get_player_urls(team[1])  # get each player page URL
        for player in player_url_list:  # for each player in player_url_list
            player_dict_list.append(get_player_stats('https://www.simulationhockey.com/' + player))
    # look into using csv dictwriter.writerows() to write the list of dictionaries into the csv file
    print(player_dict_list)


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
    has_next = True
    page = 1
    return_list = list()
    while has_next:  # this loop ensures that all pages of the roster are hit
        roster_page = requests.get(team_roster_url + '&page=' + str(page))
        soup = BeautifulSoup(roster_page.content, 'html.parser')
        smaller_soup = soup.find_all('tr', 'inline_row')
        for section in smaller_soup:
            a = section.find('a', attrs={'style': 'font-size:14px;'}, href=True)
            return_list.append(a['href'])
        has_next = len(soup.find_all('a', 'pagination_next')) != 0  # check if there is a next page
        if has_next:
            page += 1
    return return_list


def get_player_stats(name_url):
    """Use the given url to find and get all of the stats. Returns a dictionary"""
    player_page = requests.get(name_url)
    soup = BeautifulSoup(player_page.content, 'html.parser')
    post = soup.find_all('div', 'post_body scaleimages')[0]
    print(post.text)  # now I just need to do something with this text data
    return {'word': 'thing'}  # placeholder, obviously


def main():
    """main"""
    url_file = "roster_urls.json"
    smjhl_players_csv = "smjhl_players.csv"
    shl_players_csv = "shl_players.csv"
    get_smjhl_players(url_file, smjhl_players_csv)


main()

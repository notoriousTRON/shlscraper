import requests, json, csv
from bs4 import BeautifulSoup


def get_smjhl_players(url_file, smjhl_players_csv):
    """use the urls provided in the json to get each player's information"""
    team_url_list = get_roster_url(url_file, 'SMJHL')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in team_url_list:  # For each team in the list
        player_url_list = get_player_urls(team[1])  # get each player page URL
        for player in player_url_list:  # for each player in player_url_list
            player_dict_list.append(get_player_stats('https://www.simulationhockey.com/' + player, team[0]))
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


def get_player_stats(name_url, team):
    """Use the given url to find and get all of the stats. Returns a dictionary"""
    player = dict()
    player['Team'] = team
    player_page = requests.get(name_url)
    soup = BeautifulSoup(player_page.content, 'html.parser')
    post = soup.find_all('div', 'post_body scaleimages')[0]
    post_text = post.text.split('\n')  # split the text from the body up into rows for easy iteration
    for line in post_text:
        # why don't switch statements exist in Python???????
        if line.startswith('First Name'):
            player['First Name'] = line.split(': ')[1]  # this gets the first name from the first name line
        elif line.startswith('Last Name'):
            player['Last Name'] = line.split(': ')[1]  # this gets the first name from the last name line
        elif line.startswith('Position'):
            player['Position'] = line.split(': ')[1]  # this gets the player position
        elif line.startswith('Shoots'):
            player['Shoots'] = line.split(': ')[1]  # this gets the player shooting hand
        elif line.startswith('Recruited'):
            player['Recruited by'] = line.split(': ')[1]  # this gets where they were recruited (if applicable)
        elif line.startswith('Player Render'):
            player['Player Render'] = line.split(': ')[1]  # this gets the player render
        elif line.startswith('Jersey Number'):
            player['Jersey Number'] = line.split(': ')[1]  # this gets the player Jersey Number
        elif line.startswith('Height'):
            player['Height'] = line.split(': ')[1]  # this gets the player height
        elif line.startswith('Weight'):
            player['Weight'] = line.split(': ')[1]  # this gets the player weight
        elif line.startswith('Birthplace'):
            player['Birthplace'] = line.split(': ')[1]  # this gets the player birthplace
        elif line.startswith('Player Type'):
            player['Player Type'] = line.split(': ')[1]  # this gets the player type
        elif line.startswith('Strengths'):
            player['Strengths'] = line.split(': ')[1]  # this gets the player strengths
        elif line.startswith('Weakness'):
            player['Weakness'] = line.split(': ')[1]  # this gets the player weakness
        elif line.startswith('Points Available'):
            player['Points Available'] = line.split(': ')[1]  # this gets the amount of points the player has available
        elif line.startswith('CK'):
            player['CK'] = line.split(': ')[1]  # this gets the player Checking
        elif line.startswith('FG'):
            player['FG'] = line.split(': ')[1]  # this gets the player fighting
        elif line.startswith('DI'):
            player['DI'] = line.split(': ')[1]  # this gets the player Discipline
        elif line.startswith('SK'):
            player['SK'] = line.split(': ')[1]  # this gets the player skating
        elif line.startswith('ST'):
            player['ST'] = line.split(': ')[1]  # this gets the player strength
        elif line.startswith('EN'):
            player['EN'] = line.split(': ')[1]  # this gets the player endurance
        elif line.startswith('DU'):
            player['DU'] = line.split(': ')[1]  # this gets the player durability
        elif line.startswith('PH'):
            player['PH'] = line.split(': ')[1]  # this gets the player Puck handling
        elif line.startswith('FO'):
            player['FO'] = line.split(': ')[1]  # this gets the player face off
        elif line.startswith('PA'):
            player['PA'] = line.split(': ')[1]  # this gets the player Passing
        elif line.startswith('SC'):
            player['SC'] = line.split(': ')[1]  # this gets the player scoring
        elif line.startswith('DF'):
            player['DF'] = line.split(': ')[1]  # this gets the player defence
        elif line.startswith('PS'):
            player['PS'] = line.split(': ')[1]  # this gets the player penalty shot
    return player  # return the player


def main():
    """main"""
    url_file = "roster_urls.json"
    smjhl_players_csv = "smjhl_players.csv"
    shl_players_csv = "shl_players.csv"
    get_smjhl_players(url_file, smjhl_players_csv)


main()

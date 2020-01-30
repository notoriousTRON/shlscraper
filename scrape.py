import requests, json, csv, random
from bs4 import BeautifulSoup


user_agent_list = [
   # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def get_smjhl_players(url_file, smjhl_players_csv):
    """use the urls provided in the json to get each player's information"""
    team_url_list = get_roster_url(url_file, 'SMJHL')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in team_url_list:  # For each team in the list
        player_url_list = get_player_urls(team[1])  # get each player page URL
        for player in player_url_list:  # for each player in player_url_list
            player_dict_list.append(get_player_stats('https://www.simulationhockey.com/' + player, team[0]))
    # look into using csv dictwriter.writerows() to write the list of dictionaries into the csv file
    csv_file = "data.csv"
    csv_columns = player_dict_list[0].keys()
    try:
        with open(csv_file, 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in player_dict_list:
                writer.writerow(data)
    except IOError:
        print("I/O error")


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
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}
        roster_page = requests.get(team_roster_url + '&page=' + str(page), headers=headers)
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
    print(team)
    player = dict()
    player['Team'] = team
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    player_page = requests.get(name_url, headers=headers)
    soup = BeautifulSoup(player_page.content, 'html.parser')
    post = soup.find_all('div', 'post_body scaleimages')[0]
    post_text = post.text.split('\n')  # split the text from the body up into rows for easy iteration
    for line in post_text:
        # why don't switch statements exist in Python???????
        if line.startswith('First Name'):
            try:
                player['First Name'] = line.split(':')[1].strip()  # this gets the first name from the first name line
            except:
                player['First Name'] = ''
        elif line.startswith('Last Name'):
            try:
                player['Last Name'] = line.split(':')[1].strip()  # this gets the first name from the last name line
            except:
                player['Last Name'] = ''
        elif line.startswith('Position'):
            try:
                player['Position'] = line.split(':')[1].strip()  # this gets the player position
            except:
                player['Position'] = ''
        elif line.startswith('Shoots'):
            try:
                player['Shoots'] = line.split(':')[1].strip()  # this gets the player shooting hand
            except:
                player['Shoots'] = ''
        elif line.startswith('Recruited'):
            try:
                player['Recruited by'] = line.split(':')[1].strip()  # this gets where they were recruited (if applicable)
            except:
                player['Recruited by'] = ''
        elif line.startswith('Player Render'):
            try:
                player['Player Render'] = line.split(':')[1].strip()  # this gets the player render
            except:
                player['Player Render'] = ''
        elif line.startswith('Jersey Number'):
            try:
                player['Jersey Number'] = line.split(':')[1].strip()  # this gets the player Jersey Number
            except:
                player['Jersey Number'] = ''
        elif line.startswith('Height'):
            try:
                player['Height'] = line.split(':')[1].strip()  # this gets the player height
            except:
                player['Height'] = ''
        elif line.startswith('Weight'):
            try:
                player['Weight'] = line.split(':')[1].strip()  # this gets the player weight
            except:
                player['Weight'] = ''
        elif line.startswith('Birthplace'):
            try:
                player['Birthplace'] = line.split(':')[1].strip()  # this gets the player birthplace
            except:
                player['Birthplace'] = ''
        elif line.startswith('Player Type'):
            try:
                player['Player Type'] = line.split(':')[1].strip()  # this gets the player type
            except:
                player['Player Type'] = ''
        elif line.startswith('Strengths'):
            try:
                player['Strengths'] = line.split(':')[1].strip()  # this gets the player strengths
            except:
                player['Strengths'] = ''
        elif line.startswith('Weakness'):
            try:
                player['Weakness'] = line.split(':')[1].strip()  # this gets the player weakness
            except:
                player['Weakness'] = ''
        elif line.startswith('Points Available'):
            try:
                player['Points Available'] = line.split(':')[1].strip()  # this gets the amount of points the player has available
            except:
                player['Points Available'] = '0'
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

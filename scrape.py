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
    csv_file = smjhl_players_csv
    csv_columns = player_dict_list[0].keys()
    with open(csv_file, 'w+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in player_dict_list:
            writer.writerow(data)


def get_shl_players(url_file, shl_players_csv):
    """use the urls provided in the json to get each player's information"""
    team_url_list = get_roster_url(url_file, 'SHL')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in team_url_list:  # For each team in the list
        player_url_list = get_player_urls(team[1])  # get each player page URL
        for player in player_url_list:  # for each player in player_url_list
            player_dict_list.append(get_player_stats('https://www.simulationhockey.com/' + player, team[0]))
    # look into using csv dictwriter.writerows() to write the list of dictionaries into the csv file
    csv_file = shl_players_csv
    csv_columns = player_dict_list[0].keys()
    with open(csv_file, 'w+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in player_dict_list:
            writer.writerow(data)


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
        print(user_agent)
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
    player = dict.fromkeys(['Team', 'Draft Class', 'First Name', 'Last Name', 'Position', 'Shoots', 'Recruited by',
                            'Player Render', 'Jersey Number', 'Height', 'Weight', 'Birthplace', 'Player Type',
                            'Strengths', 'Weakness', 'Points Available', 'CK', 'FG', 'DI', 'SK', 'ST', 'EN', 'DU', 'PH',
                            'FO', 'PA', 'SC', 'DF', 'PS', 'AG', 'SZ', 'RB', 'RT', 'HS', 'TPE'])
    player['Team'] = team
    user_agent = random.choice(user_agent_list)
    print(user_agent)
    headers = {'User-Agent': user_agent}
    player_page = requests.get(name_url, headers=headers)
    soup = BeautifulSoup(player_page.content, 'html.parser')

    # Get the Position, TPE, and Draft Class
    position_and_class = soup.find_all('td', 'thead')[1].strong.text
    tpe = str()
    draft_class = str()
    position = str()

    if position_and_class.__contains__(' C ') or position_and_class.__contains__(
            ' Center ') or position_and_class.__contains__(' CENTER '):
        position = 'C'
    if position_and_class.__contains__(' LW ') or position_and_class.__contains__(
            ' Left Wing ') or position_and_class.__contains__(' LEFT WING '):
        position = 'LW'
    if position_and_class.__contains__(' RW ') or position_and_class.__contains__(
            ' Right Wing ') or position_and_class.__contains__(' RIGHT WING '):
        position = 'RW'
    if position_and_class.__contains__(' D ') or position_and_class.__contains__(
            ' Defense ') or position_and_class.__contains__(' DEFENSE '):
        position = 'D'
    if position_and_class.__contains__(' G ') or position_and_class.__contains__(
            ' Goalie ') or position_and_class.__contains__(' GOALIE '):
        position = 'G'

    draft_class = position_and_class.split()[0].strip('[').strip(']')
    try:
        tpe = soup.find_all('td', 'thead')[1].small.text
        if len(tpe.split()) == 3:
            tpe = tpe.split()[2]
        else:
            tpe = tpe.split()[1]
    except:
        tpe = 'Calculation function not available'


    post = soup.find_all('div', 'post_body scaleimages')[0]
    post_text = post.text.split('\n')  # split the text from the body up into rows for easy iteration

    player['Draft Class'] = draft_class
    player['TPE'] = tpe
    player['Played Position'] = position

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
                print(player['Last Name'])
            except:
                player['Last Name'] = ''
        elif line.startswith('Position'):
            try:
                player['Position'] = line.split(':')[1].strip()  # this gets the player position
            except:
                player['Position'] = ''
        elif line.startswith('Shoots'):
            try:
                if line.split(':')[1].strip() == 'L':
                    player['Shoots'] = 'Left'  # this gets the player shooting hand
                if line.split(':')[1].strip() == 'R':
                    player['Shoots'] = 'Right'
                else:
                    player['Shoots'] = line.split(':')[1].strip()
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
                available = line.split(':')[1].strip()  # this gets the amount of points the player has available
                available = available.split()[0].rstrip('Â')
                player['Points Available'] = available
            except:
                player['Points Available'] = '0'
        #if position != 'G' and player['Last Name'] != 'Yukikami' and player['Last Name'] != 'Hughes':
        if position != 'G':
            if line.startswith('CK'):
                player['CK'] = line.split(': ')[1]  # this gets the player Checking
            elif line.startswith('FG'):
                player['FG'] = line.split(': ')[1]  # this gets the player fighting
            elif line.startswith('DI'):
                player['DI'] = line.split(': ')[1]  # this gets the player Discipline
            elif line.startswith('SK'):
                player['SK'] = line.split(': ')[1]  # this gets the player skating
            elif line.startswith('ST'):
                player['ST'] = line.split(':')[1].strip()  # this gets the player strength
            elif line.startswith('EN'):
                player['EN'] = line.split(': ')[1]  # this gets the player endurance
            elif line.startswith('DU'):
                #player['DU'] = line.split(': ')[1]  # this gets the player durability
                player['DU'] = '50'
            elif line.startswith('PH'):
                try:
                    player['PH'] = line.split(':')[1].strip()  # this gets the player Puck handling
                except:
                    player['PH'] = ''
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
        elif position == 'G':
            if line.startswith('SK'):
                player['SK'] = line.split(': ')[1]  # this gets the player skating
            elif line.startswith('DU'):
                #player['DU'] = line.split(': ')[1]  # this gets the player durability
                player['DU'] = '50'
            elif line.startswith('EN'):
                player['EN'] = line.split(': ')[1]  # this gets the player endurance
            elif line.startswith('SZ'):
                player['SZ'] = line.split(': ')[1]  # this gets the player Size
            elif line.startswith('AG'):
                player['AG'] = line.split(': ')[1]  # this gets the player Agility
            elif line.startswith('RB'):
                player['RB'] = line.split(': ')[1]  # this gets the player rebound control
            elif line.startswith('SC'):
                player['SC'] = line.split(': ')[1]  # this gets the player style control
            elif line.startswith('HS'):
                player['HS'] = line.split(': ')[1]  # this gets the player Hand speed
            elif line.startswith('RT'):
                player['RT'] = line.split(': ')[1]  # this gets the player reaction Time
            elif line.startswith('PH'):
                player['PH'] = line.split(': ')[1]  # this gets the player Puck handling
            elif line.startswith('PS'):
                player['PS'] = line.split(': ')[1]  # this gets the player penalty shot
    return player  # return the player


def get_player_tpe(page, player_dict):
    """calculate the total tpe based on points given. Takes in a page and player dict as backup"""
    position_and_class = page.strong.text
    tpe = str()
    draft_class = str()
    position = str()

    if position_and_class.__contains__(' C ') or position_and_class.__contains__(' Center ') or position_and_class.__contains__(' CENTER '):
        position = 'C'
    if position_and_class.__contains__(' LW ') or position_and_class.__contains__(' Left Wing ') or position_and_class.__contains__(' LEFT WING '):
        position = 'LW'
    if position_and_class.__contains__(' RW ') or position_and_class.__contains__(' Right Wing ') or position_and_class.__contains__(' RIGHT WING '):
        position = 'RW'
    if position_and_class.__contains__(' D ') or position_and_class.__contains__(' Defense ') or position_and_class.__contains__(' DEFENSE '):
        position = 'D'
    if position_and_class.__contains__(' G ') or position_and_class.__contains__(' Goalie ') or position_and_class.__contains__(' GOALIE '):
        position = 'G'

    draft_class = position_and_class.split()[0].strip('[').strip(']')
    try:
        tpe = page.small.text
        if len(tpe.split()) == 2:
            tpe = tpe.split()[1]
        else:
            print(len(tpe.split()))
    except:
        tpe = 'Calculate it yourself!'

    print(position_and_class)
    return tpe, draft_class, position


def main():
    """main"""
    url_file = "roster_urls.json"
    smjhl_players_csv = "smjhl-2020-2-24.csv"
    shl_players_csv = "shl-2020-1-31.csv"
    get_smjhl_players(url_file, smjhl_players_csv)
    #get_shl_players(url_file, shl_players_csv)


main()

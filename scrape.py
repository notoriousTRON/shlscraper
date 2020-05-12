import requests, json, csv, random
from bs4 import BeautifulSoup
import os
os.chdir(r'C:\projects\shl_scraper')


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

def get_shl_prospects(url_file, shl_prospects_csv):
    """use the urls provided in the json to get each player's information"""
    prospect_url_list = get_roster_url(url_file, 'Prospects')
    player_dict_list = list()  # list that will hold all of the player info dicts to be put into a csv
    for team in prospect_url_list:  # For each team in the list
        player_url_list = get_player_urls(team[1])  # get each player page URL
        for player in player_url_list:  # for each player in player_url_list
            player_dict_list.append(get_player_stats('https://www.simulationhockey.com/' + player, team[0]))
    # look into using csv dictwriter.writerows() to write the list of dictionaries into the csv file
    csv_file = shl_prospects_csv
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
            a = section.find('a', attrs={'style':'font-size:14px;'}, href=True)
            return_list.append(a['href'])
        has_next = len(soup.find_all('a', 'pagination_next')) != 0  # check if there is a next page
        if has_next:
            page += 1
    return return_list


def get_player_stats(name_url, team):
    """Use the given url to find and get all of the stats. Returns a dictionary"""
    player = dict.fromkeys(['Team', 'Draft Class', 'First Name', 'Last Name', 'Position', 'Shoots', 'Recruited by',
                            'Player Render', 'Jersey Number', 'Height', 'Weight', 'Birthplace', 'Player Type',
                            'Strengths', 'Weakness', 'Points Available', 
                            'Screening', 'Getting Open', 'Passing', 'Puckhandling', 'Shooting Accuracy', 'Shooting Range', 'Offensive Read',
                            'Checking','Hitting','Stickchecking','Shot Blocking','Faceoffs','Defensive Read',
                            'Acceleration','Agility','Balance','Speed','Stamina','Strength','Fighting',
                            'Aggression','Bravery','Determination','Team Player','Leadership','Temperament','Professionalism',
                            'Blocker','Glove','Passing','Poke Check','Positioning','Rebound','Recovery','Puckhandling','Low Shots','Reflexes','Skating',
                            'Mental Toughness','Goalie Stamina',
                            'TPE'
                           ])
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

    draft_class = 'S' + position_and_class.split()[0].strip('[').strip(']').strip('S')
    try:
        tpe = soup.find_all('td', 'thead')[1].small.text
        if len(tpe.split()) == 3:
            tpe = tpe.split()[2]
        else:
            tpe = tpe.split()[1]
    except:
        tpe = 'Calculation function not available'

    post = soup.find_all('div', 'post_body scaleimages')[0]
    post_text = post.text.split('\n') # split the text from the body up into rows for easy iteration

    player['Draft Class'] = draft_class
    player['TPE'] = tpe
    player['Played Position'] = position

    for l in post_text:
        ln = l.split('|')
        for line in ln:
            # why don't switch statements exist in Python???????
            if line.startswith('First Name'):
                try:
                    player['First Name'] = get_attr(line,1)  # this gets the first name from the first name line
                except:
                    player['First Name'] = ''
            elif line.startswith('Last Name'):
                try:
                    player['Last Name'] = get_attr(line,1)  # this gets the first name from the last name line
                    print(player['Last Name'])
                except:
                    player['Last Name'] = ''
            elif line.startswith('Shoots'):
                try:
                    if get_attr(line,1)  == 'L':
                        player['Shoots'] = 'Left'  # this gets the player shooting hand
                    if get_attr(line,1)  == 'R':
                        player['Shoots'] = 'Right'
                    else:
                        player['Shoots'] = get_attr(line,1) 
                except:
                    player['Shoots'] = ''
            elif line.startswith('Recruited'):
                try:
                    player['Recruited by'] = get_attr(line,1)   # this gets where they were recruited (if applicable)
                except:
                    player['Recruited by'] = ''
            elif line.startswith('Player Render'):
                try:
                    player['Player Render'] = get_attr(line,1)   # this gets the player render
                except:
                    player['Player Render'] = ''
            elif line.startswith('Jersey Number'):
                try:
                    player['Jersey Number'] = get_attr(line,1)   # this gets the player Jersey Number
                except:
                    player['Jersey Number'] = ''
            elif line.startswith('Height'):
                try:
                    player['Height'] = get_attr(line,1)   # this gets the player height
                except:
                    player['Height'] = ''
            elif line.startswith('Weight'):
                try:
                    player['Weight'] = get_attr(line,1)   # this gets the player weight
                except:
                    player['Weight'] = ''
            elif line.startswith('Birthplace'):
                try:
                    player['Birthplace'] = get_attr(line,1)   # this gets the player birthplace
                except:
                    player['Birthplace'] = ''
            elif line.startswith('Player Type'):
                try:
                    player['Player Type'] = get_attr(line,1)   # this gets the player type
                except:
                    player['Player Type'] = ''
            elif line.startswith('Points Available'):
                try:
                    available = get_attr(line,1)   # this gets the amount of points the player has available
                    available = available.split()[0].rstrip('Â')
                    player['Points Available'] = available
                except:
                    player['Points Available'] = '0'
            #if position != 'G' and player['Last Name'] != 'Yukikami' and player['Last Name'] != 'Hughes':
            #skater ratings
            if position != 'G':
                #Offensive Ratings
                if line.startswith('Screening'):
                    player['Screening'] = get_attr(line,1)   # this gets the player Screening
                elif line.startswith('Getting Open'):
                    player['Getting Open'] = get_attr(line,1)   # this gets the player Getting Open
                elif line.startswith('Passing'):
                    player['Passing'] = get_attr(line,1)   # this gets the player Passing
                elif line.startswith('Puckhandling'):
                    player['Puckhandling'] = get_attr(line,1)  # this gets the player Puckhandling
                elif line.startswith('Shooting Accuracy'):
                    player['Shooting Accuracy'] = get_attr(line,1)   # this gets the player Shooting Accuracy
                elif line.startswith('Shooting Range'):
                    player['Shooting Range'] = get_attr(line,1)   # this gets the player Shooting Range
                elif line.startswith('Offensive Read'):
                    player['Offensive Read'] = get_attr(line,1)   # this gets the player Offensive Read
                #Defensive Ratings
                elif line.startswith('Checking'):
                    player['Checking'] = get_attr(line,1)   # this gets the player Checking
                elif line.startswith('Hitting'):
                    player['Hitting'] = get_attr(line,1)   # this gets the player Hitting
                elif line.startswith('Positioning'):
                    player['Positioning'] = get_attr(line,1)   # this gets the player Positioning
                elif line.startswith('Stickchecking'):
                    player['Stickchecking'] = get_attr(line,1)   # this gets the player Stickchecking
                elif line.startswith('Shot Blocking'):
                    player['Shot Blocking'] = get_attr(line,1)   # this gets the player Shot Blocking
                elif line.startswith('Faceoffs'):
                    player['Faceoffs'] = get_attr(line,1)   # this gets the player Faceoffs
                elif line.startswith('Defensive Read'):
                    player['Defensive Read'] = get_attr(line,1)   # this gets the player Defensive Read
                #Physical Ratings
                elif line.startswith('Acceleration'):
                    player['Acceleration'] = get_attr(line,1)   # this gets the player Acceleration
                elif line.startswith('Agility'):
                    player['Agility'] = get_attr(line,1)   # this gets the player Agility
                elif line.startswith('Balance'):
                    player['Balance'] = get_attr(line,1)   # this gets the player Balance
                elif line.startswith('Speed'):
                    player['Speed'] = get_attr(line,1)   # this gets the player Speed
                elif line.startswith('Stamina'):
                    player['Stamina'] = get_attr(line,1)   # this gets the player Stamina
                elif line.startswith('Strength'):
                    player['Strength'] = get_attr(line,1)   # this gets the player Strength
                elif line.startswith('Fighting'):
                    player['Fighting'] = get_attr(line,1)   # this gets the player Fighting
                #Mental Ratings
                elif line.startswith('Aggression'):
                    player['Aggression'] = get_attr(line,1)   # this gets the player Aggression
                elif line.startswith('Bravery'):
                    player['Bravery'] = get_attr(line,1)   # this gets the player Bravery
                elif line.startswith('*Determination'):
                    player['Determination'] = '15'  # this gets the player Determination
                elif line.startswith('*Team Player'):
                    player['Team Player'] = '15'  # this gets the player Team Player
                elif line.startswith('*Team Player'):
                    player['Team Player'] = '15'  # this gets the player Team Player
                elif line.startswith('*Temperament'):
                    player['Temperament'] = '15'  # this gets the player Temperament
                elif line.startswith('*Professionalism'):
                    player['Professionalism'] = '15'  # this gets the player Professionalism
            #goalie ratings    
            elif position == 'G':
                #goalie ratings
                if line.startswith('Blocker'):
                    player['Blocker'] = get_attr(line,1)   # this gets the player Blocker
                elif line.startswith('Glove'):
                    player['Glove'] = get_attr(line,1)  # this gets the player Glove
                elif line.startswith('Passing'):
                    player['Passing'] = get_attr(line,1)   # this gets the player Passing
                elif line.startswith('Poke Check'):
                    player['Poke Check'] = get_attr(line,1)   # this gets the player Poke Check
                elif line.startswith('Positioning'):
                    player['Positioning'] = get_attr(line,1)   # this gets the player Positioning
                elif line.startswith('Rebound'):
                    player['Rebound'] = get_attr(line,1)   # this gets the player Rebound
                elif line.startswith('Recovery'):
                    player['Recovery'] = get_attr(line,1)   # this gets the player Recovery
                elif line.startswith('Puckhandling'):
                    player['Puckhandling'] = get_attr(line,1)   # this gets the player Puckhandling
                elif line.startswith('Low Shots'):
                    player['Low Shots'] = get_attr(line,1)   # this gets the player Low Shots
                elif line.startswith('Reflexes'):
                    player['Reflexes'] = get_attr(line,1)   # this gets the player Reflexes
                elif line.startswith('Skating'):
                    player['Skating'] = get_attr(line,1)   # this gets the player Skating
                #mental ratings
                elif line.startswith('*Aggression'):
                    player['Aggression'] = '8'  # this gets the player Aggression
                elif line.startswith('Mental Toughness'):
                    player['Mental Toughness'] = get_attr(line,1)   # this gets the player Mental Toughness
                elif line.startswith('*Determination'):
                    player['Determination'] = '15'  # this gets the player Determination
                elif line.startswith('*Team Player'):
                    player['Team Player'] = '15' # this gets the player Team Player
                elif line.startswith('*Leadership'):
                    player['Leadership'] = '15'  # this gets the player Leadership
                elif line.startswith('Goalie Stamina'):
                    player['Goalie Stamina'] = get_attr(line,1)   # this gets the player Goalie Stamina
                elif line.startswith('*Professionalism'):
                    player['Professionalism'] = '15' # this gets the player Professionalism

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

def get_attr(line,pos):
    try:
        out = line.split(':')[pos].strip()
    except:
        try:
            out = line.split(' ')[pos].strip()
        except:
            try:
                out = line.split(';')[pos].strip()
            except:
                try:
                    out = line.split('-')[pos].strip()
                except:
                    out = None
    return out


def main():
    """main"""
    url_file = "roster_urls.json"
    smjhl_players_csv = "smjhl-2020-5-9.csv"
    shl_players_csv = "shl-2020-5-9.csv"
    shl_prospects_csv = "prospects-2020-5-9.csv"
    get_smjhl_players(url_file, smjhl_players_csv)
    get_shl_players(url_file, shl_players_csv)
    get_shl_prospects(url_file, shl_prospects_csv)

main()

import requests
from bs4 import BeautifulSoup

URL = 'https://simulationhockey.com/forumdisplay.php?fid=5'

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())

#print(soup.find_all('div'))

for div in soup.find_all('div', class_="float_left"):
    soup = div
    print(div)
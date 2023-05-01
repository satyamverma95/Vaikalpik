from bs4 import BeautifulSoup as bs
import requests


def write_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


res = requests.get("https://en.wikipedia.org/wiki/Differential_calculus")
soup = bs(res.text, "html.parser")
body_content = soup.find('div', {'class': 'mw-parser-output'})

naval_battles = {}


for link in body_content.find_all("a"):
    url = link.get("href", "")
    if "/wiki/" in url:
        naval_battles[link.text.strip()] = url

write_to_file("experiment.txt" , ','.join(naval_battles))
from urllib import response
from bs4 import BeautifulSoup, SoupStrainer
import re
import urllib3

# url = "home.html"
# page = urllib3.urlopen(url)
# response = BeautifulSoup(page.read())
response = BeautifulSoup(open("./home.html", encoding="utf8"), "lxml")

# print(response.prettify())

# print(response.find_all('div'))

links = []
for link in response.find_all('a', href=True):
    link_ = link['href']
    if '/ncr/' in link_[:6]:
        if not link_[:-5] in links:
            links.append(link_[:-5])

for l in links:
    print(l) 

print(len(links))

import pickle
pickle.dump(links, open("links5.pkl", "wb"))
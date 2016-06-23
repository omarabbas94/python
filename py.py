

import requests
from bs4 import BeautifulSoup

url = 'https://www.pastefs.com/pid/1439'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html,"lxml")
                     
letters = soup.find_all("div", class_="new-paste")


print soup.prettify()

 

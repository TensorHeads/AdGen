from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
import json
import shutil
import mechanize

DATA = []
f = open("data.txt","w")

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/68700.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'}
url = "https://www.gettyimages.com/photos/handbag-modelling?compositions=fulllength,portrait&page=1&mediatype=photography&numberofpeople=one&orientations=vertical&phrase=Handbag%20modelling&sort=mostpopular".format
soup = BeautifulSoup(requests.get("https://www.gettyimages.com/photos/handbag-modelling?compositions=fulllength,portrait&page=1&mediatype=photography&numberofpeople=one&orientations=vertical&phrase=Handbag%20modelling&sort=mostpopular", headers=USER_AGENT).text,"html.parser")
raw_results = soup.find_all("img", {"class": ["gallery-asset__thumb", "gallery-mosaic-asset__thumb"]})

for i in range(1,101):
	print(i, len(DATA))
	html = "https://www.gettyimages.com/photos/handbag-modelling?compositions=fulllength,portrait&page={}&mediatype=photography&numberofpeople=one&orientations=vertical&phrase=Handbag%20modelling&sort=mostpopular".format(i)
	soup = BeautifulSoup(requests.get(html, headers=USER_AGENT).text,"html.parser")
	raw_results = soup.find_all("img", {"class": ["gallery-asset__thumb", "gallery-mosaic-asset__thumb"]})

	for j in raw_results:
		DATA.append(j['src'])
		f.write(j['src']+"\n")
	
f.close()
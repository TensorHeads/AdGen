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
soup = BeautifulSoup(requests.get("https://depositphotos.com/stock-photos/model-with-handbag.html?sh=d9f2e6ed221613bd92180e837b02833c", headers=USER_AGENT).text,"html.parser")
raw_results = soup.find_all("img", {"class": ["file-container__image"]})

statics = raw_results[:22]
dynamic = raw_results[22:]

for j in statics:
	DATA.append(j['src'])
	f.write(j['src']+"\n")
for j in dynamic:
	DATA.append(j['data-src'])
	f.write(j['data-src']+"\n")


for i in range(100, 14200, 100):
	print(i, len(DATA))
	html = "https://depositphotos.com/stock-photos/model-with-handbag.html?offset={}&sh=d9f2e6ed221613bd92180e837b02833c".format(i)
	soup = BeautifulSoup(requests.get(html, headers=USER_AGENT).text,"html.parser")
	raw_results = soup.find_all("img", {"class": ["file-container__image"]})

	statics = raw_results[:22]
	dynamic = raw_results[22:]

	for j in statics:
		DATA.append(j['src'])
		f.write(j['src']+"\n")
	for j in dynamic:
		DATA.append(j['data-src'])
		f.write(j['data-src']+"\n")

f.close()
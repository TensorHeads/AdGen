from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
import json
import shutil


USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/68700.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'}

number = 1

data=[]

for i in range(0,7149,110):
	USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/{}.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'.format(i)}
	url = "https://www.123rf.com/stock-photo/backpack_models.html?imgtype=1&oriSearch=backpack%20back&cko=2&start={}&sti=nwo7pllxk0fcm0ywr9|".format(i)

	soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text,"html.parser")
	raw_results = soup.find_all("div", class_="mosaic-main-container")

	print(len(raw_results), i)

	for j in raw_results:
		data.append(j.a['href'])
		
f = open("data1.json","w")
f.write(json.dumps({"data":data}))
f.close()
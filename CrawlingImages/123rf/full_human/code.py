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
	url = "https://www.123rf.com/stock-photo/woman_standing_front.html?oriSearch=woman%20standing&cko=2&isolated=1&start={}&sti=o2sxqngycy3gljkhad|".format(i)

	soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text,"html.parser")
	raw_results = soup.find_all("div", class_="mosaic-main-container")

	print(len(raw_results), i)

	for j in raw_results:
		data.append(j.a['href'])
		
f = open("data1.json","w")
f.write(json.dumps({"data":data}))
f.close()
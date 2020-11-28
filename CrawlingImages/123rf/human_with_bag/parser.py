import json
f = open("data1.json",'r')
data = json.loads(f.read())
data = data['data']


from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
import json
import shutil


USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/68700.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'}

number = 3785
for i in range(3785,len(data)):

	try:
		USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/{}.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'.format(i%100)}
		url = data[i]

		soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text,"html.parser")
		raw_results = soup.find_all("div", class_="row comp-img-wrapper squared")


		responseImage = requests.get(raw_results[0].div.find("img", {"id": "compImg"})['src'], stream=True)
		with open('backpack/{}.jpg'.format(number), 'wb') as out_file:
			shutil.copyfileobj(responseImage.raw, out_file)
		del responseImage
		number += 1

	except Exception as e:
		print(e)
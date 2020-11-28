f = open('data1.txt','r')
data = f.read().split("\n")

data = list(set(data))


import requests
import shutil

USER_AGENT = {'User-Agent':'Mozilla/3.5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/68700.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'}

for i in range(len(data)):
	USER_AGENT = {'User-Agent':'Mozilla/{} (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/68700.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'.format(i%100)}
	if i <= 374:
		pass
	else:
		responseImage = requests.get(data[i], stream=True, headers=USER_AGENT)
		with open('data/{}.jpg'.format(i+1), 'wb') as out_file:
		    shutil.copyfileobj(responseImage.raw, out_file)
		del responseImage
f = open('data.txt','r')
data = f.read().split("\n")

data = list(set(data))


import requests
import shutil

for i in range(len(data)):
	responseImage = requests.get(data[i], stream=True)
	with open('data/{}.jpg'.format(i+1), 'wb') as out_file:
	    shutil.copyfileobj(responseImage.raw, out_file)
	del responseImage
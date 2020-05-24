#!/bin/python3
# youtubify.py
# The begnnings of a personal spotify built on youtube.
# Now lets get banned

import requests
from bs4 import BeautifulSoup
import subprocess
searchterm = 'To+Be+Alone+Five+Finger+Death+Punch'
URL = 'https://youtube.com/results?search_query='+searchterm
page = requests.get(URL)
if page.status_code != 200:
	print("failed")
	exit(1)
soup = BeautifulSoup(page.content, 'html.parser')
links = []
names = []
results = list(soup.findAll('a',attrs={'class':'yt-uix-tile-link'}))
for i in range(5):
	foundString = str(results[i])
#	print(foundString)
	offset = foundString.find("href")
	links.append(foundString[offset+15:offset+26])
#	print(links[i])
	offset1 = foundString.find("title")
	offset2 = foundString.find('"',offset1+7)
	names.append(foundString[offset1+7:offset2])
	outString = names[i]+' Link: https://youtube.com/watch?v='+links[i]
	print(outString)
proc = subprocess.run(["youtube-dl","-f 140","https://youtube.com/watch?v="+links[0]])
print(proc.stdout)
#curl 'https://img.youtube.com/vi/09DLBQy_bF4/maxresdefault.jpg' --output maxresdefault.jpg


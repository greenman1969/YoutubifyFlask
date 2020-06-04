#!/bin/python3
# youtubify.py
# The begnnings of a personal spotify built on youtube.
# Now lets get banned

from flask import Flask, request
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup
import subprocess
from typing import NamedTuple


def openHTML():
	basicPage = ''' <!DOCTYPE html>
					<html>
				'''
	return basicPage
	
def headHTML():
	basicPage = ''' <head>
						<title>Youtube/Spotify</title>
						<style>
							.leftbox {
								float:left;
								width:160px;
								height:90px;
								margin-bottom:10px;
							}
							.rightboxtop {
								width:100%;
								float:left;
								height:45px;
							}
							.rightboxbot {
								width:100%;
								float:left;
								height:45px;
							}
							.rightbox {
								display:inline-block;
							}
							.main {
								position:relative;
								width:100%;
								display:inline-block;
							}
						</style>
					</head>
				'''
	return basicPage

def closeHTML():
	basicPage = ''' </html>
				'''
	return basicPage
def homeHTML():
	basicPage = '''	<body>
						<h1>Youtube/Spotify</h1>
						<iframe src="searchPage" height="400" width="100%"></iframe>
						<h2>Currently Playing: </h2>
						<iframe src="queue" height="400" width="20%"></iframe>
					</body>
				'''
	return openHTML()+headHTML()+basicPage+closeHTML()

def searchFrame():
	basicPage = '''	<body>
						<form method="POST" action="search">
							<input name="text">
							<input type="submit">
						</form>
					</body>
				'''
	return openHTML()+headHTML()+basicPage+closeHTML()
def searchHTML(searchTerm, ids, names, URLs):
	basicPage = '''	<body>
						<p>Search Results for "'''+searchTerm+'''"</p>
						<p><a href="searchPage">Click here to return to search page</a></p>
				'''
	for i in range(len(ids)):
		basicPage+=generateResult(ids[i],names[i],URLs[i])
	basicPage += ''' </body>
				'''
	return openHTML()+headHTML()+basicPage+closeHTML()
def generateQueueItem(vidID,name,url):
	basicPage = '''	<div class="main">
						<div class="leftbox">
							<img src='https://img.youtube.com/vi/'''+vidID+'''/maxresdefault.jpg' width="160" height="90">
						</div>
						<div class="rightbox">
							<div class="rightboxtop">
								<h3><a href="'''+url+'''">'''+name+'''</a></h3>
							</div>
							<div class="rightboxbot">
								<form method="POST" action="addSong">
									<input type="submit" value="Add Song">
									<input type="submit" value="Add Front of Queue">
								</form>
							</div>
						</div>
					</div>
				'''
	return basicPage
def generateResult(vidID,name,url):
	basicPage = '''	<div class="main">
						<div class="leftbox">
							<img src='https://img.youtube.com/vi/'''+vidID+'''/maxresdefault.jpg' width="160" height="90">
						</div>
						<div class="rightbox">
							<div class="rightboxtop">
								<h3><a href="'''+url+'''">'''+name+'''</a></h3>
							</div>
							<div class="rightboxbot">
								<form method="POST" action="addSong">
									<input type="submit" value="Add Song">
									<input type="submit" value="Add Front of Queue">
								</form>
							</div>
						</div>
					</div>
				'''
	return basicPage
	
	
	
def fsearchHTML():
	basicPage = '''	<body>
						<p>Search Failed</p>
					</body>
				'''
	return openHTML()+headHTML()+basicPage+closseHTML()
@app.route('/')
def root():
	return homeHTML()
@app.route('/searchPage')
def searchPage():
	return searchFrame()
@app.route('/addSong', methods=['POST'])
def addSong():
	
	
	
	
	return searchFrame()
	
@app.route('/queue')
def queue():
	
	return searchFrame()
@app.route('/search', methods=['POST'])
def search():
	st = request.form['text']
	ytURL = generateSearchURL(st)
	page = requests.get(ytURL)
	if page.status_code != 200:
		return fsearchHTML()
	
	soup = BeautifulSoup(page.content,'html.parser')
	ids = []
	names = []
	URLs = []
	results = list(soup.findAll('a',attrs={'class':'yt-uix-tile-link'}))
	if len(results)<5:
		return fsearchHTML()
	for i in range(5):
		foundString = str(results[i])
		offset = foundString.find("href")
		ids.append(foundString[offset+15:offset+26])
		offset1 = foundString.find("title")
		offset2 = foundString.find('"',offset1+7)
		names.append(foundString[offset1+7:offset2])
		URLs.append('https://youtube.com/watch?v='+ids[i])
		
	
	return searchHTML(st,ids,names,URLs)
	
	
	
	
	
	return searchHTML()
def generateSearchURL(searchTerm):
	return '''https://youtube.com/results?search_query='''+searchTerm.replace(' ','+')
if __name__ == '__main__':
	app.run()


# searchterm = 'To+Be+Alone+Five+Finger+Death+Punch'
# URL = 'https://youtube.com/results?search_query='+searchterm
# page = requests.get(URL)
# if page.status_code != 200:
	# print("failed")
	# exit(1)
# soup = BeautifulSoup(page.content, 'html.parser')
# links = []
# names = []
# results = list(soup.findAll('a',attrs={'class':'yt-uix-tile-link'}))
# for i in range(5):
	# foundString = str(results[i])
# #	print(foundString)
	# offset = foundString.find("href")
	# links.append(foundString[offset+15:offset+26])
# #	print(links[i])
	# offset1 = foundString.find("title")
	# offset2 = foundString.find('"',offset1+7)
	# names.append(foundString[offset1+7:offset2])
	# outString = names[i]+' Link: https://youtube.com/watch?v='+links[i]
	# print(outString)
# proc = subprocess.run(["youtube-dl","-f 140","https://youtube.com/watch?v="+links[0]])
# print(proc.stdout)
# #curl 'https://img.youtube.com/vi/09DLBQy_bF4/maxresdefault.jpg' --output maxresdefault.jpg


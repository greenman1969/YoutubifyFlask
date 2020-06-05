#!/bin/python3
# youtubify.py
# The begnnings of a personal spotify built on youtube.
# Now lets get banned

from flask import Flask, request
app = Flask(__name__, static_folder='static')
import requests
from bs4 import BeautifulSoup
import subprocess
import youtube_dl


queue = []
lastSearchPage = ""

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
								margin-bottom:5px;
								margin-top:5px;
								margin-right:10px;
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
							#player {
								width:100%
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
						<iframe src="nowPlaying" height="400" width="100%"></iframe>
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
						<form method="POST" action="search">
							<input name="text" value="'''+searchTerm+'''">
							<input type="submit">
						</form>
						<p>Search Results for "'''+searchTerm+'''"</p>
						<p><a href="searchPage">Click here to return to search page</a></p>
				'''
	for i in range(len(ids)):
		basicPage+=generateResult(ids[i],names[i],URLs[i])
	basicPage += ''' </body>
				'''
	return openHTML()+headHTML()+basicPage+closeHTML()
def generateQueueItem(vidID,name,url,queueNum,isForQueue):
	basicPage = '''	<div class="main">
						<div class="leftbox">
							<img src='https://img.youtube.com/vi/'''+vidID+'''/maxresdefault.jpg' width="160" height="90">
						</div>
						<div class="rightbox">
							<div class="rightboxtop">
								<h3><a href="'''+url+'''">'''+name+'''</a></h3>
							</div>
							<div class="rightboxbot">
								<form method="POST" action="'''
								
								
	if isForQueue == True:
		basicPage += "queuePage"
	else:
		basicPage += "nowPlaying"
	
	basicPage += '''">
									<input type="hidden" name="vidID" value="'''+vidID+'''">
									<input type="hidden" name="songName" value="'''+name+'''">
									<input type="hidden" name="url" value="'''+url+'''">
									<input type="hidden" name="queueNum" value="'''+str(queueNum)+'''">
									<input type="submit" name="submit" value="Remove Song">
								</form>
							</div>
						</div>
					</div>
				'''
	return basicPage

def generateNowPlaying():
	
	if len(queue) != 0:
		basicPage = '''	<audio controls autoplay id="player">
							<source src="/static/'''+queue[0][0]+'''.mp3" type="audio/mpeg">
						</audio>
					'''
		basicPage += generateQueueItem(queue[0][0],queue[0][1],queue[0][2],0,False)
		basicPage += '''<form method='POST' action="nowPlaying">
							<input type="submit" name="submit" value="Next" width="100%">
						</form>
						'''
		count = 1
		for i in queue[1:]:
			basicPage += generateQueueItem(i[0],i[1],i[2],count,True)
			count+=1
		
	else:
		basicPage='''	<head>
							<meta http-equiv="refresh" content="1">
						</head>'''
		
	return openHTML()+headHTML()+basicPage+closeHTML()
	
def generateQueue():
	basicPage=""
	count = 1
	for i in queue[1:]:
		basicPage += generateQueueItem(i[0],i[1],i[2],count,True)
		count+=1
		
	return openHTML()+headHTML()+basicPage+closeHTML()
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
									<input type="hidden" name="vidID" value="'''+vidID+'''">
									<input type="hidden" name="songName" value="'''+name+'''">
									<input type="hidden" name="url" value="'''+url+'''">
									<input type="submit" name="submit" value="Add Song">
									<input type="submit" name="submit" value="Add Front of Queue">
								</form>
							</div>
						</div>
					</div>
				'''
	return basicPage
	
	
	
def fsearchHTML():
	basicPage = '''	<body>
						<form method="POST" action="search">
							<input name="text">
							<input type="submit">
						</form>
						<p>Search Failed</p>
						<p><a href="searchPage">Click here to return to search page</a></p>
					</body>
				'''
	return openHTML()+headHTML()+basicPage+closeHTML()
@app.route('/')
def root():
	return homeHTML()
@app.route('/searchPage')
def searchPage():
	return searchFrame()
@app.route('/addSong', methods=['POST'])
def addSong():
	global lastSearchPage
	
	queueItem = [request.form['vidID'],request.form['songName'],request.form['url']]
	
	# Add Code to download the audio of the song in the queue.
	subprocess.run(["youtube-dl",request.form['url'],"-f 140","-x","--audio-format","mp3","-o","static/"+request.form['vidID']+".mp3"])
	
	if request.form['submit'] == "Add Song":
		print("Add Song")
		queue.append(queueItem)
	elif request.form['submit'] == "Add Front of Queue":
		print("Add Song to Front of Queue")
		queue.insert(0,queueItem)
	return lastSearchPage
	
@app.route('/nowPlaying', methods=['GET','POST'])
def nowPlaying():
	if request.method == 'POST':
		if request.form['submit'] == "Remove Song":
			queue.remove(queue[int(request.form['queueNum'])])
		if request.form['submit'] == "Next":
			temp = queue[0]
			queue.remove(temp)
			queue.append(temp)
	return generateNowPlaying()

@app.route('/queuePage', methods=['GET','POST'])
def queuePage():
	
	return generateQueue()
@app.route('/search', methods=['POST'])
def search():
	global lastSearchPage
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
	if len(results)<1:
		return fsearchHTML()
		
	numResults = len(results)
	if numResults > 20:
		numresults = 20
	
	for i in range(numResults):
		foundString = str(results[i])
		offset = foundString.find("href")
		ids.append(foundString[offset+15:offset+26])
		offset1 = foundString.find("title")
		offset2 = foundString.find('"',offset1+7)
		names.append(foundString[offset1+7:offset2])
		URLs.append('https://youtube.com/watch?v='+ids[i])
		
	lastSearchPage = searchHTML(st,ids,names,URLs)
	return lastSearchPage
	
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


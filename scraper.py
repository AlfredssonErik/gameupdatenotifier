import requests
import urllib.request
from datetime import datetime
import time
from bs4 import BeautifulSoup
from gs import GS

class Gamescraper():
	def __init__(self, db):
		self._client = None
		self.db = db
		self._wait_seconds = 30

	def getGameUpdates(self):
		games = self.db.get_games_update_page()
		if games is not None:
			print("Found %d games" % len(games))
			for game in games:
				response = requests.get(game)
				soup = BeautifulSoup(response.text, "html.parser")
				# Postblock is the container for each update
				newsList = soup.findAll("div", {"class": "newsPostBlock"})
				for news in newsList:
					title = soup.find("h2", {"class": "pageheader"}).text
					date = news.select(".date")[0].text.strip()
					updatename = news.select(".posttitle > a")[0].text.strip()
					link = news.select(".posttitle > a")[0]["href"]
					# If date is incomplete, this means it's this year.
					if "," not in date:
						date = date + ', 2019'
					date = datetime.strptime(date, "%d %b, %Y")
					print("Update found, trying to insert into sheet..")
					self.db.insertUpdate(title, date.strftime("%Y-%m-%d"), updatename, link)
			print("End of updates, waiting %d seconds" % self._wait_seconds)
		else:
			print("No games tracked.")
	
	def auto_scraper(self):
		while True:
			self.getGameUpdates()
			time.sleep(self._wait_seconds)
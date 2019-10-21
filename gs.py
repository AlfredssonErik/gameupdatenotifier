import sys
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

class GS():
	def __init__(self):
		self._client = None
		self.main()
	
	def main(self):
		try:
			credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)
			self._client = gspread.authorize(credentials)
			print('Connected!')
		except:
			sys.exit("Unable to connect, please check that you have a valid credentials.json file.\nTerminating...")

	def get_last_update(self, game):
		updates = self._client.open("Game updates").get_worksheet(0)
		l = updates.get_all_values()
		last_date = None
		for row in l[1:]:
			if row[0] == game:
				date = datetime.strptime(row[1], "%Y-%m-%d")
				if last_date == None:
					last_date = date
				elif last_date < date:
					last_date = date
		if last_date is None:
			return "No updates found"
		return(last_date.strftime("%Y-%m-%d"))
	
	def get_games(self):
		start = time.time()
		games = self._client.open("Game updates").get_worksheet(1)
		values_list = games.col_values(1)
		if len(values_list) > 1:
			output = []
			values_list.pop(0)
			for x in range(len(values_list)):
				date = self.get_last_update(values_list[x])
				title = values_list[x]
				output.append("\n%s\nLast updated: %s" % (title, date))
			for o in range(len(output)):
				print(output[o])
		else:
			print("No games tracked")
		end = time.time()
		total = end - start
		print("\nCompleted in: %s seconds." % str(round(total, 2)))
	
	def get_games_update_page(self):
		games = self._client.open("Game updates").get_worksheet(1)
		values_list = games.col_values(2)
		if len(values_list) > 1:
			values_list.pop(0)
			return values_list
		else:
			return None

	def insertUpdate(self, title, date, updatename, link):
		try:
			updates = self._client.open("Game updates").get_worksheet(0)
			found = updates.find(updatename)
		except gspread.SpreadsheetNotFound:
			sys.exit("You dont have access to this spreadsheet. Terminating...")
		except gspread.CellNotFound:
			found = None

		if found is None:
			insertRow = [title, date, updatename, link]
			updates.insert_row(insertRow, 2)
			print("Added update for %s" % title)
		else:
			print("%s already registered" % updatename)
			
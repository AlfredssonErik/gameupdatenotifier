from scraper import Gamescraper
from gs import GS

db = GS()
app = Gamescraper(db)

def Menu():
    val = input('''\n1. Scrape all updates
2. Get games list
3. Start auto-scraper
0. Exit
''')
    try:
        val = int(val)
        return val
    except:
        print("\nInvalid input")
        main()
 
 
def main():
	val = Menu()
	while val != 0:
		if val == 1:
			print("\nCollecting updates...")
			app.getGameUpdates()
		elif val == 2:
			print("\nRetrieving games list...")
			db.get_games()
		elif val == 3:
			print("\nStarting scheduler...")
			app.auto_scraper()
		val = Menu()
	print("Exiting")

main()
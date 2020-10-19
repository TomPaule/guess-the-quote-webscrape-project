#url we are scraping: https://quotes.toscrape.com/
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter



#starting URL
BASE_URL = "https://quotes.toscrape.com"


def scrape_quotes():
	#create an empty list of quotes
	all_quotes = []
	url = "/page/1"
	while url:
		#make a request
		r = requests.get(f"{BASE_URL}{url}")
		#show progress
		print(f"Now Scraping {BASE_URL}{url}....")
		s = BeautifulSoup(r.text, "html.parser")
		#find on site
		quotes = s.find_all(class_="quote")

		#loop through all of the quotes
		for quote in quotes:
			#add quotes, author, bio to list
			all_quotes.append({
				"text": quote.find(class_="text").get_text(),
				"author": quote.find(class_="author").get_text(),
				"bio-link": quote.find("a")["href"]
				})
		#look for next button on each page
		next_button = s.find(class_="next")
		#if we find next button, reset URL
		url = next_button.find("a")["href"] if next_button else None
		sleep(1)
	return all_quotes


#write quotes to csv file
def write_quotes(quotes):
	with open("quotes.csv", "w") as file:
		headers = ["text", "author", "bio-link"]
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writeheader()
		for quote in quotes:
			csv_writer.writerow(quote)

quotes = scrape_quotes()
write_quotes(quotes)






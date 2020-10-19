#url we are scraping: https://quotes.toscrape.com/
import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader



#starting URL
BASE_URL = "https://quotes.toscrape.com"


def read_quotes(filename):
	with open(filename, "r") as file:
		csv_reader = DictReader(file)
		return list(csv_reader)

def start_game(quotes):
	#create random quote
	quote = choice(quotes)
	remaining_guesses = 4
	#print quote
	print("Here's a quote: ")
	print(quote["text"])

	guess = ''
	while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
		guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\n")
		#correct answer
		if guess.lower() == quote["author"].lower():
			print("You got it!")
			break
		remaining_guesses -= 1
		#give hint
		if remaining_guesses == 3:
			r = requests.get(f"{BASE_URL}{quote['bio-link']}")
			s = BeautifulSoup(r.text, "html.parser")
			birth_date = s.find(class_="author-born-date").get_text()
			birth_place = s.find(class_="author-born-location").get_text()
			print(f"Here's a hint: The author was born {birth_place} on {birth_date}")
		elif remaining_guesses == 2:
			print(f"Here's a hint: The author's first name start's with: {quote['author'][0]}")
		elif remaining_guesses == 1:
			last_initial = quote["author"].split(" ")[1][0]
			print(f"Here's a hint: The author's last name start's with: {last_initial}")
		else:
			print(f"Sorry you ran out of guesses. Ther answer is {quote['author']}")

	#options after game
	again = ''
	while again.lower() not in ('y', 'yes', 'n', 'no'):
		again = input("Would you like to play again (y/n)?")
	if again.lower() in ('yes', 'y'):
		return start_game(quotes)
	else:
		print("See ya later!")

quotes = read_quotes("quotes.csv")
start_game(quotes)













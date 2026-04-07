from bs4 import BeautifulSoup
from scraper.engine import WebcrimsBot

class WebcrimsParser:
    def __init__(self, html_soup: BeautifulSoup):
        self.html_soup = html_soup

if __name__ == "__main__":
    court_codes = ["NY051033J%3AU"]
    bot = WebcrimsBot(court_codes=court_codes)
    bot.submit_all()
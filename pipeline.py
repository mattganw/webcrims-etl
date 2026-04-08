# court_codes = ["NY051033J%3AU"]
    # bot = WebcrimsBot(court_codes=court_codes)
    # bot.submit_all()

from scraper.engine import WebcrimsBot
from scraper.parser import WebcrimsParser
from scraper.courts import COURT_CODE_LOOKUP

if __name__ == "__main__":
    court_codes = ["NY051033J%3AU", "NY051043J%3AU", "NY051053J%3AU"]

    bot = WebcrimsBot(court_codes=court_codes)
    bot.run()



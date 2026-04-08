# court_codes = ["NY051033J%3AU"]
    # bot = WebcrimsBot(court_codes=court_codes)
    # bot.submit_all()

from scraper import WebcrimsBot

if __name__ == "__main__":
    court_codes = ["NY051033J%3AU", "NY051043J%3AU", "NY051053J%3AU"]

    bot = WebcrimsBot(court_codes=court_codes)
    bot.run()
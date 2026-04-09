from scraper import WebcrimsBot
from scraper import SeleniumScraper
from database import MSSQLConnection
from database import DBController
from config import BotSettings

def main() -> None:

    # sel = SeleniumScraper()
    # sel.run()

    # All Suffolk Courts
    settings = BotSettings()
    court_codes = settings.select_by_name("Suffolk")

    # Connect to DB and instantiate DBController
    db_conn = MSSQLConnection()
    controller = DBController(db_conn)

    # Instantiate bot
    bot = WebcrimsBot(
        court_codes=court_codes, 
        num_days=settings.num_days, 
        wait_time=settings.wait_time
    )

    # Extract and transform
    df = bot.run()

    # Load into DB
    controller.insert_staging(df)
    controller.merge_tables()
    controller.truncate_staging()

    print("End of run.")


if __name__ == "__main__":
    main()




    



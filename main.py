from config import logger
from config import Settings
from database import MSSQLConnection
from database import DBController
from scraper import WebcrimsBot

def main() -> None:

    # Get settings and court codes
    settings = Settings()
    COURT_CODES = settings.select_by_name(settings.court_name)
    
    # Connect to DB
    db_conn = MSSQLConnection(settings.db_connection_string)

    # Instantiate bot
    bot = WebcrimsBot(
        court_codes=COURT_CODES, 
        num_days=settings.num_days, 
        wait_time=settings.wait_time,
        url=settings.url
    )

    logger.info("Starting Webcrims extract...")
    # Extract and transform
    df = bot.run()

    # Load into DB
    controller = DBController(db_conn)
    controller.insert_staging(df)
    controller.merge_tables()
    controller.truncate_staging()

    logger.info("End of run.")

if __name__ == "__main__":
    main()




    



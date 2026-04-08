from scraper import WebcrimsBot
from database import MSSQLConnection
from database import DBController

def main() -> None:
    # Suffolk 1-6 District Courts
    court_codes = ["NY051033J%3AU", "NY051043J%3AU", "NY051053J%3AU", "NY051063J%3AU", "NY051073J%3AU", "NY051083J%3AU"]
    days = 7

    db_conn = MSSQLConnection()
    controller = DBController(db_conn)
    bot = WebcrimsBot(court_codes=court_codes, num_days=days)

    # Extract and transform
    df = bot.run()

    # Load into DB
    controller.insert_staging(df)
    controller.merge_tables()
    controller.truncate_staging()

    print("End of run.")

if __name__ == "__main__":
    main()




    



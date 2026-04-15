""" 
SeleniumScraper helper class used to initialize and refresh court_codes.json: 
    - Scrapes website to store unique court codes and their matching names
    - Must be run without headless mode
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.remote.webelement import WebElement

from pathlib import Path
import json

from config import logger

class CourtRefresher:

    URL = "https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar"

    def __init__(self):

        driver = webdriver.Edge()
        self.driver = driver
        self.url = self.URL

    def navigate_to(self) -> None:
        """ Navigate to self.url """

        self.driver.get(self.url)

    def find_dropdown(self) -> list[WebElement]:
        """ Find the court selection dropdown and returns its list of its options """

        drp = self.driver.find_element(By.ID, 'optionCountyCourt')
        opts = drp.find_elements(By.TAG_NAME, 'option')[1:] # remove first option (value="0")
        return opts
    
    def create_dict(self, opts: list[WebElement]) -> dict[str, str]:
        """ Creates a dict from the dropdown choices {code: name} """

        return {
            opt.get_dom_attribute('value').replace(':', '%3A'): opt.text.strip() 
            for opt in opts
        }
    
    def save_to_json(self, court_dict: dict[str, str]) -> str:
        """ Saves to json """

        base_dir = Path(__file__).resolve().parent.parent
        path = base_dir / "config" / "data" / "court_codes.json"
        
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(court_dict, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return str(path)

    def run(self) -> None:
        """ Runner """
        try:
            self.navigate_to()
            opts = self.find_dropdown()
            court_dict = self.create_dict(opts)
            self.save_to_json(court_dict=court_dict)
            logger.info("court_codes.json saved")
        except Exception as e:
            logger.error("Error saving court_codes.json")
            raise(f"Error saving court_codes.json: {e}") from e
        
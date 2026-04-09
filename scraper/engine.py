import pyautogui
import pyperclip
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from .parser import WebcrimsParser
from .courts import COURT_CODE_LOOKUP

class WebcrimsBot:
    """
    Args:
        court_codes: list of encoded court codes
        num_days: amount of days to extract from calendar
    """
    def __init__(self, court_codes: list[str], num_days: int, wait_time: int):
        
        self.court_codes = court_codes
        self.num_days = num_days
        self.wait_time = wait_time

        self.start_date = datetime.today()
        self.end_date = (self.start_date + timedelta(days=self.num_days))
    
    def build_url(self, court_code: str) -> str:
        """ Builds the URL to navigate to """
        start_date_str = self.start_date.strftime('%m/%d/%Y')
        end_date_str = self.end_date.strftime('%m/%d/%Y')
        
        return (
        "https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar"
        f"?optionCountyCourt={court_code}"
        f"&dc={start_date_str}"
        f"&td={end_date_str}"
        )
    
    def open_chrome(self) -> None:
        " Opens an instance of a Chrome browser "
        pyautogui.press("win")
        pyautogui.write("chrome")
        pyautogui.press("enter")
        pyautogui.sleep(3)

    def navigate_to_url(self, url: str) -> None:
        """ Navigates to URL """
        pyautogui.hotkey("ctrl", "l")
        pyautogui.write(url)
        pyautogui.press("enter")
        pyautogui.sleep(3)
    
    def submit_current_form(self) -> None:
        """ Logic to submit the current form """
        # Select all judges
        pyautogui.press('tab', presses=22)
        pyautogui.hotkey('ctrl', 'a')

        # Submit
        pyautogui.press('tab')
        pyautogui.press('enter')
        pyautogui.sleep(self.wait_time) # Wait for results to load
    
    def get_page_html(self) -> BeautifulSoup:
        """ Extracts the current page's HTML, returns it as a BeautifulSoup object to be parsed """

        pyperclip.copy('')
         # open DevTools
        pyautogui.press('f12')
        pyautogui.sleep(2)

        # focus console (Ctrl + `)
        pyautogui.hotkey('ctrl', '`')
        pyautogui.sleep(1)

        # type JS to get full HTML
        pyautogui.write("copy(document.querySelector('*').outerHTML)")
        pyautogui.press('enter')

        pyautogui.sleep(1)

        # close DevTools 
        pyautogui.press('f12')
        pyautogui.sleep(1)

        html = pyperclip.paste()
        return BeautifulSoup(html, 'html.parser')

    def run(self) -> pd.DataFrame:
        """ Submit for all courts initialized in self.court_codes """
        print("Starting Webcrims extract...")
        print(f" Start date: {self.start_date.strftime('%m/%d/%Y')}\tEnd date: {self.end_date.strftime('%m/%d/%Y')}")

        # Collect all dfs
        dataframes = []
        
        parser = WebcrimsParser()
        self.open_chrome()
        for court_code in self.court_codes:
            court_name = COURT_CODE_LOOKUP.get(court_code, "Unknown Court")
            print(f"Extracting court calendar for {court_name}...")

            # Extract
            url = self.build_url(court_code)
            self.navigate_to_url(url)
            self.submit_current_form()
            html_soup = self.get_page_html()
            df = parser.create_dataframe(soup=html_soup, court_name=court_name)
            print(f"{df.shape[0]} dockets found for {court_name}")
            dataframes.append(df)

        return pd.concat(dataframes)




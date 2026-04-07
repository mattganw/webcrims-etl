from datetime import datetime, timedelta
import pyautogui
from bs4 import BeautifulSoup
import pyperclip


class WebcrimsBot:
    """
    Args:
        court_codes: list of encoded court codes
        num_days: amount of days to extract
    """
    def __init__(self, court_codes: list[str], num_days: int = 0):
        
        self.court_codes = court_codes
        self.start_date = datetime.today()
        self.end_date = (self.start_date + timedelta(days=num_days))
    
    def build_url(self, county_code) -> str:
        """ Builds the URL to navigate to """
        start_date_str = self.start_date.strftime('%m/%d/%Y')
        end_date_str = self.end_date.strftime('%m/%d/%Y')
        
        return (
        "https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar"
        f"?optionCountyCourt={county_code}"
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
        pyautogui.sleep(15) # Wait for results to load
    
    def get_page_html(self) -> BeautifulSoup:
        """ Extracts the current page's HTML, returns it as a BeautifulSoup object to be parsed """
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
        print(html)
        return BeautifulSoup(html, 'html.parser')

    def submit_all(self):
        """ Submit for all courts initialized in self.court_codes """
        self.open_chrome()
        for county_code in self.court_codes:
            url = self.build_url(county_code)
            self.navigate_to_url(url)
            self.submit_current_form()
            self.get_page_html()
    
if __name__ == "__main__":
    # "NY051043J%3AU", "NY051053J%3AU"
    court_codes = ["NY051033J%3AU"]
    bot = WebcrimsBot(court_codes=court_codes)
    bot.submit_all()



import pyautogui
import pyperclip
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from controller import (
    insert_data,
    merge_data
)


def submit_form():
    """ Visits Webcrims and submits the form using pyautogui """
    start_date = datetime.today()
    start_date_str = datetime.today().strftime('%m/%d/%Y')

    end_date = start_date + timedelta(days=7)
    end_date_str = end_date.strftime('%m/%d/%Y')

    url = f"https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar?optionCountyCourt=NY051033J%3AU&dc={start_date_str}&td={end_date_str}"

    pyautogui.press('win')
    pyautogui.sleep(2)
    pyautogui.write('chrome')
    pyautogui.press('enter')
    pyautogui.sleep(2)
    pyautogui.write(url)
    pyautogui.press('enter')
    pyautogui.sleep(3)
    pyautogui.press("tab", presses=21)
    pyautogui.press("down", presses=2)

    # Select court parts ( 25 limit )
    pyautogui.keyDown("ctrl")
    for _ in range(15):
        pyautogui.press('down')
        pyautogui.press('space')
    pyautogui.keyUp("ctrl")
    
    # Submit
    pyautogui.press('tab', presses=2)
    pyautogui.press('enter')
    pyautogui.sleep(15) # Wait for results to load

def extract_html():
    """ Extracts and returns full HTML of the page """
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
    return html

def create_dataframe(soup):
    """ Converts HTML tables into a dataframe object """
    data = []

    cols = ['Docket', 'CourtPart', 'Defendant', 'CalendarSection', 'Judge', 'CourtDate']

    tables = soup.find_all('table')
    for table in tables:
        date = table.find('caption').text.strip()
        body = table.find('tbody')
        for row in body.find_all('tr')[1:]: # skip header
            cells = [td.text.strip() for td in row.find_all('td')]
            if cells:
                data.append(cells + [date])

    df = pd.DataFrame(data, columns=cols)

    # Convert 'April 09, 2026' → datetime.date(2026, 4, 9)
    df['CourtDate'] = pd.to_datetime(df['CourtDate'], format='%B %d, %Y', errors='coerce').dt.date
    # Replace asterisks *
    df['CalendarSection'] = df['CalendarSection'].apply(lambda x: x.replace('*', '') if isinstance(x, str) else x)

    return df

if __name__ == "__main__":

    # 1. Submit form and extract HTML tables
    submit_form()
    html = extract_html()
    soup = BeautifulSoup(html, 'html.parser')

    # 2. Create dataframe
    df = create_dataframe(soup=soup)
    #pd.set_option('display.max_rows', None)
    #print(df)

    # 3. Insert into SQL db into staging
    insert_data(df)

    # 4. Merge changes
    merge_data()

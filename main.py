import pyautogui
import pyperclip
import pandas as pd
from bs4 import BeautifulSoup

from controller import insert_data


# https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar?optionCountyCourt=NY051033J%3AU&dc={lstDates[0]}&td={lstDates[-1]}

def submit_form():
    """ Visits Webcrims and submits the form using pyautogui """
    url = "https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar?optionCountyCourt=NY051033J%3AU&dc=04/03/2026&td=04/09/2026"
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
    pyautogui.sleep(30) # Wait for results to load

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

    # Convert 'April 09, 2026' → '2026-04-09'
    df['CourtDate'] = pd.to_datetime(df['CourtDate'], format='%B %d, %Y').dt.strftime('%Y-%m-%d')
    # Replace asterisks *
    df['CalendarSection'] = df['CalendarSection'].apply(lambda x: x.replace('*', ''))

    return df

if __name__ == "__main__":

    # 1. Submit form and extract HTML tables
    submit_form()
    html = extract_html()
    soup = BeautifulSoup(html, 'html.parser')

    # 2. Create dataframe
    df = create_dataframe(soup=soup)

    # 3. Insert into SQL db
    # TODO: Use MERGE to handle updates and state
    # Need to create staging table to merge results
    # TRUNCATE TABLE before each load

    
    insert_data(df)
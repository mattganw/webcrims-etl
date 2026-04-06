import pyautogui
import pyperclip
import pandas as pd
import sys
import traceback
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from controller import (
    insert_data,
    merge_data
)

def submit_form() -> None:
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
    for _ in range(24):
        pyautogui.press('down')
        pyautogui.press('space')
    pyautogui.keyUp("ctrl")
    
    # Submit
    pyautogui.press('tab', presses=2)
    pyautogui.press('enter')
    pyautogui.sleep(30) # Wait for results to load

def extract_html() -> str:
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

def create_dataframe(soup: BeautifulSoup) -> pd.DataFrame:
    """ Converts HTML tables into a DataFrame """
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

def main() -> None:
    """ Main pipeline """
    try:
        # Submit form and extract HTML tables
        submit_form()
        html = extract_html()
        soup = BeautifulSoup(html, 'html.parser')

        # Create DataFrame
        df = create_dataframe(soup=soup)
        print(f"{df.shape[0]} dockets found")

        if df.empty:
            raise Exception("No dockets found")

        inserted_count = insert_data(df)
        print(f"{inserted_count} rows inserted into staging")

        merge_data()
        print("Merged into Webcrims")

    except Exception as e:
        print(f"Error running pipeline: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

import pyautogui
import pyperclip
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from controller import (
    insert_data,
    merge_data
)

from main_helper import (
    get_num_courtparts
)

TOTAL_PARTS = get_num_courtparts()
BATCH_SIZE = 25

def submit_form(limit: int = 25, offset: int = 0) -> None:
    """ Visits Webcrims and submits the form using pyautogui """

    if limit > 25:
        raise ValueError("Limit cannot be greater than 25")
    
    start_date = datetime.today()
    start_date_str = datetime.today().strftime('%m/%d/%Y')

    end_date = start_date + timedelta(days=7)
    end_date_str = end_date.strftime('%m/%d/%Y')

    url = f"https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar?optionCountyCourt=NY051033J%3AU&dc={start_date_str}&td={end_date_str}"

    # Start chrome
    pyautogui.press('win')
    pyautogui.sleep(2)
    pyautogui.write('chrome')
    pyautogui.press('enter')
    pyautogui.sleep(2)
    
    # Navigate to URL
    pyautogui.write(url)
    pyautogui.press('enter')
    pyautogui.sleep(3)

    # Tab to court part dropdown with an offset to focus on correct <option>
    pyautogui.press("tab", presses=21)
    pyautogui.press("down", presses=offset + 2)

    # Select court parts ( 25 limit )
    pyautogui.keyDown("ctrl")
    for _ in range(limit - 1):
        pyautogui.press('down')
        pyautogui.press('space')
    pyautogui.keyUp("ctrl")
    
    # Submit
    pyautogui.press('tab', presses=2)
    pyautogui.press('enter')
    pyautogui.sleep(30) # Wait for results to load

def extract_soup() -> BeautifulSoup:
    """ Returns full HTML of the page as a BeautifulSoup object """
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

def create_dataframe(soup: BeautifulSoup) -> pd.DataFrame:
    """ Cleans and transforms HTML tables into a DataFrame """
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

def extract_webcrims(total_parts: int, batch_size: int) -> pd.DataFrame:
    """ Uses a batch run to extract all court parts and collects the results into a DataFrame """
    dfs = []
    try:
        batches = range(0, total_parts, batch_size)
        for start in batches:
            limit = min(batch_size, total_parts - start)
            submit_form(limit=limit, offset=start)
            soup = extract_soup()
            df = create_dataframe(soup=soup)
            dfs.append(df)
    except Exception:
        raise
    
    df_final = pd.concat(dfs, ignore_index=True)
    print(f"{df_final.shape[0]} dockets extracted from website")

    return df_final

def load_webcrims(df: pd.DataFrame) -> None:
    """ Loads and merges DataFrame into dbo.Webcrims_Staging """
    inserted_count = insert_data(df)
    print(f"{inserted_count} rows inserted into dbo.Webcrims_Staging")

    merge_data()
    print("dbo.Webcrims_Staging successfully merged into dbo.Webcrims")

def run() -> None:
    """ ETL pipeline """
    # Extract, transform clean
    df = extract_webcrims(TOTAL_PARTS, BATCH_SIZE)

    # Load
    load_webcrims(df)

if __name__ == "__main__":
    run()

    
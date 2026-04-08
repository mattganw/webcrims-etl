from bs4 import BeautifulSoup
import pandas as pd

class WebcrimsParser:
    def __init__(self):
        self.dataframes: list[pd.DataFrame] = []

    def create_dataframe(self, soup: BeautifulSoup, court_name: str) -> pd.DataFrame:
        """ Cleans and transforms HTML tables into a DataFrame """
        data = []

        cols = ['Docket', 'CourtPart', 'Defendant', 'CalendarSection', 'Judge', 'CourtDate', 'Court']

        tables = soup.find_all('table')
        for table in tables:
            date = table.find('caption').text.strip()
            body = table.find('tbody')
            for row in body.find_all('tr')[1:]: # skip header
                cells = [td.text.strip() for td in row.find_all('td')]
                if cells:
                    data.append(cells + [date] + [court_name])

        df = pd.DataFrame(data, columns=cols)

        # Convert 'April 09, 2026' → datetime.date(2026, 4, 9)
        df['CourtDate'] = pd.to_datetime(df['CourtDate'], format='%B %d, %Y', errors='coerce').dt.date
        # Replace asterisks *
        df['CalendarSection'] = df['CalendarSection'].apply(lambda x: x.replace('*', '') if isinstance(x, str) else x)

        return df
from pathlib import Path
import os
import json
import pandas as pd

from config import Settings
from database import MSSQLConnection
from database import DBController

class Archive:
    def __init__(self):
        user_str = os.environ.get('USERNAME')
        self.path = Path(fr"C:\Users\{user_str}\Suffolk County NY\ISMUInitiatives - Initiatives Library\FP1 - Case Notes\CourtCases")

        self.data = None

    def create_dataframe(self) -> None:
        json_files = []
        dataframes = []

        # Scan folder, clean up files 
        for file in self.path.iterdir():
            if file.is_file() and 'PRIMIANO' not in file.name:
                json_files.append(file)
        
        # Open files, save data to a DataFrame
        for file in json_files:
            with open(file, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                df = pd.DataFrame(data)
                #df['CourtDate'] = pd.to_datetime(df['CourtDate'])
                dataframes.append(df)
        
        df = pd.concat(dataframes)

        # Convert to date
        
        df['CourtDate'] = (
            pd.to_datetime(df['CourtDate'].replace('', pd.NA), errors='coerce')
            .dt.strftime('%Y-%m-%d')
            .fillna('') 
        )

        df['DefendantDOB'] = (
            pd.to_datetime(df['DefendantDOB'].replace('', pd.NA), errors='coerce')
            .dt.strftime('%Y-%m-%d')
            .fillna('') 
        )

        df = df.fillna('')

        return df
    
    def save_to_archives(self, df: pd.DataFrame) -> None:
        settings = Settings()
        conn = MSSQLConnection(settings.db_connection_string)
        controller = DBController(conn)

        controller.insert_archives(df)

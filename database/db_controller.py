from .connection import MSSQLConnection
import pandas as pd

class DBController():
    def __init__(self, connection: MSSQLConnection): 
        self.connection = connection

    def insert_staging(self, df: pd.DataFrame) -> int:
        """ Inserts DataFrame into dbo.Webcrims_Staging, returns amount of rows inserted """

        if df.empty:
            raise Exception("Empty DataFrame. Cannot insert")
        
        insert_sql = '''
            INSERT INTO Webcrims_Staging (
                Docket, 
                CourtPart, 
                Defendant, 
                CalendarSection, 
                Judge, 
                CourtDate, 
                Court
            )
            VALUES (
                NULLIF(?, ''), 
                NULLIF(?, ''), 
                NULLIF(?, ''), 
                NULLIF(?, ''), 
                NULLIF(?, ''), 
                NULLIF(?, ''), 
                NULLIF(?, '')
            );
            '''
        
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_sql, df.values.tolist())
            conn.commit()
            print(f"{df.shape[0]} rows inserted into dbo.Webcrims_Staging")

        return df.shape[0]
    
    def truncate_staging(self) -> None:
        """ Truncate dbo.Webcrims_Staging """
        truncate_sql = "TRUNCATE TABLE dbo.Webcrims_Staging;"

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(truncate_sql)
            conn.commit()
            print("Truncated dbo.Webcrims_Staged")

    def merge_tables(self) -> None:
        """ Merges dbo.Webcrims_Staging into dbo.Webcrims """

        merge_sql = '''
            MERGE dbo.Webcrims AS target
            USING dbo.Webcrims_Staging AS source
            ON target.Docket = source.Docket

            WHEN MATCHED THEN
            UPDATE SET 
                target.CourtPart = source.CourtPart,
                target.Defendant = source.Defendant,
                target.CalendarSection = source.CalendarSection,
                target.Judge = source.Judge,
                target.CourtDate = source.CourtDate,
                target.Court = source.Court,
                target.Active = 1,
                target.ModifiedAt = SYSDATETIME()
                
            WHEN NOT MATCHED BY TARGET THEN
            INSERT (Docket, CourtPart, Defendant, CalendarSection, Judge, CourtDate, Court, Active)
            VALUES (source.Docket, source.CourtPart, source.Defendant, source.CalendarSection, source.Judge, source.CourtDate, source.Court, 1)
            
            WHEN NOT MATCHED BY SOURCE THEN
            UPDATE SET
                target.Active = 0,
                target.ModifiedAt = SYSDATETIME();
        '''

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT TOP (1) 1 FROM dbo.Webcrims_Staging;")
            is_empty = cursor.fetchone() is None
            if is_empty:
                raise Exception("Staging table is empty. Cannot perform merge.")
            
            cursor.execute(merge_sql)
            conn.commit()
            print("dbo.Webcrims_Staging merged into dbo.Webcrims")
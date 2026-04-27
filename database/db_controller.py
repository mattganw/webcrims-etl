"""
DBController class to handle and perform db operations using a MSSQLConnection
    Defined methods/operations:
        - INSERT
        - MERGE
        - TRUNCATE
"""

from .connection import MSSQLConnection
import pandas as pd
from config import logger

class DBController():
    def __init__(self, connection: MSSQLConnection): 
        self.connection = connection

    def insert_archives(self, df: pd.DataFrame) -> int:
        """ Inserts DataFrame into dbo.Webcrims_Archive, returns amount of rows inserted """
        if df.empty:
            logger.error("Empty DataFrame. Cannot insert.")
            raise Exception("Empty DataFrame. Cannot insert")
        
        
        insert_sql = """
            INSERT INTO dbo.Webcrims_Archive (
                Docket, 
                Defendant, 
                DefendantDOB,
                ADA,
                ADAEmail,
                PCMSLink,
                CaseNotes,
                QuickNotes,
                NotesToProsecutor,
                Charges,
                CourtDate,
                CourtPart
            )
            VALUES (
                NULLIF(?, ''),  -- Docket
                NULLIF(?, ''),  -- Defendant
                NULLIF(?, ''),  -- DefendantDOB 
                NULLIF(?, ''),  -- ADA
                NULLIF(?, ''),  -- ADAEmail
                NULLIF(?, ''),  -- PCMSLink
                NULLIF(?, ''),  -- CaseNotes
                NULLIF(?, ''),  -- QuickNotes
                NULLIF(?, ''),  -- NotesToProsecutor
                NULLIF(?, ''),  -- Charges
                NULLIF(?, ''),  -- CourtDate 
                NULLIF(?, '')   -- CourtPart
            );
        """

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_sql, df.values.tolist())
            conn.commit()
            row_count = df.shape[0]
            logger.info(f"{row_count} rows inserted into dbo.Webcrims_Archive")

        return df.shape[0]


    def insert_staging(self, df: pd.DataFrame) -> int:
        """ Inserts DataFrame into dbo.Webcrims_Staging, returns amount of rows inserted """

        if df.empty:
            logger.error("Empty DataFrame. Cannot insert.")
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
            row_count = df.shape[0]
            logger.info(f"{row_count} rows inserted into dbo.Webcrims_Staging")

        return df.shape[0]
    
    def truncate_staging(self) -> None:
        """ Truncate dbo.Webcrims_Staging """
        truncate_sql = "TRUNCATE TABLE dbo.Webcrims_Staging;"

        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(truncate_sql)
            conn.commit()
            logger.info("dbo.Webcrims_Staging truncated.")

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
                logger.error("Staging table is empty. Cannot perform merge.")
                raise Exception("Staging table is empty. Cannot perform merge.")
            
            cursor.execute(merge_sql)
            conn.commit()
            logger.info("dbo.Webcrims_Staging merged into dbo.Webcrims")
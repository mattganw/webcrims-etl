from database import connect_to_db
import pandas as pd

def fetch_webcrims() -> pd.DataFrame:
    """ Fetches dbo.Webcrims and returns it as a DataFrame """

    query = '''SELECT * FROM dbo.Webcrims;'''
    cols = ['ID', 'Docket', 'CourtPart', 'Defendant', 'CalendarSection', 'Judge', 'CourtDate', 'Active', 'CreatedAt', 'ModifiedAt']
    
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    return pd.DataFrame(rows, columns=cols)

def insert_data(df: pd.DataFrame) -> int:
    """ Inserts DataFrame into dbo.Webcrims_Staging, returns amount of rows inserted """

    if df.empty:
        raise Exception("Empty dataframe")
    
    insert_sql = '''
        INSERT INTO Webcrims_Staging (Docket, CourtPart, Defendant, CalendarSection, Judge, CourtDate)
        VALUES (
            NULLIF(?, ''), 
            NULLIF(?, ''), 
            NULLIF(?, ''), 
            NULLIF(?, ''), 
            NULLIF(?, ''), 
            NULLIF(?, '')
        );
        '''
    
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(insert_sql, df.values.tolist())
            conn.commit()
    return df.shape[0]

def merge_data() -> None:
    """ Merges dbo.Webcrims_Staging into dbo.Webcrims, and then truncates dbo.Webcrims_Staging """

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
            target.Active = 1,
            target.ModifiedAt = SYSDATETIME()
            
        WHEN NOT MATCHED BY TARGET THEN
        INSERT (Docket, CourtPart, Defendant, CalendarSection, Judge, CourtDate, Active)
        VALUES (source.Docket, source.CourtPart, source.Defendant, source.CalendarSection, source.Judge, source.CourtDate, 1)
        
        WHEN NOT MATCHED BY SOURCE THEN
        UPDATE SET
            target.Active = 0,
            target.ModifiedAt = SYSDATETIME();
    '''

    truncate_sql = "TRUNCATE TABLE dbo.Webcrims_Staging;"

    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT TOP (1) 1 FROM dbo.Webcrims_Staging;")
            is_empty = cursor.fetchone() is None

            if is_empty:
                raise Exception("Staging table is empty. Cannot perform merge.")
            
            cursor.execute(merge_sql)
            cursor.execute(truncate_sql)

            conn.commit()

if __name__ == "__main__":
    pass
from database import connect_to_db

def fetch_webcrims():
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Webcrims_Staging;")
        for row in cursor.fetchall():
            print(row)
    except Exception:
        raise
    finally:
       conn.close()

def insert_data(df):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

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

        cursor.executemany(insert_sql, df.values.tolist())
        conn.commit()
    except Exception:
        raise
    finally:
        conn.close()

def merge_data():
    conn = None
    try:

        conn = connect_to_db()
        cursor = conn.cursor()

        merge_sql = '''
        MERGE Webcrims AS target
        USING Webcrims_Staging AS source
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
        truncate_sql = '''TRUNCATE TABLE dbo.Webcrims_Staging;'''
        cursor.execute(merge_sql)
        cursor.execute(truncate_sql)
        conn.commit()
    except Exception:
        raise
    finally:
        conn.close()
        

if __name__ == "__main__":
    #fetch_webcrims()
    #insert_data()
    #merge_data()
    pass
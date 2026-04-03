from database import connect_to_db

def fetch_data():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Webcrims;")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def insert_data(df):
    conn = connect_to_db()
    cursor = conn.cursor()

    insert_sql = '''
    INSERT INTO Webcrims (Docket, CourtPart, Defendant, CalendarSection, Judge, CourtDate)
    VALUES (?, ?, ?, ?, ?, ?)
    '''

    cursor.executemany(insert_sql, df.values.tolist())
    cursor.commit()
    conn.close()

if __name__ == "__main__":
    #insert_data()
    fetch_data()
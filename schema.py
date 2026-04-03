from database import connect_to_db

if __name__ == "__main__":

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE Webcrims (
            ID INT IDENTITY(1, 1) PRIMARY KEY,
            Docket NVARCHAR(255) NOT NULL,
            CourtPart NVARCHAR(255),
            Defendant NVARCHAR(255), 
            CalendarSection NVARCHAR(255),
            Judge NVARCHAR(255), 
            CourtDate DATE,
            Active BIT NOT NULL DEFAULT 1,
            CreatedAt DATETIME NOT NULL DEFAULT SYSDATETIME()
        )
    ''')
    
    conn.commit()
    conn.close()

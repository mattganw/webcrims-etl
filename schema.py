from database import connect_to_db

if __name__ == "__main__":

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('''
        IF NOT EXISTS (
            SELECT 1 
            FROM sys.tables 
            WHERE name = 'Webcrims'
        )
        BEGIN
            CREATE TABLE Webcrims (
                ID INT IDENTITY(1, 1) PRIMARY KEY,
                Docket NVARCHAR(100) NOT NULL,
                CourtPart NVARCHAR(100),
                Defendant NVARCHAR(255), 
                CalendarSection NVARCHAR(100),
                Judge NVARCHAR(255), 
                CourtDate DATE,
                Active BIT NOT NULL DEFAULT 1,
                CreatedAt DATETIME NOT NULL DEFAULT SYSDATETIME(), 
                ModifiedAt DATETIME NULL
            );
        END
    ''')

    cursor.execute('''
        IF NOT EXISTS (
            SELECT 1 
            FROM sys.tables 
            WHERE name = 'Webcrims_Staging'
        )
        BEGIN
            CREATE TABLE Webcrims_Staging (
                ID INT IDENTITY(1, 1) PRIMARY KEY,
                Docket NVARCHAR(100) NOT NULL,
                CourtPart NVARCHAR(100),
                Defendant NVARCHAR(255), 
                CalendarSection NVARCHAR(100),
                Judge NVARCHAR(255), 
                CourtDate DATE,
                CreatedAt DATETIME NOT NULL DEFAULT SYSDATETIME()
            );
        END
    ''')
    
    conn.commit()
    conn.close()

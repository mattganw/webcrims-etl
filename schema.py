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
                Docket NVARCHAR(50) NOT NULL,
                CourtPart NVARCHAR(20),
                Defendant NVARCHAR(255), 
                CalendarSection NVARCHAR(20),
                Judge NVARCHAR(255), 
                CourtDate DATE,
                Active BIT NOT NULL DEFAULT 1,
                CreatedAt DATETIME NOT NULL DEFAULT SYSDATETIME()
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
                Docket NVARCHAR(50) NOT NULL,
                CourtPart NVARCHAR(20),
                Defendant NVARCHAR(255), 
                CalendarSection NVARCHAR(20),
                Judge NVARCHAR(255), 
                CourtDate DATE,
                Active BIT NOT NULL DEFAULT 1,
                CreatedAt DATETIME NOT NULL DEFAULT SYSDATETIME()
            );
        END
    ''')
    
    conn.commit()
    conn.close()

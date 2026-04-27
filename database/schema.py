"""
DBSchema class used to initialize and reset dbo.Webcrims, dbo.Webcrims_Staging tables.
    Defined methods/operations:
        - CREATE TABLE
        - DROP TABLE
"""


from .connection import MSSQLConnection
from config import logger

class DBSchema:
    def __init__(self, connection: MSSQLConnection):
        self.connection = connection

        self.WEBCRIMS_SQL = '''
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
                Court NVARCHAR(255),
                Active BIT NOT NULL DEFAULT 1,
                CreatedAt DATETIME NOT NULL DEFAULT SYSDATETIME(), 
                ModifiedAt DATETIME NULL
            );
        END
        '''

        self.WEBCRIMS_STAGING_SQL = '''
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
                Court NVARCHAR(255),
                CreatedAt DATETIME NOT NULL DEFAULT SYSDATETIME()
            );
        END
        '''

        self.WEBCRIMS_ARCHIVE_SQL = '''
        IF NOT EXISTS (
            SELECT 1 
            FROM sys.tables 
            WHERE name = 'Webcrims_Archive'
        )
        BEGIN
            CREATE TABLE Webcrims_Archive (
                ID INT IDENTITY(1, 1) PRIMARY KEY,
                Docket NVARCHAR(MAX) NOT NULL,
                Defendant NVARCHAR(MAX),
                DefendantDOB DATETIME, 
                ADA NVARCHAR(MAX), 
                ADAEmail NVARCHAR(MAX),
                PCMSLink NVARCHAR(MAX), 
                CaseNotes NVARCHAR(MAX), 
                QuickNotes NVARCHAR(MAX), 
                NotesToProsecutor NVARCHAR(MAX), 
                Charges NVARCHAR(MAX), 
                CourtDate DATETIME, 
                CourtPart NVARCHAR(MAX),
                Active BIT NOT NULL DEFAULT 0,
                CreatedAt DATETIME NOT NULL DEFAULT SYSDATETIME(), 
            );
        END
        '''

        self.DELETE_WEBCRIMS_SQL = '''DROP TABLE IF EXISTS dbo.Webcrims;'''
        self.DELETE_WEBCRIMS_STAGING_SQL = '''DROP TABLE IF EXISTS dbo.Webcrims_Staging;'''
        self.DELETE_WEBCRIMS_ARCHIVE_SQL = '''DROP TABLE IF EXISTS dbo.Webcrims_Archive;'''


    def create_tables(self) -> None:
        """ Init schema and create tables """
        with self.connection as conn:
            cursor = conn.cursor()

            cursor.execute(self.WEBCRIMS_SQL)
            logger.info("Created dbo.Webcrims")

            cursor.execute(self.WEBCRIMS_STAGING_SQL)
            logger.info("Created dbo.Webcrims_Staging")

            cursor.execute(self.WEBCRIMS_ARCHIVE_SQL)
            logger.info("Created dbo.Webcrims_Archive")

            conn.commit()

    def delete_webcrims(self) -> None:
        """ Drops table dbo.Webcrims """
        with self.connection as conn:
            cursor = conn.cursor()

            cursor.execute(self.DELETE_WEBCRIMS_SQL)
            logger.info("Dropped dbo.Webcrims")

            conn.commit()

    def delete_webcrims_staging(self) -> None:
        """ Drops table dbo.Webcrims_Staging """
        with self.connection as conn:
            cursor = conn.cursor()

            cursor.execute(self.DELETE_WEBCRIMS_STAGING_SQL)
            logger.info("Dropped dbo.Webcrims_Staging")

            conn.commit()

    def delete_webcrims_archive(self) -> None:
        """ Drops table dbo.Webcrims_Archive """
        with self.connection as conn:
            cursor = conn.cursor()

            cursor.execute(self.DELETE_WEBCRIMS_ARCHIVE_SQL)
            logger.info("Dropped dbo.Webcrims_Archive")

            conn.commit()

    def reset(self) -> None:
        """ Hard reset by deleting all tables """
        self.delete_webcrims()
        self.delete_webcrims_staging()
        self.delete_webcrims_archive()
        logger.info("RESET: Schema reset.")


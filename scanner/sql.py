import sqlite3
import os

def create_tables(connection):
    # Get the script's directory
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # db_path = os.path.join(script_dir, 'profiles.db')

    # connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create Location Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Location (
            LocationKey INTEGER PRIMARY KEY AUTOINCREMENT,
            City TEXT,
            State TEXT
        );
    ''')

    # Create EventDate Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EventDate (
            DateKey INTEGER PRIMARY KEY AUTOINCREMENT,
            Date INTEGER,
            Year INTEGER,
            Month INTEGER,
            YearDay INTEGER,
            Day INTEGER,
            Quarter INTEGER,
            Week INTEGER,
            FYYear INTEGER,
            FYYearDay INTEGER,
            FYQuarter INTEGER,
            FYWeek INTEGER
        );
    ''')

    # Create ScanSummary Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ScanSummary (
            ScanKey INTEGER PRIMARY KEY AUTOINCREMENT,
            DateKey INTEGER,
            EventLoadStatus INTEGER,
            RunMilliseconds INTEGER,
            HttpErrorCount INTEGER,
            Status TEXT CHECK (Status IN ('ok', 'error')),
            FOREIGN KEY (DateKey) REFERENCES EventDate(DateKey)
        );
    ''')

    # Create Profile Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profile (
            ProfileKey INTEGER PRIMARY KEY AUTOINCREMENT,
            StartDate TEXT,
            EndDate TEXT,
            LinkedInId TEXT,
            IsAlum INTEGER,
            FullName TEXT,
            Location TEXT,
            connections TEXT
        );
    ''')

    # Create Observation Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Observation (
            ObservationKey INTEGER PRIMARY KEY AUTOINCREMENT,
            observationdate TEXT,
            ProfileKey INTEGER,
            Action TEXT CHECK (Action IN ('noAction', 'updated', 'error', 'newProfile', 'newBlankProfile')),
            ScanKey INTEGER,
            FOREIGN KEY (ProfileKey) REFERENCES Profile(ProfileKey),
            FOREIGN KEY (ScanKey) REFERENCES ScanSummary(ScanKey)
        );
    ''')

    # Commit
    connection.commit()

if __name__ == '__main__':
    create_tables()

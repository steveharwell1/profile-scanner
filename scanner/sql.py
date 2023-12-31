import sqlite3
import os

def create_tables(connection):
    cursor = connection.cursor()

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
            FOREIGN KEY (ProfileKey) REFERENCES Profile(ProfileKey)
        );
    ''')

    # Commit
    connection.commit()

select_most_recent_profile_by_id = """
        select * from Profile where enddate is null and linkedinID=?
        """

select_alumni_profiles_not_recently_updated = """
        select p.*
        from Profile as p
        inner join Observation as o
        on p.ProfileKey = o.ProfileKey
        GROUP BY p.LinkedInId
        HAVING MAX(p.isalum) = 1 AND MAX(o.observationdate) < DATE('now', '-' || ? || ' month')
        ORDER BY MAX(o.observationdate)
        """

select_non_alumni_profiles_not_recently_updated = """
        select p.*
        from Profile as p
        inner join Observation as o
        on p.ProfileKey = o.ProfileKey
        GROUP BY p.LinkedInId
        HAVING MAX(p.isalum) = 0 AND MAX(o.observationdate) < DATE('now', '-' || ? || ' month')
        ORDER BY MAX(o.observationdate)
        """

select_blank_profiles = """
        SELECT p.*
        FROM Profile AS p
        LEFT JOIN Observation AS o
        ON p.ProfileKey = o.ProfileKey
        GROUP BY p.linkedinid
        HAVING MAX(o.observationkey) IS NULL
        ORDER BY p.startdate
        """

add_end_date_to_stale_profile_by_id = """
        UPDATE profile SET enddate=date('now') WHERE ProfileKey=?
        """
insert_new_observation = """
        insert into Observation(observationdate, ProfileKey, Action)
        values(DATE('now'), ?, ?)
        """
insert_new_profile = """
        insert into Profile(StartDate, EndDate, Linkedinid, isalum, fullname, location, connections)
        values(date('now'), Null, ?, ?, ?, ?, ?)
        """
insert_stub_profile_by_id = """
        insert into Profile(StartDate, Linkedinid)
        values(date('now'), ?)
        """

select_profile_timeline = """
        SELECT *
        FROM profile
        WHERE linkedinid = ?
        ORDER BY profilekey DESC, startdate DESC
        """

select_all_alumni = """
        SELECT *
        FROM profile
        WHERE isalum = TRUE AND enddate IS NULL
        """
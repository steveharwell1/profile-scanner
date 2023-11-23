# Imports like sql.py and types.py
import time
from crawlertypes import Profile
import sql
import logging
logger = logging.getLogger("scanner")

class Storage:
    def __init__(self, conn):
        """
            Save the connection resource in an instance var
        """
        self.conn = conn
        sql.create_tables(conn)
        'select * from Profile where enddate is null' 
        
        
        
    def save_profile(self, profile:Profile) -> None:
        """
        Will create an observation.
        If any data has changed the old profile will have an end date added,
        and a new profile record will be made
        """
        cursor=self.conn.cursor()
        query = cursor.execute('select * from Profile where enddate is null and linkedinID=?', (profile.id,))  
        result = query.fetchone()
        if result is None:
            logger.info(f"{profile.id} not found in db. Saving new profile.")
            self._insert_profile(cursor, profile)
            self._record_observation(cursor, cursor.lastrowid, "newProfile")
        elif result[4] != profile.is_alum or result[3] != profile.id or result[5] != profile.fullname or result[6] != profile.location or result[7] != profile.connections:
            logger.info(f"{profile.id} does not match db. Saving new profile.")
            cursor.execute("""
                UPDATE profile SET enddate=date('now') WHERE ProfileKey=?
                """,
                (result[0],))
            self._insert_profile(cursor, profile)
            self._record_observation(cursor, cursor.lastrowid, "updated")
        else:
            logger.info('other state')
            self._record_observation(cursor, result[0], "noAction")
            
    def _record_observation(self, cursor, profilekey, action):
        cursor.execute("""
            insert into Observation(observationdate, ProfileKey, Action, ScanKey)
            values(DATE('now'), ?, ?, Null)
            """,
            (profilekey, action))
        self.conn.commit()


    def _insert_profile(self, cursor, profile):
        cursor.execute("""
                insert into Profile(StartDate, EndDate, Linkedinid, isalum, fullname, location, connections)
                values(date('now'), Null, ?, ?, ?, ?, ?)
                """,
                (profile.id, profile.is_alum, profile.fullname, profile.location, profile.connections))
        self.conn.commit()

    def save_blank_profile_if_unknown(self, id:str) -> None:
        """
            If not in db, create a blank record.
            Do nothing if this profile is already in the database.
        """
        cursor=self.conn.cursor()
        query = cursor.execute('select * from Profile where enddate is null and linkedinID=?', (id,))  
        result = query.fetchone()
        if result is None:
            logger.info(f"{id} not found in db. Saving new profile.")
            cursor.execute("""
                insert into Profile(StartDate, Linkedinid)
                values(date('now'), ?)
                """,
                (id, ))
            self.conn.commit()
        else:
            logger.info(f'{id} already in db')

    def delete_profile(self, id:str) -> None:
        """Do not implement at this time"""
        raise NotImplementedError('self.delete_profile not implemented')

    def get_profiles_to_update(self) -> Profile:
        """should be a generator function"""
        # DB query
        # order profiles by observation
        # oldest observation will be the next profile
        cursor=self.conn.cursor()
        while (True):
            yield from self._get_stale_alumni(cursor)
            yield from self._get_stale_non_alumni(cursor)
            yield from self._get_new_profiles(cursor)

    def _get_stale_alumni(self, cursor):
        while (True):
            query = cursor.execute("""
                                select p.LinkedInId, MAX(o.observationdate) as odate
                                from Profile as p
                                inner join Observation as o
                                on p.ProfileKey = o.ProfileKey
                                GROUP BY p.LinkedInId
                                HAVING MAX(p.isalum) = 1 AND odate < DATE('now', '-1 month')
                                ORDER BY odate
                                """)  
            result = query.fetchone()
            if result is not None:
                yield result[0] 
            else: break

    def _get_stale_non_alumni(self, cursor):
        count = 20
        while (count > 0):
            count = count - 1
            query = cursor.execute("""
                                select p.LinkedInId, MAX(o.observationdate) as odate
                                from Profile as p
                                inner join Observation as o
                                on p.ProfileKey = o.ProfileKey
                                GROUP BY p.LinkedInId
                                HAVING MAX(p.isalum) = 0 AND odate < DATE('now', '-3 month')
                                ORDER BY odate
                                """)  
            result = query.fetchone()
            if result is not None:
                yield result[0] 
            else: break

    def _get_new_profiles(self, cursor):
        count = 20
        while (count > 0):
            count = count - 1
            query = cursor.execute("""
                                SELECT p.LinkedInId, MAX(o.observationkey)
                                FROM Profile AS p
                                LEFT JOIN Observation AS o
                                ON p.ProfileKey = o.ProfileKey
                                GROUP BY p.linkedinid
                                HAVING MAX(o.observationkey) IS NULL
                                ORDER BY p.startdate
                                """)
            result = query.fetchone()
            if result is not None:
                yield result[0] 
            else:
                logger.warning('Blank profiles exhausted. This should probably never happen.')
                time.sleep(2)

    def to_csv(self, id=None, filename="") -> None:
        """
            If id, output that person's timeline.
            If no id, export the most recent record for all profiles
        """
        pass

    def to_xlsx(self, id=None, filename=""):
        """
            If id, output that person's timeline.
            If no id, export the most recent record for all profiles
        """
        pass


def main() -> None:
	print('Hello from storage.py')
if __name__ == '__main__':
    main()
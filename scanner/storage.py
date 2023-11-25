# Imports like sql.py and types.py
import pandas as pd
import time

from crawlertypes import Profile
import sql

import logging
logger = logging.getLogger("scanner")

class Storage:
    def __init__(self, conn, settings):
        """
            Save the connection resource in an instance var
        """
        self.conn = conn
        self.settings = settings
        sql.create_tables(conn)
        

    def save_profile(self, profile:Profile) -> None:
        """
        Will create an observation.
        If any data has changed the old profile will have an end date added,
        and a new profile record will be made
        """
        cursor=self.conn.cursor()
        query = cursor.execute(sql.select_most_recent_profile_by_id, (profile.id,))  
        result = query.fetchone()
        record = Profile.from_record(result)
        if record is None:
            logger.info(f"{profile.id} not found in db. Saving new profile.")
            self._insert_profile(cursor, profile)
            self._record_observation(cursor, cursor.lastrowid, "newProfile")
        elif profile != record:
            logger.info(f"{profile.id} does not match db. Saving new profile.")
            cursor.execute(sql.add_end_date_to_stale_profile_by_id, (result[0],))
            self._insert_profile(cursor, profile)
            self._record_observation(cursor, cursor.lastrowid, "updated")
        else:
            logger.info(f"{profile.id} matches db. Only recording observation.")
            self._record_observation(cursor, result[0], "noAction")
            
    def _record_observation(self, cursor, profilekey, action):
        cursor.execute(sql.insert_new_observation, (profilekey, action))
        self.conn.commit()


    def _insert_profile(self, cursor, profile):
        cursor.execute(sql.insert_new_profile, profile.to_tuple())
        self.conn.commit()

    def save_blank_profile_if_unknown(self, id:str) -> None:
        """
            If not in db, create a blank record.
            Do nothing if this profile is already in the database.
        """
        cursor=self.conn.cursor()
        query = cursor.execute(sql.select_most_recent_profile_by_id, (id,))  
        result = query.fetchone()
        if result is None:
            logger.info(f"{id} not found in db. Saving new profile.")
            cursor.execute(sql.insert_stub_profile_by_id, (id, ))
            self.conn.commit()
        else:
            logger.info(f'{id} already in db')

    def delete_profile(self, id:str) -> None:
        """Do not implement at this time"""
        raise NotImplementedError('self.delete_profile not implemented')

    def get_profiles_to_update(self) -> Profile:
        """should be a generator function"""
        cursor=self.conn.cursor()
        while (True):
            yield from self._get_stale_alumni(cursor)
            yield from self._get_stale_non_alumni(cursor, self.settings.batch_size_for_reviewing_non_alumni)
            yield from self._get_new_profiles(cursor, self.settings.batch_size_for_reviewing_new_profiles)

    def _get_stale_alumni(self, cursor):
        while (True):
            query = cursor.execute(sql.select_alumni_profiles_not_recently_updated, (self.settings.months_to_revisit_alumni,))  
            result = query.fetchone()
            if result is not None:
                yield result[0] 
            else: break

    def _get_stale_non_alumni(self, cursor,  batch_size=20):
        while (batch_size > 0):
            batch_size = batch_size - 1
            query = cursor.execute(sql.select_non_alumni_profiles_not_recently_updated, (self.settings.months_to_revisit_non_alumni,))  
            result = query.fetchone()
            if result is not None:
                yield result[0] 
            else: break

    def _get_new_profiles(self, cursor, batch_size=20):
        while (batch_size > 0):
            batch_size = batch_size - 1
            query = cursor.execute(sql.select_blank_profiles)
            result = query.fetchone()
            if result is not None:
                yield result[0] 
            else:
                logger.warning("""Blank profiles exhausted. Try restarting the scanner(ctrl+c or ctrl+z) with a search term to kick things off.""")
                logger.warning("""python scanner -s tamuc""")
                time.sleep(2)

    def to_csv(self, id=None, filename="output.csv") -> None:
        """
        If id, output that person's timeline.
        If no id, export the most recent record for all profiles
        """
        cursor = self.conn.cursor()

        if id:
            # Export timeline for a specific profile
            query = cursor.execute(sql.select_profile_timeline, (id,))
            results = query.fetchall()

            df = pd.DataFrame(results, columns=["ProfileKey", "Action", "Timestamp"])
            df.to_csv(filename, index=False)
        else:
            # Export most recent record for all profiles
            query = cursor.execute(sql.select_all_profiles)
            results = query.fetchall()

            df = pd.DataFrame(results, columns=["ProfileKey", "FirstName", "LastName", "Email", "OtherFields", "Timestamp"])
            df.to_csv(filename, index=False)

    def to_xlsx(self, id=None, filename="output.xlsx"):
        """
        If id, output that person's timeline.
        If no id, export the most recent record for all profiles
        """
        cursor = self.conn.cursor()

        if id:
            # Export timeline for a specific profile
            query = cursor.execute(sql.select_profile_timeline, (id,))
            results = query.fetchall()

            df = pd.DataFrame(results, columns=["ProfileKey", "Action", "Timestamp"])
            df.to_excel(filename, index=False, sheet_name="ProfileTimeline")
        else:
            # Export most recent record for all profiles
            query = cursor.execute(sql.select_all_profiles)
            results = query.fetchall()

            df = pd.DataFrame(results, columns=["ProfileKey", "FirstName", "LastName", "Email", "OtherFields", "Timestamp"])
            df.to_excel(filename, index=False, sheet_name="AllProfiles")

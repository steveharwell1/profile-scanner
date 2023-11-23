# Imports like sql.py and types.py
import time
from crawlertypes import Profile
import sql

import sql

class Storage:
    def __init__(self, conn):
        """
            Save the connection resource in an instance var
        """
        self.conn = conn
        sql.create_tables()
        'select * from Profile where enddate is null' 
        
        
        
    def save_profile(self, profile:Profile) -> None:
        """
        Will create an observation.
        If any data has changed the old profile will have an end date added,
        and a new profile record will be made
        """
        cursor=self.conn.cursor()
        query = cursor.execute('select * from Profile where enddate is null and linkedinID=?', profile.id)  
        result = query.fetchone()
        if result is None:
            cursor.execute('insert into Profile values(date(\'now\'),Null,?,?,?,?)',
                           profile.id, True, profile.fullname, None, None)
            
        # Check db for profile
        
        

        # If profile in db is same as current then do nothing

        # Else add end date to old profile and create new profile in db
        self.conn.execute(sql.update_profile, profile.id, profile.fullname, profile.location)
        

    def save_blank_profile_if_unknown(self, id:str) -> None:
        """
            Do nothing if this profile is already in the database.
            If not in db, create a blank record.
        """
        pass

    def delete_profile(self, id:str) -> None:
        """Do not implement at this time"""
        raise NotImplementedError('self.delete_profile not implemented')

    def get_profiles_to_update(self) -> Profile:
        """should be a generator function"""
        # DB query
        yield "https://www.linkedin.com/in/jim-brown-93478012/"
        yield "https://www.linkedin.com/in/steve-harwell/"
        yield "https://www.linkedin.com/in/roshan-d-988232144/"

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
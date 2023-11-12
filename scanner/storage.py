# Imports like sql.py and types.py
from crawlertypes import Profile

import sql

class storage:
    def __init__(self, conn):
        """
            Save the connection resource in an instance var
        """
        pass

    def save_profile(self, profile:Profile) -> None:
        """
        Will create an observation.
        If any data has changed the old profile will have an end date added,
        and a new profile record will be made
        """
        pass

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
        pass

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
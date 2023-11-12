# profile-scanner
**When you want to run an individual file run `python3 scanner/filename.py`**

**When you want to run the command line tool run `python3 scanner`**

You cannot be inside of the scanner folder with all of the `.py` files when you run the previous 2 commands.
### Listing of steps
- [x] Create Github repository
- [ ] Write `main.py` (Steve)
- [ ] Write `types.py`
- [ ] Write `crawler.py`
- [ ] Create db schema
- [ ] Write `storage.py` (Janak) [sqlite](https://docs.python.org/3/library/sqlite3.html)
- [ ] Write `pagereader.py`
- [ ] Write `profilereader.py` (Roshan) [selenium instructions](https://github.com/11bender/alumni-scraping/blob/main/alumni_scraping.ipynb)
- [ ] Write `searchreader.py` (Tapiwa) [selenium instructions](https://github.com/11bender/alumni-scraping/blob/main/alumni_scraping.ipynb)
- [ ] Write `sql.py` (Janak)
- [ ] Write `settings.py`
- [x] Write `__init__.py`
- [ ] Create requirements.txt
- [ ] Integrate VPN into the system
- [ ] Write installation instructions
- [ ] Write usage instructions
- [ ] Write modification instructions
    - [ ] Write ERD for database into documentation
## Module Structure
// Will be able to both run as a module and as main file
### main.py
```python
# import resources like settings.py

	
def main() -> None:
    """
    Should only run from the command line
    Will read from the command line and start the scraper in the
    user selected mode.
    """
    # read command line controls implemented with [argparse]
	  
    # https://docs.python.org/3/library/argparse.html
	
def automatic(...)
    ## todo setup resources
    crawler.scanprofiles()

def search_text(text):
    crawler.fromSearch(text)

def add_names(file)
    ## todo setup resources
    for id in ids:
        storage.save_blank_profile_if_unknown(id)

def update_profile(id):
    ## todo setup resources
    crawler.scanprofile(id)

def get_person(id, filename):
    ## todo setup resources
    storage.to_xlsx(id, filename)

def get_profiles(filename)
    ## todo setup resources
    storage.to_xlsx(None, filename)

if __name__ == '__main__':
    main()
```

### crawler.py
```python
class Crawler:
    def __init__(self, settings, browser, xmlparser, storage, pageReader):
	self.settings = settings
	self.browser = browser
	self.xmlparser = xmlparser
	self.storage = storage
	self.pageReader = pageReader

    def scanprofiles(self)
        for id in self.storage.get_profiles_to_update():
            time.sleep(self.settings.sleep_seconds)
            # todo Get page from id
            result = self.pageReader(page, xmlparser)
            if result.status == "ok":
                self.process_ok_result(result)

    def fromSearch(self, text)
        url = "linkedinsearchurl"
	page = self.browser.get(url)
	result = self.searchReader(page, xmlparser)
	if result.status == "ok":
            self.process_ok_result(result)

    def process_ok_result(self, result)
	self.storage.save_profile(result.profile)
	for id in result.ids:
            self.storage.save_blank_profile_if_unknown(id)

def main() -> none:
    # imports resources
    crawler = Crawler(...)
    crawler.scanprofiles()

if __name__ == '__main__':
    main()
```
### pagereader.py
```python
from abc import ABC, abstractmethod
class PageReader(ABC):
    @abstractmethod
    def scan(self, page, xmlparser):
        pass
```
### profilereader.py
```python
# Do Imports
class ProfileReader(PageReader):
    def scan(self, page, xmlparser) -> PageScanResult:

    def _page_setup(self, page) -> None:

    def _is_alum(self, page, xmlparser) -> bool:

    def _is_correct_page_type(self, page, xmlparser) -> bool:

    def _get_name(self, page, xmlparser) -> str:

    def _get_location(self, page, xmlparser) -> str:

    def _get_connections(self, page, xmlparser) -> int:

    def _get_more_ids(self, page, xmlparser) -> list[str]:


def main() -> none:
    pass

if __name__ == '__main__':
    main()
```

### storage.py
```python
# Imports like sql.py and types.py
class storage:
    def __init__(self, conn):
	"""
	   Save the connection resource in an instance var
	"""

    def save_profile(self, profile:Profile) -> None:
	"""
	   Will create an observation.
	   If any data has changed the old profile will have an end date added,
	   and a new profile record will be made
	"""

    def save_blank_profile_if_unknown(self, id:str) -> None:
	"""
	   Do nothing if this profile is already in the database.
	   If not in db, create a blank record.
	"""

    def delete_profile(self, id:str) -> None
	"""Do not implement at this time"""

    def get_profiles_to_update(self) -> Profile:
	"""should be a generator function"""

    def to_csv(self, id=None):
	"""
	   If id, output that person's timeline.
	   If no id, export the most recent record for all profiles
	"""

    def to_xlsx(self, id=None, filename):
	"""
	   If id, output that person's timeline.
	   If no id, export the most recent record for all profiles
	"""


def main() -> none:
	pass
if __name__ == '__main__':
    main()
```

### crawlertypes.py
```python
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional

class PageScanResultStatus(Enum):
    OK = "OK"
    ERR = "ERR"

@dataclass
class PageScanResult:
    """Return type for an individual page scan"""
    status: PageScanResultStatus
    profile: Optional[Profile] = None
    found_ids: list[str] #python 3.9 or later

@dataclass
class Profile:
    fullname: str
    location: str #should this be it's own datatype?
    connections: int # Not sure if int is appr. I see some listings like ">900"
```
### sql.py
```python
create_tables = """CREATE TABLE IF NOT EXISTS..."""
find_most_recent_profile = """
   SELECT * FROM profiles where id = ? and enddate=null
   """
...
```

### DB Schema

#### Observation
- ObservationKey (int)
- ProfileKey(FK)
- Action: Enum('noAction', 'updated', 'error', 'newProfile', 'newBlankProfile')
- ScanSummary(FK)
#### Profile
- ProfileKey (int)
- LinkedInId (string)
- IsAlum (bool)
- Full name (string)
- LocationKey (FK) # Or just city and state?
- Connections (int)
- Optional: ProfessionKey (FK)
- StartDate (FK)
- EndDate (FK)
#### Location
- City
- State
- etc
#### Date
- **dateKey**: int
- **date**: YYYYMMDD (int)
- **year**: YYYY
- **month**: MM
- **yearDay**: DDD
- **day**: DD
- **quarter**: Q
- **week**: WW
- **fyyear**: YYYY
- **fyyearDay**: DDD
- **fyquarter**: Q
- **fyweek**: WW

### ScanSummary
- **scanKey**: int
- **dateKey**: foreign key
- **loadedFromFile**: bool
- **runMilliseconds**: int
- **httpErrorCount**: int
- **status**: enum(ok or error code)


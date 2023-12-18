# Knowledge Base


## Database Design
The Database is implemented in SQLite for its portability and for being packaged along with Python.
The following is the current schema used for our database.

### Profile
- ProfileKey (PK)
- LinkedInId TEXT
- StartDate TEXT
- EndDate TEXT
- LinkedInId TEXT
- IsAlum INTEGER
- FullName TEXT
- Location TEXT
- Connections TEXT

### Observation
- ObservationKey (PK)
- ProfileKey (FK)
- ObservationDate TEXT
- Action TEXT


![2023-11-26-er-diagram](https://github.com/steveharwell1/profile-scanner/assets/3698156/1b1a128d-3a26-4293-8368-41edbc8c8d0c)


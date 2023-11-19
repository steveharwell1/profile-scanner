create_tables = """CREATE TABLE IF NOT EXISTS..."""
find_most_recent_profiles = """
   SELECT * FROM profiles where enddate is NULL
   """
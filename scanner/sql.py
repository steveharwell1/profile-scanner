create_tables = """CREATE TABLE IF NOT EXISTS..."""
find_most_recent_profile = """
   SELECT * FROM profiles where id = ? and enddate=null
   """
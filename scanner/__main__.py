import sqlite3
from selenium import webdriver

from crawler import Crawler
from profilereader import ProfileReader
from loginreader import LoginReader
import secrets
from searchreader import SearchReader
import settings
from storage import Storage

import logging
logger = logging.getLogger("scanner")

def main() -> None:
    """
    Should only run from the command line
    Will read from the command line and start the scraper in the
    user selected mode.
    """
    # read command line controls implemented with [argparse]
	  
    # https://docs.python.org/3/library/argparse.html
    import argparse
    from datetime import datetime
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log_level", help="Choose the level of logging.", choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"], default=settings.log_level)
    parser.add_argument("-a", "--automatic", help="Allow the scraper to manage itself.", action="store_true")
    parser.add_argument("-s", "--search", help="Start the scraper by searching for specific text.")
    parser.add_argument("-i", "--ids", help="Load a csv of LinkedIn ids in the ids column. Scraper prioritizes blank profiles in automatic mode.")
    parser.add_argument("-u", "--update_profile", help="Update one specific profile by id.")
    parser.add_argument("-g", "--get_person", help="Get an individual person's timeline in a csv file.")
    parser.add_argument("-c", "--get_current", help="Get the most current version of each person's profile in a csv file.")
    parser.add_argument("-o", "--output", help="Filename for the output file.", default=f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}-output.csv")
    args = parser.parse_args()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(args.log_level)
    settings.log_level = args.log_level
    logger.info(f'Logging level set to {args.log_level}')
    if args.search:
        logger.info(f"Running in search mode with text ({args.search})")
        do_scrape(scantype="search", text=args.search)
    elif args.ids:
        logger.info(f'Running in load mode reading from file ({args.ids})')
        add_names(args.ids)
    elif args.update_profile:
        logger.info(f'Updating profile by id ({args.update_profile})')
        update_profile(args.update_profile)
    elif args.get_person:
        logger.info(f'Getting person with id ({args.get_person}) into file ({args.output})')
        get_person(args.get_person, args.output)
    elif args.get_current:
        logger.info(f'Saving all current profiles info file ({args.output})')
        get_profiles(args.output)
    else:
        logger.info("Running in automatic mode")
        do_scrape()

def do_scrape(scantype="automatic", **kwargs):
    browser = None
    conn = None
    complete = False
    try:
        logger.info('Starting browser (Chrome) and database ({settings.db.name})')
        browser = webdriver.Chrome()
        conn = sqlite3.connect(settings.db_name)
        store = Storage(conn)
        crawler = Crawler(settings, browser, store, ProfileReader())
        crawler.single_scan(LoginReader(), username=secrets.username, password=secrets.password)
        if scantype == "search":
            crawler.single_scan(SearchReader(), **kwargs)
        crawler.scanprofiles()
        complete = True
    finally:
        if not complete:
            logger.warning("Finished without completing.")
        if browser is not None:
            browser.close()
        if conn is not None:
            conn.close()

def add_names(filename):
    ## todo setup resources
    # for id in ids:
    #     storage.save_blank_profile_if_unknown(id)
    pass

def update_profile(id):
    ## todo setup resources
    #crawler.scanprofile(id)
    pass

def get_person(id, filename):
    ## todo setup resources
    #storage.to_xlsx(id, filename)
    pass

def get_profiles(filename):
    ## todo setup resources
    #storage.to_xlsx(None, filename)
    pass

if __name__ == '__main__':
    main()
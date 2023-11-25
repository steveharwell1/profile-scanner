import sqlite3

from crawler import Crawler
from loginreader import LoginReader
from profilereader import ProfileReader
from searchreader import SearchReader
from storage import Storage
import secrets
import settings

from selenium import webdriver

import logging
logger = logging.getLogger("scanner")

def main() -> None:
    """
    Should only run from the command line
    Will read from the command line and start the scraper in the
    user selected mode.
    # https://docs.python.org/3/library/argparse.html
    """

    import argparse
    from datetime import datetime
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--automatic", help="Allow the scraper to manage itself.", action="store_true")
    parser.add_argument("-s", "--search", help="Start the scraper by searching for specific text.")
    parser.add_argument("-g", "--get_person", help="Get an individual person's timeline in an excel file.")
    parser.add_argument("-c", "--get_current", help="Get the most current version of each person's profile in an excel file.", action="store_true")
    parser.add_argument("-o", "--output", help="Filename for the output file.", default=f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}-output.xlsx")
    args = parser.parse_args()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(settings.log_level)
    logger.info(f'Logging level set to {settings.log_level}')
    if args.search:
        logger.info(f"Running in search mode with text ({args.search})")
        do_scrape(scantype="search", text=args.search)
    elif args.get_person:
        logger.info(f'Getting person with id ({args.get_person}) into file ({args.output})')
        conn = sqlite3.connect(settings.db_name)
        store = Storage(conn, settings)
        get_person(store, args.get_person, args.output)
        conn.close()
    elif args.get_current:
        logger.info(f'Saving all current profiles info file ({args.output})')
        conn = sqlite3.connect(settings.db_name)
        store = Storage(conn, settings)
        get_profiles(store, args.output)
        conn.close()
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
        store = Storage(conn, settings)
        crawler = Crawler(settings, browser, store, ProfileReader(settings))
        crawler.single_scan(LoginReader(settings), username=secrets.username, password=secrets.password)
        if scantype == "search":
            crawler.single_scan(SearchReader(settings), **kwargs)
        crawler.scanprofiles()
        complete = True
    finally:
        if not complete:
            logger.warning("Finished without completing.")
        if browser is not None:
            browser.close()
        if conn is not None:
            conn.close()

def get_person(storage: Storage, id, filename):
    storage.to_xlsx(id, filename)

def get_profiles(storage: Storage, filename):
    storage.to_xlsx(None, filename)

if __name__ == '__main__':
    main()
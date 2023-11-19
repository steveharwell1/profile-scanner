from  pagereader import PageReader
from crawlertypes import PageScanResult, PageScanResultStatus
from selenium.webdriver.common.by import By
import time
import logging
logger = logging.getLogger("scanner")

class LoginReader(PageReader):
    def scan(self, browser, **kwargs):
        logger.info('Navigating to login page.')
        browser.get("https://www.linkedin.com/login/")
        elementID = browser.find_element(By.ID, 'username')
        elementID.send_keys(kwargs['username'])
        elementID = browser.find_element(By.ID, 'password')
        elementID.send_keys(kwargs['password'])
        elementID.submit()
        logger.info(f'Waiting for {kwargs["wait"]} seconds')
        time.sleep(kwargs['wait'])
        return PageScanResult(PageScanResultStatus.SETUP, [], None)
    
def main(scantype = "automatic", **kwargs) -> None:
    from selenium.webdriver.firefox.options import Options 
    import settings
    from selenium import webdriver
    import sqlite3
    from storage import Storage
    from crawler import Crawler
    from profilereader import ProfileReader
    from searchreader import SearchReader
    import secrets

    browser = None
    conn = None
    options = Options() 
    try:
        browser = webdriver.Firefox(options)
        conn = sqlite3.connect(settings.db_name)
        store = Storage(conn)
        crawler = Crawler(settings, browser, store, ProfileReader())
        crawler.single_scan(LoginReader(), username=secrets.username, password=secrets.password, wait=settings.wait_after_login)
        if scantype == "search":
            crawler.single_scan(SearchReader(), **kwargs)
    finally:
        if browser is not None:
            browser.close()
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    main()
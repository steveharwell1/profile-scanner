from pagereader import PageReader
from crawlertypes import PageScanResult, PageScanResultStatus
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import time
from selenium.webdriver.common.keys import Keys
import logging
logger = logging.getLogger("scanner")

class SearchReader(PageReader):
    def scan(self, browser, **kwargs) -> PageScanResult:
        time.sleep(2)
        search_text = kwargs['text']
        elementID = browser.find_element(By.CSS_SELECTOR, '.search-global-typeahead__input')
        elementID.send_keys(search_text)
        time.sleep(1)
        elementID.send_keys(Keys.RETURN)
        time.sleep(3)
        ids = self._get_more_ids(browser, browser.current_url)
        logger.info(ids)
        return PageScanResult(PageScanResultStatus.OK, ids, None)


def main() -> None:
    print("Hello from searchreader.py")
    searchReader = SearchReader()
    print(searchReader.scan(None, None))

if __name__ == '__main__':
    main()
import time

from crawlertypes import PageScanResult, PageScanResultStatus
from pagereader import PageReader

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import logging
logger = logging.getLogger("scanner")

class SearchReader(PageReader):
    def scan(self, browser, **kwargs) -> PageScanResult:
        time.sleep(2)
        search_text = kwargs['text']
        elementID = browser.find_element(By.CSS_SELECTOR, self.settings.selector_for_search_input)
        elementID.send_keys(search_text)
        time.sleep(1)
        elementID.send_keys(Keys.RETURN)
        time.sleep(3)
        ids = self._get_more_ids(browser, browser.current_url)
        for id in ids:
            logger.info(f'{id} found when searching "{search_text}"')
        return PageScanResult(PageScanResultStatus.OK, ids, None)

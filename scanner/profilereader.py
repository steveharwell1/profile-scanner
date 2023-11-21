from pagereader import PageReader
from crawlertypes import PageScanResult, PageScanResultStatus, Profile
import time
import logging
logger = logging.getLogger("scanner")
from urllib.parse import urlparse
from selenium.webdriver.common.by import By

class ProfileReader(PageReader):
    def scan(self, browser, **kwargs) -> PageScanResult:
        logger.info('Navigating to profile page.')
        
        #Setup Page
        #If is alumni, get profile info
        if self._is_alum (browser):
            name = self._get_name(browser)
            logger.info(f'The user name is {name}')
            location = self._get_location(browser)
            logger.info(f'{name}\'s location is {location}')
            ids = self._get_more_ids(browser, browser.current_url)
            logger.info(ids)
            result = PageScanResult(PageScanResultStatus.OK, ids, Profile(id=browser.current_url, fullname=name, location=location))
            return result
        else:
            logger.info ("This user is not an alum")
            return PageScanResult(PageScanResultStatus.OK, [], None)

    def _page_setup(self, page) -> None:
        pass

    def _is_alum(self,browser) -> bool:
        try:
            has_tamuc_link = browser.find_element(By.CSS_SELECTOR, '.scaffold-layout__main a[href*="https://www.linkedin.com/company/36631/"]')
            return has_tamuc_link is not None
        except:
            return False

    def _get_name(self, browser) -> str:
        elem = browser.find_element(By.CSS_SELECTOR, 'h1')
        return elem.text


    def _get_location(self, browser) -> str:
        elem = browser.find_element(By.CSS_SELECTOR, '.pv-text-details__right-panel + div > span:first-of-type')
        return elem.text

    def _get_connections(self, page) -> int:
        pass

    def _get_more_ids(self, browser, current_url) -> list[str]:
        elems = browser.find_elements(By.CSS_SELECTOR, f'a[href^="https://www.linkedin.com/in/"]')
        return list(set([ urlparse(elem.get_attribute("href")).hostname + urlparse(elem.get_attribute("href")).path for elem in elems if current_url not in elem.get_attribute("href")]))

def main() -> None:
    print("Hello from profilereader.py")

if __name__ == '__main__':
    main()
from pagereader import PageReader
from crawlertypes import PageScanResult, PageScanResultStatus, Profile
import time
import logging
logger = logging.getLogger("scanner")
from selenium.webdriver.common.by import By

class ProfileReader(PageReader):
    def scan(self, browser, **kwargs) -> PageScanResult:
        logger.info('Navigating to profile page.')
        
        #Setup Page
        #If is alumni, get profile info
        if self._is_alum (browser):
            logger.info ("This user is an alum")
        else:
            logger.info ("This user is not an alum")
            
            
        time.sleep(20)
        
        #For each extra ID, add it to a list
        
        return PageScanResult(PageScanResultStatus.OK, [], None)

    def _page_setup(self, page) -> None:
        pass

    def _is_alum(self,browser) -> bool:
        is_good = True
        try:
            has_tamuc_link = browser.find_element(By.CSS_SELECTOR, '.scaffold-layout__main a[href*="https://www.linkedin.com/company/36631/"]')
        except:
            is_good = False
        return is_good
    
    def _is_correct_page_type(self, page) -> bool:
        pass

    def _get_name(self, page) -> str:
        pass

    def _get_location(self, page) -> str:
        pass

    def _get_connections(self, page) -> int:
        pass

    def _get_more_ids(self, page) -> list[str]:
        pass


def main() -> None:
    print("Hello from profilereader.py")

if __name__ == '__main__':
    main()
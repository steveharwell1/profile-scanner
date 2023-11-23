import time
import logging
from crawlertypes import PageScanResultStatus
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger("scanner")
class Crawler:
    def __init__(self, settings, browser, storage, pageReader):
        self.settings = settings
        self.browser = browser
        self.storage = storage
        self.pageReader = pageReader

    def scanprofiles(self):
        for id in self.storage.get_profiles_to_update():
            time.sleep(self.settings.anti_spam_sleep_seconds)
            logger.info (f"Searching for user {id}")
            time.sleep(self.settings.page_load_time)
            result = self.pageReader.scan(self.browser, id=id)
            if result.status == PageScanResultStatus.OK:
                logger.info(f'scan of {id} was ok')
                self.process_ok_result(result)
            else:
                logger.warning(f'scan of {id} was not ok')

    def single_scan(self, reader, **kwargs):
        result = reader.scan(self.browser, **kwargs)
        if result.status == PageScanResultStatus.OK:
            self.process_ok_result(result)

    def process_ok_result(self, result):
        if result.profile is not None:
            logger.info(f'saving profile {result.profile.id}')
            self.storage.save_profile(result.profile)
        for id in result.found_ids:
            self.storage.save_blank_profile_if_unknown(id)

def main() -> None:
    # imports resources
    #crawler = Crawler(...)
    #crawler.scanprofiles()
    print("Hello from crawler.py")

if __name__ == '__main__':
    main()
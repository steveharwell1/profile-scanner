import time
import logging
from crawlertypes import PageScanResultStatus

logger = logging.getLogger("scanner")
class Crawler:
    def __init__(self, settings, browser, storage, pageReader):
        self.settings = settings
        self.browser = browser
        self.storage = storage
        self.pageReader = pageReader

    def scanprofiles(self):
        for id in self.storage.get_profiles_to_update():
            time.sleep(self.settings.sleep_seconds)
            # todo Get page from id
            logger.info (f"Searching for user {id}")
            self.browser.get(id)
            time.sleep(self.settings.page_load_time)
            result = self.pageReader.scan(self.browser)
            if result.status == PageScanResultStatus.OK:
                logger.info('scan was ok')
                self.process_ok_result(result)
            else:
                logger.info('scan was not ok')

    def single_scan(self, reader, **kwargs):
        result = reader.scan(self.browser, **kwargs)
        if result.status == PageScanResultStatus.OK:
            self.process_ok_result(result)

    def process_ok_result(self, result):
        if result.profile is not None:
            logger.info('saving profile')
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
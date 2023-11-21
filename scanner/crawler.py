import time
import logging
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
            result = self.pageReader.scan(self.browser)
            if result.status == "ok":
                self.process_ok_result(result)

    def single_scan(self, reader, **kwargs):
        result = reader.scan(self.browser, **kwargs)
        if result.status == "ok":
            self.process_ok_result(result)

    def process_ok_result(self, result):
        if result.profile is not None:
            self.storage.save_profile(result.profile)
        for id in result.ids:
            self.storage.save_blank_profile_if_unknown(id)

def main() -> None:
    # imports resources
    #crawler = Crawler(...)
    #crawler.scanprofiles()
    print("Hello from crawler.py")

if __name__ == '__main__':
    main()
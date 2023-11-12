import time
class Crawler:
    def __init__(self, settings, browser, xmlparser, storage, pageReader):
        self.settings = settings
        self.browser = browser
        self.xmlparser = xmlparser
        self.storage = storage
        self.pageReader = pageReader

    def scanprofiles(self):
        for id in self.storage.get_profiles_to_update():
            time.sleep(self.settings.sleep_seconds)
            # todo Get page from id
            page = self.browser.get(id)
            result = self.pageReader(page, self.xmlparser)
            if result.status == "ok":
                self.process_ok_result(result)

    def fromSearch(self, search_text):
        url = "linkedinsearchurl"
        page = self.browser.get(url)
        result = self.searchReader(page, self.xmlparser, search_text)
        if result.status == "ok":
            self.process_ok_result(result)

    def process_ok_result(self, result):
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
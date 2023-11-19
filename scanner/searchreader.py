from pagereader import PageReader
from crawlertypes import PageScanResult, PageScanResultStatus

class SearchReader(PageReader):
    def scan(self, browser, **kwargs) -> PageScanResult:
        search_text = kwargs['search']
        self._page_setup(browser, **kwargs)
        ids = self._get_more_ids(browser) or []
        return PageScanResult(PageScanResultStatus.OK, ids, None)

    def _page_setup(self, browser) -> None:
        pass

    def _get_more_ids(self, page) -> list[str]:
        pass


def main() -> None:
    print("Hello from searchreader.py")
    searchReader = SearchReader()
    print(searchReader.scan(None, None))

if __name__ == '__main__':
    main()
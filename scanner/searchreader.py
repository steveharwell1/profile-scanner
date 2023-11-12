from pagereader import PageReader
from crawlertypes import PageScanResult, PageScanResultStatus

class SearchReader(PageReader):
    def scan(self, page, xmlparser) -> PageScanResult:
        self._page_setup(page)
        ids = self._get_more_ids(page, xmlparser) or []
        return PageScanResult(PageScanResultStatus.OK, ids, None)

    def _page_setup(self, page) -> None:
        pass

    def _get_more_ids(self, page, xmlparser) -> list[str]:
        pass


def main() -> None:
    print("Hello from searchreader.py")
    searchReader = SearchReader()
    print(searchReader.scan(None, None))

if __name__ == '__main__':
    main()
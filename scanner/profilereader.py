from pagereader import PageReader
from crawlertypes import PageScanResult, PageScanResultStatus, Profile

class ProfileReader(PageReader):
    def scan(self, browser, **kwargs) -> PageScanResult:
        pass

    def _page_setup(self, page) -> None:
        pass

    def _is_alum(self, page) -> bool:
        pass

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
from pagereader import PageReader
from crawlertypes import PageScanResult, PageScanResultStatus, Profile

class ProfileReader(PageReader):
    def scan(self, page, xmlparser) -> PageScanResult:
        pass

    def _page_setup(self, page) -> None:
        pass

    def _is_alum(self, page, xmlparser) -> bool:
        pass

    def _is_correct_page_type(self, page, xmlparser) -> bool:
        pass

    def _get_name(self, page, xmlparser) -> str:
        pass

    def _get_location(self, page, xmlparser) -> str:
        pass

    def _get_connections(self, page, xmlparser) -> int:
        pass

    def _get_more_ids(self, page, xmlparser) -> list[str]:
        pass


def main() -> None:
    print("Hello from profilereader.py")

if __name__ == '__main__':
    main()
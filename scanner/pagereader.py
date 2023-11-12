from abc import ABC, abstractmethod
class PageReader(ABC):
    @abstractmethod
    def scan(self, page, xmlparser):
        pass
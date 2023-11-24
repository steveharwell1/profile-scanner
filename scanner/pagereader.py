from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from abc import ABC, abstractmethod
class PageReader(ABC):

    def __init__(self, settings):
        self.settings = settings

    @abstractmethod
    def scan(self, browser):
        pass

    def _get_more_ids(self, browser, current_url) -> list[str]:
        elems = browser.find_elements(By.CSS_SELECTOR, f'a[href^="https://www.linkedin.com/in/"]:not([href^="https://www.linkedin.com/in/AC"])')
        return list(set([ 'https://' + urlparse(elem.get_attribute("href")).hostname + urlparse(elem.get_attribute("href")).path + '/' for elem in elems if current_url not in elem.get_attribute("href")]))

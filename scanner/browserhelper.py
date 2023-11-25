import time
import sys
import settings

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import logging
logger = logging.getLogger("scanner")

class BrowserHelper:
    def __init__(self, driver):
        self.get_count = 0
        self.driver = driver

    def safe_find_element(self, by, selector):
        try:
            elem = self.driver.find_element(by, selector)
            return elem
        except NoSuchElementException:
            return None
        
    def safe_find_element_by_css(self, selector):
        return self.safe_find_element(By.CSS_SELECTOR, selector)

    def safe_find_element_by_id(self, id):
        return self.safe_find_element(By.ID, id)
        
    def get(self, url) -> None:
        if self.get_count >= settings.max_page_views:
            logger.info("Hit the limit for page views today.")
            sys.exit(0)
        self.driver.get(url)
        self.get_count = self.get_count + 1
        time.sleep(settings.buffer_seconds_after_page_get)

    def wait_for(self, url, css_selector):
        try:
            WebDriverWait(self.driver, settings.max_time_for_load).until(
                EC.all_of(
                    EC.url_to_be(url),
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
            )
            time.sleep(settings.sleep_after_js_load)
        except TimeoutException:
            logger.warning(f'{url} Waited too long for page')
import time

import settings

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import logging
logger = logging.getLogger("scanner")

def safe_find_element(driver, by, selector):
    try:
        elem = driver.find_element(by, selector)
        return elem
    except NoSuchElementException:
        return None
    
def safe_find_element_by_css(driver, selector):
    return safe_find_element(driver, By.CSS_SELECTOR, selector)

def safe_find_element_by_id(driver, id):
    return safe_find_element(driver, By.ID, id)
    
def get(driver, url) -> None:
    driver.get(url)
    time.sleep(settings.buffer_seconds_after_page_get)

def wait_for(driver, url, css_selector):
    try:
        WebDriverWait(driver, settings.max_time_for_load).until(
            EC.all_of(
                EC.url_to_be(url),
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        )
        time.sleep(settings.sleep_after_js_load)
    except TimeoutException:
        logger.warning(f'{url} Waited too long for page')
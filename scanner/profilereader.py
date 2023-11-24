import time

from crawlertypes import PageScanResult, PageScanResultStatus, Profile
from pagereader import PageReader
import browserhelper

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
logger = logging.getLogger("scanner")

class ProfileReader(PageReader):
    def scan(self, browser, **kwargs) -> PageScanResult:
        id = kwargs['id']
        logger.info(f'{id} Navigating to profile page')
        #Setup Page
        #If is alumni, get profile info
        ids = []
        profile = Profile(id=id, is_alum=False)
        if self._is_alum(browser, id):
            logger.info (f"{id} is an alum")
            browser.get(id)
            try:
                WebDriverWait(browser, 10).until(
                    #EC.presence_of_element_located((By.ID, "myDynamicElement"))
                    EC.all_of(
                        EC.url_to_be(id),
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.settings.wait_for_element_on_profile_page))
                    )
                )
                time.sleep(0.5)
            except:
                logger.error(f'{id} Waited too long for page')
            name = self._get_name(browser)
            logger.info(f'{id} The user name is {name}')
            location = self._get_location(browser)
            logger.info(f'{id} {name}\'s location is {location}')
            connections = self._get_connections(browser)
            logger.info(f'{id} {name}\'s connections are {connections}')
            ids = self._get_more_ids(browser, id)
            profile = Profile(id=id, fullname=name, location=location, is_alum=True, connections=connections)
        else:
            logger.info (f"{id} is not an alum")
        return PageScanResult(PageScanResultStatus.OK, ids, profile)

    def _is_alum(self, browser, id) -> bool:
        #check is alum
        details_page = f"{id}{self.settings.education_details_path}"
        browser.get(details_page)
        try:
            WebDriverWait(browser, 10).until(
                EC.all_of(
                    EC.url_to_be(details_page),
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.settings.wait_for_element_on_education_page))
                )
            )
        except:
            logger.error(f'{details_page} Waited too long for page')
        tamuc_link = browserhelper.safe_find_element(browser, By.CSS_SELECTOR, self.settings.selector_for_is_alum)
        return tamuc_link is not None



    def _get_name(self, browser) -> str:
        elem = browserhelper.safe_find_element(browser, By.CSS_SELECTOR, self.settings.selector_for_get_name)
        if elem is None:
            logger.warning('Name not found.')
            return elem
        else:
            return elem.text


    def _get_location(self, browser) -> str:
        elem = browserhelper.safe_find_element(browser, By.CSS_SELECTOR, self.settings.selector_for_get_location)
        if elem is None:
            logger.warning('Location not found.')
            return elem
        else:
            return elem.text

    def _get_connections(self, browser) -> int:
        elem = browserhelper.safe_find_element(browser, By.CSS_SELECTOR, self.settings.selector_for_get_connections)
        if elem is None:
            logger.warning('Connections not found.')
            return elem
        else:
            return elem.text

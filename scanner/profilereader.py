import time

from crawlertypes import PageScanResult, PageScanResultStatus, Profile
from pagereader import PageReader

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
            self.browserhelper.get(id)
            self.browserhelper.wait_for(id, self.settings.wait_for_element_on_profile_page)
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
        self.browserhelper.get(details_page)
        self.browserhelper.wait_for(details_page, self.settings.wait_for_element_on_education_page)
        tamuc_link = self.browserhelper.safe_find_element_by_css(self.settings.selector_for_is_alum)
        return tamuc_link is not None

    def _get_name(self, browser) -> str:
        elem = self.browserhelper.safe_find_element_by_css(self.settings.selector_for_get_name)
        if elem is None:
            logger.warning('Name not found.')
            return elem
        else:
            return elem.text


    def _get_location(self, browser) -> str:
        elem = self.browserhelper.safe_find_element_by_css(self.settings.selector_for_get_location)
        if elem is None:
            logger.warning('Location not found.')
            return elem
        else:
            return elem.text

    def _get_connections(self, browser) -> int:
        elem = self.browserhelper.safe_find_element_by_css(self.settings.selector_for_get_connections)
        if elem is None:
            logger.warning('Connections not found.')
            return elem
        else:
            return elem.text

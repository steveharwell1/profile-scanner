import time

from crawlertypes import PageScanResult, PageScanResultStatus, Profile
from pagereader import PageReader
import browserhelper

import logging
logger = logging.getLogger("scanner")

class ProfileReader(PageReader):
    def scan(self, browser, **kwargs) -> PageScanResult:
        prev_profile = kwargs['prev_profile']
        logger.info(f'{prev_profile.id} Navigating to profile page')
        ids = []
        browserhelper.get(browser, prev_profile.id)
        browserhelper.wait_for(browser, prev_profile.id, self.settings.wait_for_element_on_profile_page)
        name = self._get_name(browser)
        logger.info(f'{prev_profile.id} The user name is {name}')
        location = self._get_location(browser)
        logger.info(f'{prev_profile.id} {name}\'s location is {location}')
        connections = self._get_connections(browser)
        logger.info(f'{prev_profile.id} {name}\'s connections are {connections}')
        ids = self._get_more_ids(browser, prev_profile.id)
        is_alum = self._is_alum(browser, prev_profile)
        profile = Profile(id=prev_profile.id, fullname=name, location=location, is_alum=is_alum, connections=connections)
        if is_alum:
            logger.info (f"{prev_profile.id} is an alum")
        else:
            logger.info (f"{prev_profile.id} is not an alum")
            ids = []
        return PageScanResult(PageScanResultStatus.OK, ids, profile)

    def _is_alum(self, browser, prev_profile) -> bool:
        if prev_profile.is_alum:
            return True
        tamuc_profile_link = browserhelper.safe_find_element_by_css(browser, self.settings.selector_for_education_area_on_profile)
        extra_experience = browserhelper.safe_find_element_by_css(browser, self.settings.selector_for_has_extended_education)
        if tamuc_profile_link is not None:
            return True
        if extra_experience is not None:
            details_page = f"{prev_profile.id}{self.settings.education_details_path}"
            browserhelper.get(browser, details_page)
            browserhelper.wait_for(browser, details_page, self.settings.wait_for_element_on_education_page)
            tamuc_link = browserhelper.safe_find_element_by_css(browser, self.settings.selector_for_is_alum)
            return tamuc_link is not None
        else:
            return False

    def _get_name(self, browser) -> str:
        elem = browserhelper.safe_find_element_by_css(browser, self.settings.selector_for_get_name)
        if elem is None:
            logger.warning('Name not found.')
            return elem
        else:
            return elem.text


    def _get_location(self, browser) -> str:
        elem = browserhelper.safe_find_element_by_css(browser, self.settings.selector_for_get_location)
        if elem is None:
            logger.warning('Location not found.')
            return elem
        else:
            return elem.text

    def _get_connections(self, browser) -> int:
        elem = browserhelper.safe_find_element_by_css(browser, self.settings.selector_for_get_connections)
        if elem is None:
            logger.warning('Connections not found.')
            return elem
        else:
            return elem.text

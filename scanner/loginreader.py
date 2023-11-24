import time

from crawlertypes import PageScanResult, PageScanResultStatus
from pagereader import PageReader
import browserhelper

import logging
logger = logging.getLogger("scanner")

class LoginReader(PageReader):
    def scan(self, browser, **kwargs):
        logger.info('Navigating to login page.')
        browserhelper.get(browser, self.settings.login_url)
        elementID = browserhelper.safe_find_element_by_id(browser, self.settings.login_username_input_id)
        elementID.send_keys(kwargs['username'])
        elementID = browserhelper.safe_find_element_by_id(browser, self.settings.login_password_input_id)
        elementID.send_keys(kwargs['password'])
        elementID.submit()
        logger.info(f'Waiting for user to perform MFA')
        while(self.settings.post_login_landing_url_snippet not in browser.current_url):
            time.sleep(.5)
        return PageScanResult(PageScanResultStatus.SETUP, [], None)
    
import time

from crawlertypes import PageScanResult, PageScanResultStatus
from pagereader import PageReader

from selenium.webdriver.common.by import By

import logging
logger = logging.getLogger("scanner")

class LoginReader(PageReader):
    def scan(self, browser, **kwargs):
        logger.info('Navigating to login page.')
        browser.get(self.settings.login_url)
        elementID = browser.find_element(By.ID, self.settings.login_username_input_id)
        elementID.send_keys(kwargs['username'])
        elementID = browser.find_element(By.ID, self.settings.login_password_input_id)
        elementID.send_keys(kwargs['password'])
        elementID.submit()
        logger.info(f'Waiting for user to perform MFA')
        while(self.settings.post_login_landing_url_snippet not in browser.current_url):
            time.sleep(1)
        return PageScanResult(PageScanResultStatus.SETUP, [], None)
    
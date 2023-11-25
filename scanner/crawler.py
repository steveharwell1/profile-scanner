import time

from crawlertypes import PageScanResultStatus

import logging
logger = logging.getLogger("scanner")

class Crawler:
    def __init__(self, settings, browser, storage, pageReader):
        self.settings = settings
        self.browser = browser
        self.storage = storage
        self.pageReader = pageReader

    def scanprofiles(self):
        for profile in self.storage.get_profiles_to_update():
            time.sleep(self.settings.sleep_between_profiles)
            logger.info (f"{profile.id} scan started")
            result = self.pageReader.scan(self.browser, prev_profile=profile)
            if result.status == PageScanResultStatus.OK:
                logger.info(f'{profile.id} scan was ok')
                self.process_ok_result(result)
            else:
                logger.warning(f'{profile.id} scan was not ok')

    def single_scan(self, reader, **kwargs):
        result = reader.scan(self.browser, **kwargs)
        if result.status == PageScanResultStatus.OK:
            self.process_ok_result(result)

    def process_ok_result(self, result):
        if result.profile is not None:
            logger.info(f'{result.profile.id} saving profile')
            self.storage.save_profile(result.profile)
        for id in result.found_ids:
            self.storage.save_blank_profile_if_unknown(id)

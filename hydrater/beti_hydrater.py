from core.interfaces.inner.hydrater import HydraterInterface
from selenium.webdriver.chrome.webdriver import WebDriver

import logging
from infra.logging import create_logger

class BetiHydrater(HydraterInterface):

    def __init__(self, logger: logging.Logger, *, js_hydrater_file):
        self.logger = logger

        self.logger.debug(f"Instantiating hydrater. Loading script from file: {js_hydrater_file}")

        with open(js_hydrater_file, 'r') as js_file:
            self.hydrater_script = js_file.read()

        self.logger.debug(f"Hydrater instantiated with script: {self.hydrater_script}")

    def hydrate(self, driver: WebDriver, *args) -> None:
        self.logger.debug(f"Executing hydrater script...")
        driver.execute_script(self.hydrater_script, *args)
        self.logger.debug(f"HydraterInterface executed successfully")
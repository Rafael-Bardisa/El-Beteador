import pathlib
from typing import Dict

from src.web_core.scraper.interfaces.inner.extracter import ExtracterInterface, typeWebDriver

import logging


class BetiExtracter(ExtracterInterface):

    def __init__(self, logger: logging.Logger, extracter_path: pathlib.Path):
        self.logger = logger

        self.logger.debug(f"Instantiating hydrater. Loading script from file: {extracter_path.name}")

        self.extracter_script = extracter_path.read_text()

        self.logger.debug(f"Extracter instantiated with script: {self.extracter_script}")

    def extract(self, driver: typeWebDriver, *args) -> Dict:
        self.logger.debug(f"Executing Extracter script...")
        result = driver.execute_script(self.extracter_script, *args)
        self.logger.debug(f"Extracter result: {result}")

        return result

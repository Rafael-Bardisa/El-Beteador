import pathlib

from src.core.types.type_webdriver import TypeWebDriver
from src.web_core.scraper.interfaces.hydrater import IHydrater

import logging


class BetiHydrater(IHydrater):

    def __init__(self, logger: logging.Logger, hydrater_path: pathlib.Path):
        self.logger = logger

        self.logger.debug(f"Instantiating hydrater. Loading script from file: {hydrater_path.name}")

        self.hydrater_script = hydrater_path.read_text()

        self.logger.debug(f"Hydrater instantiated with script: {self.hydrater_script}")

    def hydrate(self, driver: TypeWebDriver, *args) -> None:
        self.logger.debug(f"Executing Hydrater script...")
        driver.execute_script(self.hydrater_script, *args)
        self.logger.debug(f"Hydrater executed successfully")
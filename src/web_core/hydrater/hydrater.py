import pathlib
import uuid

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

        beti_signal: str = str(uuid.uuid4())
        id_injector = f'Beti.done = Beti.done.bind(Beti, "{beti_signal}");\n'

        self.logger.debug(f"Executing Hydrater script...")
        driver.execute_script(id_injector + self.hydrater_script, *args)
        # TODO set up implicit wait and test this part of the code
        driver.find_element(value=beti_signal)
        self.logger.debug(f"Hydrater executed successfully")
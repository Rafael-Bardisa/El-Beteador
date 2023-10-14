import logging
from typing import Dict

from src.core.interfaces.inner.scraper import ScraperInterface, typeWebDriver
from src.web_core.scraper.interfaces.inner.hydrater import HydraterInterface
from src.web_core.scraper.interfaces.inner.extracter import ExtracterInterface
from src.web_core.scraper.interfaces.inner.parser import ParserInterface

class BetiScraper(ScraperInterface):

    def __init__(self, logger: logging.Logger, hydrater: HydraterInterface, extracter: ExtracterInterface, parser: ParserInterface):
        self.logger = logger
        self.hydrater = hydrater
        self.extracter = extracter
        self.parser = parser

    def scrap(self, driver: typeWebDriver) -> Dict:

        self.logger.debug(f"Hydrating page")
        self.hydrater.hydrate(driver)

        self.logger.debug(f"Extracting web data")
        raw_website_data = self.extracter.extract(driver)

        self.logger.debug(f"Parsing web data")
        result = self.parser.parse(raw_website_data)

        self.logger.debug(f"Parsed web data. Result: {result}")
        return result
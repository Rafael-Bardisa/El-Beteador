import logging
from typing import Dict, List

from src.core.interfaces.scraper import IScraper, typeWebDriver
from src.web_core.scraper.interfaces.hydrater import IHydrater
from src.web_core.scraper.interfaces.extracter import IExtracter
from src.web_core.scraper.interfaces.parser import IParser

class BetiScraper(IScraper):

    def __init__(self, logger: logging.Logger, hydrater: IHydrater, extracter: IExtracter, parser: IParser):
        self.logger = logger
        self.hydrater = hydrater
        self.extracter = extracter
        self.parser = parser

    def prepare_page(self, driver: typeWebDriver) -> bool:
        self.logger.debug(f"preparing web page for scraping")
        self.hydrater.hydrate(driver)
        return True

    def scrap(self, driver: typeWebDriver) -> Dict[str, List]:
        self.logger.debug(f"Extracting web data")
        raw_website_data = self.extracter.extract(driver)

        self.logger.debug(f"Parsing web data: {raw_website_data}")
        result = self.parser.parse(raw_website_data)

        self.logger.debug(f"Parsed web data. Result: {result}")
        return result
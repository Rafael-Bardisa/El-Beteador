import logging
from typing import Dict, List

from src.core.interfaces.scraper import IScraper, TypeWebDriver
from src.web_core.scraper.interfaces.hydrater import IHydrater
from src.web_core.scraper.interfaces.extracter import IExtracter
from src.web_core.scraper.interfaces.parser import IParser

class BetiScraper(IScraper):
    """
    Concrete implementation of a Scraper that uses python and javascript code to manipulate webpages and extract match info from them
    """

    def __init__(self, logger: logging.Logger, hydrater: IHydrater, extracter: IExtracter, parser: IParser):
        self.logger = logger
        self.hydrater = hydrater
        self.extracter = extracter
        self.parser = parser

    def prepare_page(self, driver: TypeWebDriver) -> bool:

        self.logger.debug(f"preparing web page for scraping")
        self.hydrater.hydrate(driver)
        return True

    def scrap(self, driver: TypeWebDriver) -> Dict[str, List]:

        self.logger.debug(f"Extracting web data")
        raw_website_data = self.extracter.extract(driver)

        self.logger.debug(f"Parsing web data: {raw_website_data}")
        result = self.parser.parse(raw_website_data)

        self.logger.debug(f"Parsed web data. Result: {result}")
        return result
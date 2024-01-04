# main program loop, is given list of modules to use
import logging
import pathlib
from typing import Dict, List

from src.core.interfaces.module_importer import IModuleImporter
from src.core.interfaces.arithmetic_core import IArithmeticCore
from src.core.interfaces.driver_manager import IDriverManager, typeWebDriver
from src.core.interfaces.scraper import IScraper
from src.core.types.scraper_config import ScraperConfig

class BeteadorCore:
    def __init__(self
                 , logger: logging.Logger
                 , driver_manager: IDriverManager
                 , module_loader: IModuleImporter
                 , arithmetic_core: IArithmeticCore):
        self.logger = logger
        self.driver_manager = driver_manager
        self.module_loader = module_loader
        self.arithmetic_core = arithmetic_core

        self.scraper_config_options: List[ScraperConfig] = []
        self.scrapers: List[IScraper] = []

        self.driver_scraper_pairs: Dict[typeWebDriver, IScraper] = {}

    def setup(self, scrap_modules_directory: pathlib.Path):
        self.logger.debug(f"Setting up BeteadorCore. Scrap modules path: {scrap_modules_directory}")
        self.scraper_config_options, self.scrapers = self.module_loader.import_scrapers(scrap_modules_directory)

        for idx, (scraper_option, scraper) in enumerate(zip(self.scraper_config_options, self.scrapers)):
            self.logger.debug(f"creating driver")
            driver = self.driver_manager.create_driver("chrome")

            self.logger.debug(f"Opening website: {scraper_option.website['url']}")
            driver.get(scraper_option.website["url"])

            scraper.prepare_page(driver)
            self.driver_scraper_pairs[driver] = scraper

    def run(self):
        data_by_website: Dict[str, Dict[str, List]] = {}

        for scraper_option, (driver, scraper) in zip(self.scraper_config_options, self.driver_scraper_pairs.items()):
            try:
                self.logger.debug(f"Scraping website: {scraper_option.website['url']}")
                data_by_website[scraper_option.website['name']] = scraper.scrap(driver)
            except Exception as e:
                self.logger.warning(f"Exception encountered when scraping {scraper_option.website['url']}: {e}")

        self.logger.debug(f"Scraping complete. calculating arbitrage...")
        arbitrage_opportunities = self.arithmetic_core.find_arbitrage(data_by_website)
        print(arbitrage_opportunities)

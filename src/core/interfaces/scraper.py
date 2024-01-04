from abc import ABC, abstractmethod
from typing import Dict, List

from src.core.types.type_webdriver import TypeWebDriver


# scraper of web pages based on scrap_modules


class IScraper(ABC):
    """
    IScraper interface for getting relevant information from a betting website
    """
    @abstractmethod
    def prepare_page(self, driver: TypeWebDriver) -> bool:
        """
        prepares the page in the driver for scraping
        :param driver:
        :return:
        """

    @abstractmethod
    def scrap(self, driver: TypeWebDriver) -> Dict[str, List]:
        """
        Scraps match data from a given webdriver session. Assumes it is correctly aet up and hydrated
        :param driver: A chrome webdriver
        :return: dictionary containing {match: [odd 1, odd 2]}
        where match should be a consistent identifier between websites
        """

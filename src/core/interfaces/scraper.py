from abc import ABC, abstractmethod
from typing import Union, Dict, List

from selenium import webdriver

typeWebDriver = Union[webdriver.Firefox,
                      webdriver.Chrome,
                      webdriver.Edge,
                      webdriver.Safari
                      ]

# scraper of web pages based on scrap_modules


class IScraper(ABC):
    """
    IScraper interface for getting relevant information from a betting website
    """
    @abstractmethod
    def prepare_page(self, driver: typeWebDriver) -> bool:
        """
        prepares the page in the driver for scraping
        :param driver:
        :return:
        """

    @abstractmethod
    def scrap(self, driver: typeWebDriver) -> Dict[str, List]:
        """
        Scraps match data from a given webdriver session. Assumes it is correctly aet up and hydrated
        :param driver: A chrome webdriver
        :return: dictionary containing {match: [odd 1, odd 2]}
        where match should be a consistent identifier between websites
        """

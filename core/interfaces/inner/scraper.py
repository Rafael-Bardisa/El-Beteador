from abc import ABC, abstractmethod
from selenium import webdriver

from typing import Dict, Union

typeWebDriver = Union[webdriver.Firefox,
                      webdriver.Chrome,
                      webdriver.Edge,
                      webdriver.Safari
                      ]

# scraper of web pages based on scrap_modules


class ScraperInterface(ABC):
    """
    ScraperInterface interface for getting relevant information from a betting website
    """
    @abstractmethod
    def scrap(self, driver: typeWebDriver) -> Dict:
        """
        Scraps match data from a given webdriver session. Assumes it is correctly aet up and hydrated
        :param driver: A chrome webdriver
        :return: dictionary containing {match: [odd 1, odd 2]}
        where match should be a consistent identifier between websites
        """

from abc import ABC, abstractmethod
from typing import Union, Dict

from selenium import webdriver

typeWebDriver = Union[webdriver.Firefox,
                      webdriver.Chrome,
                      webdriver.Edge,
                      webdriver.Safari
                      ]

# extract data from web pages


class ExtracterInterface(ABC):
    """
    ScraperInterface interface for getting relevant information from a betting website
    """
    @abstractmethod
    def extract(self, driver: typeWebDriver, *args) -> Dict:
        """
        Scraps match data from a given webdriver session. Assumes it is correctly aet up and hydrated
        :param driver: A chrome webdriver
        :param args: Javascript parameters
        :return: dictionary containing {match: [odd 1, odd 2]}
        where match should be a consistent identifier between websites
        """

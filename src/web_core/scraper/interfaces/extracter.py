from abc import ABC, abstractmethod
from typing import Union, Dict

from selenium import webdriver

from src.core.types.type_webdriver import TypeWebDriver

# extract data from web pages


class IExtracter(ABC):
    """
    IScraper interface for getting relevant information from a betting website
    """
    @abstractmethod
    def extract(self, driver: TypeWebDriver, *args) -> Dict:
        """
        Scraps match data from a given webdriver session. Assumes it is correctly aet up and hydrated
        :param driver: A chrome webdriver
        :param args: Javascript parameters
        :return: dictionary containing {match: [odd 1, odd 2]}
        where match should be a consistent identifier between websites
        """

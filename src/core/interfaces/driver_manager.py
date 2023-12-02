from abc import ABC, abstractmethod
from typing import Union, Literal

from selenium import webdriver

typeWebDriver = Union[webdriver.Firefox,
                      webdriver.Chrome,
                      webdriver.Edge,
                      webdriver.Safari
                      ]


class IDriverManager(ABC):
    """
    Interface for implementing a class that creates and configures a webdriver for El Beteador
    """

    @abstractmethod
    def create_driver(self, driver_type: Literal["firefox", "chrome", "safari", "edge"]) -> typeWebDriver:
        """
        Loads all beteador modules from the given python package.
        :param driver_type: the type of driver to create (e.g, chrome, safari, firefox, edge
        :return: list of website urls and list of scrapers
        """

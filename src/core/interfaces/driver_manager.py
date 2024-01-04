from abc import ABC, abstractmethod
from typing import Literal

from src.core.types.type_webdriver import TypeWebDriver


class IDriverManager(ABC):
    """
    Interface for implementing a class that creates and configures a webdriver for El Beteador
    """

    @abstractmethod
    def create_driver(self, driver_type: Literal["firefox", "chrome", "safari", "edge"]) -> TypeWebDriver:
        """
        Loads all beteador modules from the given python package.
        :param driver_type: the type of driver to create (e.g, chrome, safari, firefox, edge
        :return: list of website urls and list of scrapers
        """

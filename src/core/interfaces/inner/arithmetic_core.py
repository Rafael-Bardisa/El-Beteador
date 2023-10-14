from abc import ABC, abstractmethod


class ArithmeticCoreInterface(ABC):
    """
    Interface for implementing a class that creates and configures a webdriver for El Beteador
    """

    @abstractmethod
    def idk(self):
        """
        Loads all beteador modules from the given python package.
        :return: list of website urls and list of scrapers
        """

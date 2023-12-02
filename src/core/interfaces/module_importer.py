import pathlib
from abc import ABC, abstractmethod
from typing import List, Union, Tuple

from src.core.interfaces.scraper import IScraper
from src.core.types.scraper_config import ScraperConfig


# scraper of web pages based on scrap_modules


class IModuleImporter(ABC):
    """
    Interface for loading beteador modules from python files
    """
    @abstractmethod
    def _import_scraper(self, *, module_directory: Union[pathlib.Path, str]) -> Tuple[ScraperConfig, IScraper]:
        """
        Loads a beteador module
        :param module_directory: a python module object which contains all relevant information for a beteador module
        :return: tuple containing website data and associated scraper object
        """

    @abstractmethod
    def import_scrapers(self, package_directory: Union[pathlib.Path, str]) -> Tuple[List[ScraperConfig], List[IScraper]]:
        """
        Loads all beteador modules from the given python package.
        :param package_directory: package containing all beteador modules
        :return: list of website data and list of scrapers
        """

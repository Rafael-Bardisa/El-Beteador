import pathlib
from abc import ABC, abstractmethod
from typing import List, Dict, Union

from src.core.interfaces.inner.scraper import ScraperInterface


# scraper of web pages based on scrap_modules


class ModuleImporterInterface(ABC):
    """
    Interface for loading beteador modules from python files
    """
    @abstractmethod
    def _import_scraper(self, *, module_directory: Union[pathlib.Path, str]) -> (Dict, ScraperInterface):
        """
        Loads a beteador module
        :param module_directory: a python module object which contains all relevant information for a beteador module
        :return: tuple containing website data and associated scraper object
        """

    @abstractmethod
    def import_scrapers(self, package_directory: Union[pathlib.Path, str]) -> (List[Dict], List[ScraperInterface]):
        """
        Loads all beteador modules from the given python package.
        :param package_directory: package containing all beteador modules
        :return: list of website data and list of scrapers
        """

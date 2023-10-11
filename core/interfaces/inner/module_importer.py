from types import ModuleType
from abc import ABC, abstractmethod

from core.interfaces.inner.scraper import ScraperInterface
from core.interfaces.inner.hydrater import HydraterInterface

from typing import List
# scraper of web pages based on scrap_modules


class ModuleImporterInterface(ABC):
    """
    Interface for loading beteador modules from python files
    """
    @abstractmethod
    def _import_module(self, *, module: ModuleType) -> (str, ScraperInterface, HydraterInterface):
        """
        Loads a beteador module
        :param module: a python module object which contains all relevant information for a beteador module
        :return: tuple containing website url and associated scraper object
        """

    @abstractmethod
    def import_modules(self) -> (List[str], List[ScraperInterface], List[HydraterInterface]):
        """
        Loads all beteador modules from the given python package.
        :param package: package containing all beteador modules
        :return: list of website urls and list of scrapers
        """

import pathlib
from abc import ABC, abstractmethod
from typing import Dict

from src.core.types.scraper_config import ScraperConfig


class IConfigManager(ABC):
    """
    Load a configuration file for a scraper.
    """

    @abstractmethod
    def load_config(self, config_file_path: pathlib.Path) -> ScraperConfig:
        """
        Loads the configuration file for a scraper
        :return: configuration parameters as a dict
        """

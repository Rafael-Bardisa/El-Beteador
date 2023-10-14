import pathlib
from abc import ABC, abstractmethod
from typing import Dict


class ConfigManagerInterface(ABC):
    """
    Load a configuration file for a scraper.
    """

    @abstractmethod
    def load_config(self, config_file_path: pathlib.Path) -> Dict:
        """
        Loads the configuration file for a scraper
        :return: configuration parameters as a dict
        """

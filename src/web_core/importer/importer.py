import os
from pathlib import Path
import importlib

import sys

from src.core.interfaces.module_importer import IModuleImporter
from src.core.interfaces.scraper import IScraper

from src.web_core.importer.interfaces.config_manager import IConfigManager
from src.web_core.hydrater.hydrater import BetiHydrater
from src.web_core.extracter.extracter import BetiExtracter


from typing import List, Dict, Union, Tuple

import logging

from src.web_core.scraper.interfaces.parser import IParser
from src.web_core.scraper.beti_scraper import BetiScraper

from src.core.types.scraper_config import ScraperConfig


class BetiImporter(IModuleImporter):

    def __init__(self, logger: logging.Logger, config_manager: IConfigManager, package: Union[Path, str]):
        if not (isinstance(package, Path) or isinstance(package, str)):
            raise TypeError(f"module_directory must be either Path or str, not {type(package)}")

        if isinstance(package, str):
            package = Path(package).absolute().resolve()

        self.logger = logger
        self.logger.info(f"Instantiating BetiImporter. Modules directory: {package}")
        self.config_manager = config_manager

        sys.path.append(str(package))
        self.logger.debug(f"Extended python path with scrap modules directory: {package}")

        self.scrap_modules_package = package


    def _import_scraper(self, *, module_directory: Union[Path, str]) -> Tuple[ScraperConfig, IScraper]:
        if not (isinstance(module_directory, Path) or isinstance(module_directory, str)):
            raise TypeError(f"module_directory must be either Path or str, not {type(module_directory)}")

        if isinstance(module_directory, str):
            module_directory = Path(module_directory).absolute().resolve()

        module_config = self.config_manager.load_config(module_directory / "config.yaml")

        hydrater = BetiHydrater(self.logger, module_directory / "hydrater.js")
        extracter = BetiExtracter(self.logger, module_directory / "extracter.js")
        parser: IParser = importlib.import_module(f"{module_directory.name}.parser").ModuleParser(self.logger)

        scraper = BetiScraper(self.logger, hydrater, extracter, parser)

        return module_config, scraper


    def import_scrapers(self, package_directory: Union[Path, str]) -> Tuple[List[ScraperConfig], List[IScraper]]:
        if not (isinstance(package_directory, Path) or isinstance(package_directory, str)):
            raise TypeError(f"module_directory must be either Path or str, not {type(package_directory)}")

        if isinstance(package_directory, str):
            package_directory = Path(package_directory).absolute().resolve()

        config_list: List[Dict] = []
        scraper_list: List[IScraper] = []

        self.logger.debug(f"Loading all scrapers from {package_directory}...")

        folder_list = [folder.name for folder in os.scandir(package_directory)\
                       if folder.is_dir() and not folder.name.startswith(".") and not folder.name.startswith("__")]

        self.logger.debug(f"Loading from folders: {folder_list}")

        for scrap_folder in folder_list:
            self.logger.debug(f"Loading scraper: {scrap_folder}")
            config, scraper = self._import_scraper(module_directory=package_directory / scrap_folder)

            config_list.append(config)
            scraper_list.append(scraper)

            self.logger.debug(f"Config for {scrap_folder} scraper: {config}")
            self.logger.debug(f"Scraper loaded: {scraper}")

        return config_list, scraper_list

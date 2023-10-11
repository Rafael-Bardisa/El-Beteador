from core.interfaces.inner.module_importer import ModuleImporterInterface, ModuleType
from core.interfaces.inner.scraper import ScraperInterface
from core.interfaces.inner.hydrater import HydraterInterface
from hydrater.beti_hydrater import BetiHydrater
from typing import List

import logging
from infra.logging import create_logger

from importlib import import_module

class BetiImporter(ModuleImporterInterface):

    def __init__(self, logger: logging.Logger, package: str):
        self.logger = logger
        self.logger.info(f"Instantiating BetiImporter. Module directory: {package}")
        self.scrap_modules_package = package

        self.default_hydrater_file = f"{self.scrap_modules_package}/javascript_hydraters/template_hydrater.txt"

    def _import_module(self, *, module: ModuleType) -> (str, ScraperInterface, HydraterInterface):

        try:
            url = module.url
        except AttributeError as e:
            self.logger.error(f"Could not import module: no url attribute in {module}")
            raise e

        try:
            scraper = module.ModuleScraper()
        except AttributeError as e:
            self.logger.error(f"Could not import module: no ModuleScraperInterface found in {module}")
            raise e

        try:
            hydrater = BetiHydrater(js_hydrater_file=module.hydrater_source)

        except AttributeError as e:
            self.logger.warning(f"No hydrater_source attribute found in {module}. Proceeding with default hydrater")
            hydrater = BetiHydrater(js_hydrater_file=self.default_hydrater_file)

        except FileNotFoundError as e:
            self.logger.warning(f"{module.hydrater_source} not found. Proceeding with default hydrater")
            hydrater = BetiHydrater(js_hydrater_file=self.default_hydrater_file)

        return url, scraper, hydrater

    def import_modules(self) -> (List[str], List[ScraperInterface], List[HydraterInterface]):
        beti_urls = []
        beti_scrapers = []
        beti_hydraters = []

        module_names = import_module(name=self.scrap_modules_package).__all__
        self.logger.debug(f"Importer will try to import: {module_names}")

        for module_name in module_names:
            self.logger.debug(f"Importing [{module_name}]")

            beti_module = import_module(name=f".{module_name}", package=self.scrap_modules_package)

            self.logger.debug(f"[{module_name}] imported, parsing...")

            url, scraper, hydrater = self._import_module(module=beti_module)

            self.logger.debug(f"{module_name}: loaded url [{url}]")
            self.logger.debug(f"{module_name}: loaded scraper [{scraper}]")
            self.logger.debug(f"{module_name}: loaded hydrater [{hydrater}]")

            beti_urls.append(url)
            beti_scrapers.append(scraper)
            beti_hydraters.append(hydrater)

        self.logger.debug(f"import modules finished loading urls: {beti_urls}")
        self.logger.debug(f"import modules finished loading scrapers: {beti_scrapers}")
        self.logger.info(f"import modules finished loading hydraters: {beti_hydraters}")
        self.logger.info(f"import modules finished loading modules: {module_names}")

        return beti_urls, beti_scrapers, beti_hydraters


if __name__ == "__main__":
    test = BetiImporter("scrap_modules")
    test.import_modules()
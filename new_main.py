import logging
import sys

from pathlib import Path

import configparser
config = configparser.ConfigParser()

from src.core.beteador_core import BeteadorCore
from src.core.arithmetic_core import ArithmeticCore
from src.web_core.driver.driver_manager import DriverManager
from src.web_core.importer.importer import BetiImporter
from src.web_core.config_manager.config_manager import ConfigManager


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "\033[95m%(levelname)s\033[0m %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

config.read('config.ini')

scrap_modules_directory = str(config["scrap_modules"]["directory"])

driver_manager = DriverManager(logger)
driver = driver_manager.create_driver("chrome")

config_manager = ConfigManager(logger)

module_loader = BetiImporter(logger
                             , config_manager
                             , scrap_modules_directory
                             )

arithmetic_core = ArithmeticCore(logger)

beti_core = BeteadorCore(logger
                         , driver
                         , module_loader
                         , arithmetic_core
                         )

beti_core.setup(Path(scrap_modules_directory))
beti_core.run()

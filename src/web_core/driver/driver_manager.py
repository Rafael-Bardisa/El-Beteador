import logging
from typing import Literal
from pathlib import Path

from src.core.interfaces.driver_manager import IDriverManager
from ...core.types.type_webdriver import TypeWebDriver

from .chromedriver import chrome


class DriverManager(IDriverManager):

    def __init__(self, logger: logging.Logger):
        self.logger = logger

        self.framework_folder = Path(__file__).resolve().parent / "framework"

        self.logger.debug(f"DriverManager instantiated. Framework folder: {self.framework_folder}")
        pass
    def create_driver(self, driver_type: Literal["firefox", "chrome", "safari", "edge"]) -> TypeWebDriver:
        if not driver_type in ["firefox", "chrome", "safari", "edge"]:
            raise TypeError('Driver must be one of ["firefox", "chrome", "safari", "edge"]')

        if driver_type == "firefox":
            self.logger.debug(f"Creating driver: Firefox")
            pass
        elif driver_type == "chrome":
            self.logger.debug(f"Creating driver: Chrome")
            return chrome(js_framework_path=self.framework_folder)
        elif driver_type == "safari":
            self.logger.debug(f"Creating driver: Safari")
            pass
        elif driver_type == "edge":
            self.logger.debug(f"Creating driver: Edge")
            pass
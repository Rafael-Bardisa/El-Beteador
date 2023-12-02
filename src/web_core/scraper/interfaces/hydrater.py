from selenium.webdriver.chrome.webdriver import WebDriver
from abc import ABC, abstractmethod


class IHydrater(ABC):

    @abstractmethod
    def hydrate(self, driver: WebDriver, *args) -> None:
        """
        Hydrate the DOM loaded by the driver
        :param driver:
        :return:
        """
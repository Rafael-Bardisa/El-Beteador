from src.core.types.type_webdriver import TypeWebDriver

from abc import ABC, abstractmethod


class IHydrater(ABC):
    """
    This is the common interface of all classes that can be used to prepare a web page for scraping.

    It contains only the hydrate method, which should ensure it returns when the page is correctly set up.
    """

    @abstractmethod
    def hydrate(self, driver: TypeWebDriver, *args) -> None:
        """
        Hydrate the DOM loaded by the driver. Must ensure the script is run before returning
        :param driver:
        :return:
        """
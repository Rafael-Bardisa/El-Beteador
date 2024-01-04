from src.core.types.type_webdriver import TypeWebDriver

from abc import ABC, abstractmethod


class IHydrater(ABC):

    @abstractmethod
    def hydrate(self, driver: TypeWebDriver, *args) -> None:
        """
        Hydrate the DOM loaded by the driver
        :param driver:
        :return:
        """
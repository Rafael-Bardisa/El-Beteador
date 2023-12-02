from abc import ABC, abstractmethod
from typing import Dict, List


class IArithmeticCore(ABC):
    """
    Interface for a module containing the logic to find arbitrage given odds grouped by houses
    """

    @abstractmethod
    def find_arbitrage(self, house_odds: Dict[str, Dict[str, List[float]]]):
        """
        Given dictionary of odds, find arbitrage opportunities
        :param house_odds: odds grouped by source (website)
        :return: found arbitrages
        """

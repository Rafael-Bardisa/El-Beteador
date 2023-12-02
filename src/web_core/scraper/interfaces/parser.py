from abc import ABC, abstractmethod
from typing import Dict, List


# parser of scrapped web page data


class IParser(ABC):
    """
    IParser interface for getting relevant information from a betting (?) website
    """
    @abstractmethod
    def parse(self, data: Dict) -> Dict[str, List]:
        """
        Scraps match data from a given webdriver session. Assumes it is correctly aet up and hydrated
        :return: dictionary containing {match: [odd 1, odd 2]}
        where match should be a consistent identifier between websites
        """

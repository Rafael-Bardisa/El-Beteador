from typing import Dict, List
import logging

from src.core.interfaces.arithmetic_core import IArithmeticCore


class ArithmeticCore(IArithmeticCore):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.debug(f"Arithmetic Core initialized")

    def find_arbitrage(self, house_odds: Dict[str, Dict[str, List]]):
        pass


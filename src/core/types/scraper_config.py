from dataclasses import dataclass
from typing import Dict, Literal


@dataclass(frozen=True)
class ScraperConfig:
    website: Dict[Literal["url", "name"], str]
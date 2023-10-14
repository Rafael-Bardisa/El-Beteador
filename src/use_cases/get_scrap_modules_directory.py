import logging
import os
from pathlib import Path

from src.use_cases.get_root_project_directory import get_root_project_directory


def get_scrap_modules_directory(logger: logging.Logger) -> Path:
    logger.debug(f"Searching for scrap_modules path")
    project_dir = get_root_project_directory(logger)

    for root, subdirectories, _ in os.walk(project_dir):
        logger.debug(f"Searching directory {root}")
        if "scrap_modules" in subdirectories:
            result = Path(f"{root}/scrap_modules")
            logger.debug(f"Found directory: {result}")
            return result

logger = logging.Logger(__name__, logging.CRITICAL)
logger.addHandler(logging.StreamHandler())
scrap_modules_directory = get_scrap_modules_directory(logger)

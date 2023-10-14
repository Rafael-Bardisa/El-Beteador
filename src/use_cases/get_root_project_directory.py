import logging
from pathlib import Path


def get_root_project_directory(logger: logging.Logger) -> Path:
    logger.debug(f"Accessing root project directory")
    return Path(__file__).parent.parent.parent


if __name__ == "__main__":
    logger = logging.Logger(__name__, logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    print(get_root_project_directory(logger))
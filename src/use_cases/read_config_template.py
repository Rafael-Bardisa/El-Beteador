import logging

from src.use_cases.get_scrap_modules_directory import scrap_modules_directory

def read_config_template(logger: logging.Logger):
    config_template_path = scrap_modules_directory / "config_template.txt"
    if not config_template_path.exists():
        logger.error(f"config template path not found.")
        raise FileNotFoundError(config_template_path)

    with open(config_template_path, "r") as file:
        result = file.read()
        logger.debug(f"config template: {result}")
    return result

config_template = read_config_template(logging.Logger(__name__, logging.ERROR))

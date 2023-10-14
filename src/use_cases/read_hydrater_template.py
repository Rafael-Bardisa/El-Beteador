import logging

from src.use_cases.get_scrap_modules_directory import scrap_modules_directory


def read_hydrater_template(logger: logging.Logger):
    hydrater_template_path = scrap_modules_directory / "hydrater_template.txt"
    if not hydrater_template_path.exists():
        logger.error(f"hydrater template path not found.")
        raise FileNotFoundError(hydrater_template_path)

    with open(hydrater_template_path, "r") as file:
        result = file.read()
        logger.debug(f"hydrater template: {result}")
    return result


hydrater_template = read_hydrater_template(logging.Logger(__name__, logging.ERROR))

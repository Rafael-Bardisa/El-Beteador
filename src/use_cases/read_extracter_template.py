import logging

from src.use_cases.get_scrap_modules_directory import scrap_modules_directory

def read_extracter_template(logger: logging.Logger):
    extracter_template_path = scrap_modules_directory / "extracter_template.txt"
    if not extracter_template_path.exists():
        logger.error(f"Extracter template path not found.")
        raise FileNotFoundError(extracter_template_path)

    with open(extracter_template_path, "r") as file:
        result = file.read()
        logger.debug(f"Extracter template: {result}")
    return result

extracter_template = read_extracter_template(logging.Logger(__name__, logging.ERROR))

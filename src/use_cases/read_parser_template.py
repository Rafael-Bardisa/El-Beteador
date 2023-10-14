import logging

from src.use_cases.get_scrap_modules_directory import scrap_modules_directory


def read_parser_template(logger: logging.Logger):
    parser_template_path = scrap_modules_directory / "parser_template.txt"
    if not parser_template_path.exists():
        logger.error(f"parser template path not found.")
        raise FileNotFoundError(parser_template_path)

    with open(parser_template_path, "r") as file:
        result = file.read()
        logger.debug(f"parser template: {result}")
    return result


parser_template = read_parser_template(logging.Logger(__name__, logging.ERROR))

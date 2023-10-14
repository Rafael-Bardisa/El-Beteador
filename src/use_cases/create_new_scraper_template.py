import logging
import os

from src.use_cases.get_scrap_modules_directory import scrap_modules_directory

from src.use_cases.read_hydrater_template import hydrater_template
from src.use_cases.read_extracter_template import extracter_template
from src.use_cases.read_parser_template import parser_template
from src.use_cases.read_config_template import config_template


def create_new_scraper_template(name: str, logger: logging.Logger):
    scraper_path = scrap_modules_directory / name

    if os.path.exists(scraper_path):
        logger.error(f"Cannot create new scraper: directory already exists")
        raise FileExistsError(scraper_path)

    logger.debug(f"Creating new scraper: {scraper_path}")
    os.mkdir(scraper_path)

    with open(scraper_path / "hydrater.js", 'x') as file:
        logger.debug(f"Writing hydrater template...")
        file.write(hydrater_template)

    with open(scraper_path / "extracter.js", 'x') as file:
        logger.debug(f"Writing extracter template...")
        file.write(extracter_template)

    with open(scraper_path / "parser.py", 'x') as file:
        logger.debug(f"Writing parser template...")
        file.write(parser_template.format(
            name=name,
            dict="{}",
            match_format="{match: [odd 1, odd 2]}",
            data="{data}",
            parsed_data=f"{{{name}_dict}}",
            key="{key}",
            val="{val}",
            url_fmt = "{url = !s}"
        ))

    with open(scraper_path / "config.yaml", 'x') as file:
        logger.debug(f"Writing config template...")
        file.write(config_template)


if __name__ == "__main__":
    logger = logging.Logger(__name__, logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    create_new_scraper_template("bwin", logger)

from src.web_core.driver.driver_manager import DriverManager
from typing import Dict, Union

from selenium import webdriver

typeWebDriver = Union[webdriver.Firefox,
                      webdriver.Chrome,
                      webdriver.Edge,
                      webdriver.Safari
                      ]

import logging

from src.core.interfaces.inner.scraper import ScraperInterface
import pandas

# url de la pagina:
url = 'https://www.betfred.es/ES/512/sports#bo-navigation=356554.1&action=market-group-list'



def split_match_names(names):
    
    split_names = []
    for elem in names:
        names1 = elem.split(' v ')
        match_names = []
        for i in names1:

            surnames, name = i.split(', ')
            surname = surnames.split()[0]
            name = name[0]
            match_names.append(f'{surname} {name}')
        split_names.append(f'{match_names[0]} {match_names[1]}')
    return split_names



class ModuleScraper(ScraperInterface):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    def scrap(self, driver: typeWebDriver) -> Dict:

        self.logger.debug("Loading js script")

        # El bicho magico de la velocidad
        jScript = """const bfredmatches = Array.prototype.slice.call(document.getElementsByTagName("td"))
    return bfredmatches.map(function (match){
        return match.innerText
    })"""

        self.logger.debug("Script loaded. Executing...")

        betfredjsdata = driver.execute_script(jScript)

        self.logger.debug(f"Data found: {betfredjsdata}")
        self.logger.debug("Parsing data...")

        vs_pos = [idx for idx, elem in enumerate(betfredjsdata) if elem == '-']

        betfred_raw_names = [betfredjsdata[idx - 2] for idx in vs_pos]
        cuota_text_1 = [betfredjsdata[idx - 1] for idx in vs_pos]
        cuota_text_2 = [betfredjsdata[idx + 1] for idx in vs_pos]

        cuota_1 = list(pandas.to_numeric(cuota_text_1))
        cuota_2 = list(pandas.to_numeric(cuota_text_2))

        betfred_names = split_match_names(betfred_raw_names)

        betfred_dict = {name: cuotas for name, cuotas in
                        zip(betfred_names, map(list, zip(cuota_1, cuota_2)))}

        self.logger.debug(f"Parsed data: {betfred_dict}")

        return betfred_dict


def print_dict(dict_to_str):
    for key, val in dict_to_str.items():
        print(f'{key}: {val}')

def main():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter

    formatter = logging.Formatter('%(asctime)s %(filename)s - %(funcName)s [%(levelname)-s] - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    test_scraper = ModuleScraper(logger)

    driver = DriverManager(logger).create_driver("chrome")
    driver.get(url)
    input(f'{url = !s}')
    print_dict(test_scraper.scrap(driver))
    input('exit')
    driver.close()

if __name__ == '__main__':  # testea solo el scrapper de william
    main()

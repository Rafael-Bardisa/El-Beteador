from src.web_core.driver.driver_manager import DriverManager
from typing import Dict, Union

import logging

from selenium import webdriver

typeWebDriver = Union[webdriver.Firefox,
                      webdriver.Chrome,
                      webdriver.Edge,
                      webdriver.Safari
                      ]

from src.core.interfaces.scraper import IScraper
import pandas

url = "https://sports.williamhill.es/betting/es-es/tenis/partidos/competici%C3%B3n/hoy"

hydrater_source = "./javascript_hydraters/william_hydrater.js"

# driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
# bet365tenis = "https://www.bet365.es/#/AC/B13/C1/D50/E2/F163/"
# codere = "https://www.codere.es/"


def process_names(names):
    # quita el texto garbage y deja los nombres de los broskis del tenis
    true_names = []
    for elem in names:
        if ('Ganador' not in elem) and ('apuestas' not in elem) and (elem != ''):
            true_names.append(elem)
    return true_names


def format_names(split_names):
    # reformatea los nombres como apellido, inicial del nombre
    true_names = []
    drop_idx = []
    for idx, splitname in enumerate(split_names):
        if splitname[0].isnumeric():  # ignora la fecha si existe (dd mmm)
            splitname = splitname.split('\n')[1]
        data = splitname.split(" ")
        if len(data) == 1:  # si es doble, skippea
            drop_idx.append(idx)
        else:
            name = data[0][0]
            surname = apellido(data[1])
            # nombre = str(surname) + " " + str(name)
            nombre = f'{surname} {name}'
            true_names.append(nombre)
    return drop_idx, true_names


# TODO arreglar los nombres para que salgan bien las colisiones
# TODO a veces salen cuotas nan y desaparejan las cuotas de los nombres, no se como se arregla pero bastante importante


def split_match_names(true_names):
    # divide el nombre de la match en los dos jugadores
    split_names = []
    for elem in true_names:
        names = elem.split(' v ')
        split_names.append(names[0])
        split_names.append(names[1])
    return split_names


def apellido(surnamedata: str) -> str:  # corta str en el primer caracter no alfanumerico que encuentre
    surname = surnamedata.split('\n')
    return surname[0]

class ModuleScraper(IScraper):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def scrap(self, driver: typeWebDriver) -> Dict:
        """
        Scrapea la pagina william y recoge las cuotas de los partidos de tenis
        :param driver: referencia a un driver de selenium
        :return william_dict: diccionario estilo {match: [cuota 1, cuota 2]}
        """
        self.logger.debug(f"Loading scraper scripts")

        jScript_cuotas = """const willmatches = Array.prototype.slice.call(document.getElementsByClassName("betbutton__odds"))
        return willmatches.map(function (match){return match.innerText})"""

        jScript_names = """const willmatches = Array.prototype.slice.call(document.getElementsByClassName("btmarket__content"))
        return willmatches.map(function (match){return match.innerText})"""

        self.logger.debug("Scripts loaded. executing...")

        william_cuotas = driver.execute_script(jScript_cuotas)
        william_names = driver.execute_script(jScript_names)

        self.logger.debug(f"odds scraped: {william_cuotas}")
        self.logger.debug(f"names scraped: {william_names}")

        self.logger.debug("parsing data...")

        # convierte los elementos de las cuotas a numeros
        william_cuotas[:] = [pandas.to_numeric(cuota) for cuota in william_cuotas]

        # procesa y divide los nombres
        true_william_names = process_names(william_names)
        split_names = split_match_names(true_william_names)

        # formatea los nombres y tambien devuelve la lista de cuotas a borrar
        drop_idx, true_names = format_names(split_names)
        william_cuotas[:] = [cuota for idx, cuota in enumerate(william_cuotas) if idx not in drop_idx]

        # une los nombres para identificar el partido
        truer_william_names = [f'{local} {visitor}' for local, visitor in zip(true_names[::2], true_names[1::2])]

        # crea el diccionario magico que usa el main para crear la dataframe final
        william_dict = {name: cuotas for name, cuotas in
                        zip(truer_william_names, map(list, zip(william_cuotas[::2], william_cuotas[1::2])))}

        self.logger.debug(f"parsed data: {william_dict}")

        return william_dict

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

    driver = DriverManager(logger).create_driver("chrome")
    driver.get(url)
    william_scraper = ModuleScraper(logger)

    input(f'{url = !s}')
    print_dict(william_scraper.scrap(driver))
    input('exit')
    driver.close()


if __name__ == '__main__':  # testea solo el scrapper de william
    main()

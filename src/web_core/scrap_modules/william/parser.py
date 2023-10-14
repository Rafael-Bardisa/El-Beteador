import logging
from typing import Dict

import pandas

from src.web_core.scraper.interfaces.inner.parser import ParserInterface


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

class ModuleParser(ParserInterface):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def parse(self, data: Dict) -> Dict:
        """
        Parses data from william webpage and returns dict of found matches
        :param data: whatever result from extracter, to be fully treated in this function
        :return template_dict: a dictionary like {match: [odd 1, odd 2]}
        """
        self.logger.debug(f"Parser received data: {data}")

        # diccionario a llenar con las datas scrapeadas
        william_cuotas = data["odds"]
        william_names = data["names"]

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

        self.logger.debug(f"Parsed data: {william_dict}")

        return william_dict

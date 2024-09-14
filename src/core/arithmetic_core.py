from typing import Dict, List
import logging

import pandas as pd

from src.core.interfaces.arithmetic_core import IArithmeticCore


def build_odds_dataframe(odds_by_house: Dict[str, Dict[str, List]]) -> pd.DataFrame:
    odds_frame = pd.DataFrame()
    for idx, (name, odds) in enumerate(odds_by_house.items()):  # por cada data de cada casa
        series = pd.Series(odds)  # convierte la data a series

        # añade al dataframe, hay que hacer reassign because pandas
        odds_frame = odds_frame.merge(series.rename(name), left_index=True, right_index=True, how='outer')

    return odds_frame


# une los maximos e indices en un dataframe para tener la info ordenada
def big_merge(odd_1: pd.Series, odd_2: pd.Series, house_1: pd.Series, house_2: pd.Series) -> pd.DataFrame:
    odd_summary = pd.concat([odd_1, odd_2], axis=1)
    house_summary = pd.concat([house_1, house_2], axis=1)
    data_summary = odd_summary.merge(house_summary, left_index=True, right_index=True, how='outer')
    data_summary.columns = ['cuota 1', 'cuota 2', 'mejor casa 1', 'mejor casa 2']
    return data_summary


# comprueba si vale la pena apostar si hay cuotas a, b
def z(a, b) -> float:
    """
    Métrica que valora el retorno de una apuesta con cuotas a, b utilizando la apuesta de varianza 0
    :param a: el retorno por euro apostado si gana el jugador 1
    :param b: el retorno por euro apostado si gana el jugador 2

    :returns: el dinero que se gana al apostar a+b en total
    """
    return a * b - (a + b)


# {partido: [cuota1, cuota2]} -> {partido: cuota1}, {partido: cuota2}. dict_cuotas == cuotas de *una* casa
def split_odds(dict_odds):
    keys = [key for key in dict_odds.keys()]
    values_1 = [odds[0] for odds in dict_odds.values()]
    values_2 = [odds[1] for odds in dict_odds.values()]

    odds_1 = dict(zip(keys, values_1))  # {partido: cuota1}
    odds_2 = dict(zip(keys, values_2))  # {partido: cuota2}

    return odds_1, odds_2


class ArithmeticCore(IArithmeticCore):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.debug(f"Arithmetic Core initialized")

    def find_arbitrage(self, house_odds: Dict[str, Dict[str, List]]) -> pd.DataFrame:
        odd_1_by_house = {}
        odd_2_by_house = {}

        for house_name, house in house_odds.items():
            odd_1, odd_2 = split_odds(house)
            odd_1_by_house[house_name] = odd_1
            odd_2_by_house[house_name] = odd_2

        data_odd_1 = build_odds_dataframe(odd_1_by_house)
        data_odd_2 = build_odds_dataframe(odd_2_by_house)

        # columnas para saber si hay arbitraje
        best_odd_1 = data_odd_1.max(axis=1, skipna=True)  # mejor cuota 1 para cada partido
        best_house_1 = data_odd_1.idxmax(axis=1, skipna=True)  # que house ofrece la mejor cuota

        best_odd_2 = data_odd_2.max(axis=1, skipna=True)  # mejor cuota 2 para cada partido
        best_house_2 = data_odd_2.idxmax(axis=1, skipna=True)  # que house ofrece la mejor cuota

        final_data = big_merge(best_odd_1, best_odd_2, best_house_1, best_house_2)
        final_data['z'] = z(final_data['cuota 1'], final_data['cuota 2'])
        # printear oportunidades
        self.logger.debug(final_data.sort_values(by='z', ascending=False).head(10))
        return final_data


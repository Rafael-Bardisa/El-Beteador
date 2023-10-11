from driver_manager.chromedriver import chrome
from typing import Dict, Union

from driver_manager.driver_manager import DriverManager

from selenium import webdriver

typeWebDriver = Union[webdriver.Firefox,
                      webdriver.Chrome,
                      webdriver.Edge,
                      webdriver.Safari
                      ]

import logging

from core.interfaces.inner.scraper import ScraperInterface
import pandas

# url de la pagina:
url = "https://www.bet365.es/#/AC/B13/C1/D50/E2/F163/"


def is_tennis_player(string: str) -> bool:
	bad_chars = '0123456789:.'
	# no hay ninguno de los bad chars en string y no es LIVE -> es el nombre de un tenista
	return not (any(char in string for char in bad_chars) or string == 'LIVE')


def format_name(name: str) -> str:
	name_elems = name.split()
	return f'{name_elems[1]} {name_elems[0][0]}'  # apellido, inicial


# nombre torneo\n fecha\n hora\n ??
def format_names(market_group: str):  # coge los nombres de los tenistas y cuantas matches hay
	market_data = market_group.split('\n')
	actual_names = []
	# coje los nombres antes para saber cuanto saltar con las cuotas
	tennis_names = [name for name in market_data[1:] if is_tennis_player(name)]  # solo nombres de tenistas
	n_matches = len(tennis_names)//2  # numero de partidos (cuanto hay que saltar en las cuotas)
	if "Dobles" not in market_data[0]:  # elimina los dobles
		names_list = list(map(format_name, tennis_names))
		actual_names = [f'{local} {visitor}' for local, visitor in zip(names_list[::2], names_list[1::2])]  # los
	# junta segun partido
	return actual_names, n_matches


def dict_builder(strings, cuotas) -> dict:  # construye el diccionario poco a poco con los datos cogidos por jScript
	cuota_idx = 0
	bet365_dict = {}
	for market_group in strings:
		bet365_names, scope = format_names(market_group)  # partidos y cuantos hay
		if bet365_names:  # si la lista de nombres no esta vacia
			cuotas_grupo = list(
				map(list, zip(cuotas[cuota_idx:cuota_idx + scope], cuotas[cuota_idx + scope:cuota_idx + 2 * scope])))
			grupo_dict = {name: cuota for name, cuota in zip(bet365_names, cuotas_grupo)}
			bet365_dict.update(grupo_dict)
		cuota_idx += 2 * scope
	return bet365_dict

class ModuleScraper(ScraperInterface):
	def __init__(self, logger: logging.Logger):
		self.logger = logger

	def scrap(self, driver: typeWebDriver) -> Dict:
		"""
		Scrapea la pagina bet365 y recoge las cuotas de los partidos de tenis
		:param driver: referencia a un driver de selenium
		:return bet365_dict: diccionario estilo {match: [cuota 1, cuota 2]}
		"""
		self.logger.debug("loading scripts")
		# replacea los ######## por lo que usarias con el driver find elements
		jScript_cuotas = """const bet365matches = Array.prototype.slice.call(document.getElementsByClassName("sgl-ParticipantOddsOnly80"))
		return bet365matches.map(function (match){return match.innerText})"""

		jScript_names = """const bet365matches = Array.prototype.slice.call(document.getElementsByClassName("src-CompetitionMarketGroup"))
		return bet365matches.map(function (match){return match.innerText})"""

		self.logger.debug("scripts loaded. executing...")

		bet365_cuotas_web = driver.execute_script(jScript_cuotas)
		bet365_names = driver.execute_script(jScript_names)
		bet365_cuotas = list(pandas.to_numeric(bet365_cuotas_web))

		self.logger.debug(f"Odds found: {bet365_cuotas}")
		self.logger.debug(f"Names found: {bet365_names}")
		# es mucho mas chungo en bet 365
		self.logger.debug("parsing data...")
		result = dict_builder(bet365_names, bet365_cuotas)

		self.logger.debug(f"Parsed data: {result}")
		return result


def print_dict(dict_to_str):
	for key, val in dict_to_str.items():
		print(f'{key}: {val}')


def main():  # de testeo para comprobar que la funcion va bien

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


if __name__ == '__main__':  # testea solo el scrapper de bet365
	main()

from typing import Dict

from src.web_core.scraper.interfaces.parser import IParser

import logging

# webpage url:
url = ''

class ModuleParser(IParser):
	def __init__(self, logger: logging.Logger):
		self.logger = logger

	def parse(self, data: Dict) -> Dict:
		"""
		Parses data from bet365 webpage and returns dict of found matches
		:param data: whatever result from extracter, to be fully treated in this function
		:return template_dict: a dictionary like {match: [odd 1, odd 2]}
		"""
		self.logger.debug(f"Parser received data: {data}")

		# diccionario a llenar con las datas scrapeadas
		bet365_dict = {}

		self.logger.debug(f"Parsed data: {bet365_dict}")

		return bet365_dict

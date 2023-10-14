import logging
import pathlib
import yaml
import json
from typing import Dict

from src.web_core.importer.interfaces.inner.config_manager import ConfigManagerInterface


def _load_yaml_config(yaml_path: pathlib.Path) -> Dict:
    config = yaml.safe_load(yaml_path.read_text())
    return config


def _load_json_config(json_path: pathlib.Path) -> Dict:
    with open(json_path, "rb") as file:
        config = json.load(file)
    return config


class ConfigManager(ConfigManagerInterface):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def load_config(self, config_file_path: pathlib.Path) -> Dict:
        self.logger.debug(f"parsing config file: {config_file_path.name}")
        config_file_extension = config_file_path.name.split(".")[-1]

        if config_file_extension == "yml" or config_file_extension == "yaml":
            return _load_yaml_config(config_file_path)
        elif config_file_extension == "json":
            return _load_json_config(config_file_path)
        elif config_file_extension == "txt":
            pass
        else:
            raise ValueError(f"{config_file_path} is not a valid configuration file")

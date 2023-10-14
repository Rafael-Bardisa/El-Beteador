# main program loop, is given list of modules to use
import logging

from src.core.interfaces.inner.module_importer import ModuleImporterInterface


class BeteadorCore:
    def __init__(self, logger: logging.Logger, module_loader: ModuleImporterInterface, arithmetic_core):
        self.logger = logger
        self.module_loader = module_loader
        self.arithmetic_core = arithmetic_core

from typing import Union

from selenium import webdriver

TypeWebDriver = Union[webdriver.Firefox,
                      webdriver.Chrome,
                      webdriver.Edge,
                      webdriver.Safari
                      ]

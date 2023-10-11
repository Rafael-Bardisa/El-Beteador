from selenium import webdriver
from driver_manager import chromedriver
from core.interfaces.inner.scraper import ScraperInterface

try:
    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
except Exception:
    print('\33[91mWebdriver path incorrect!\33[0m')
a = '09090'
print(a)

class Test(ScraperInterface):
    def __init__(self):
        self.scrap = lambda _, x: x

test = Test()
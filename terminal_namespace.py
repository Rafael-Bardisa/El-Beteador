from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver
import pandas as pd

try:
    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
except Exception:
    print('\33[91mWebdriver path incorrect!\33[0m')
a = '09090'
print(a)
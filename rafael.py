from selenium import webdriver
import chromedriver
import atexit
import sys


def test2():
    print('exit')


driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver")
chromedriver.placeholder(driver)

# test()
atexit.register(test2)
sys.exit()

from selenium import webdriver
import chromedriver

if __name__ == '__main__':
    driver_1 = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver")
    driver_2 = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver")
    chromedriver.BETEADOR(driver_1, driver_2)

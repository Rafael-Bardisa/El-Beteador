from selenium import webdriver
import pandas
import time

driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver")
bet365 = "https://www.bet365.es/#/OF/"
codere = "https://www.codere.es/"

#Entra en Bet365
driver.get(bet365)

#Espera y entra en tenis
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div[29]").click()

#Espera y entra en la lista de partidos
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/span").click()


databet365 = pandas.DataFrame()


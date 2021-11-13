from selenium import webdriver
import pandas
import time

driver = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver")
bet365 = "https://www.bet365.es/#/OF/"
codere = "https://www.codere.es/"


driver.get(bet365)

time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div[29]").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/span").click()

prueba = driver.find_elements_by_class_name("sgl-ParticipantOddsOnly80_Odds")

for i in range(len(prueba)):
    prueba[i] = pandas.to_numeric(prueba[i].get_attribute("innerText"))



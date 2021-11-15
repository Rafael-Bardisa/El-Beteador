from selenium import webdriver
import pandas
import time

driver = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver")
bet365 = "https://www.bet365.es/#/OF/"
codere = "https://www.codere.es/"

def go(driver):
    driver.get(bet365)

    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div[29]").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/span").click()
    time.sleep(1)


def scrap(driver):
    cuotas = driver.find_elements_by_class_name("sgl-ParticipantOddsOnly80_Odds")

    for i in range(len(cuotas)):
        cuotas[i] = pandas.to_numeric(cuotas[i].get_attribute("innerText"))
    
    Datos = pandas.DataFrame()    

    Datos["Cuota1"] = cuotas[1:52]

    cuotas[102]
    
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]").get_attribute("innerText")
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div[4]").get_attribute("innerText")
    
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]").get_attribute("innerText")
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div[8]").get_attribute("innerText")

    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]").get_attribute("innerText")


    #pillar cuotas y 1 y 2. Despues, para distinguir los 1 de los 2, recordar la posicion en la que estan los 1 en el loop; los 2 con la misma posicion son falsos.
    
    

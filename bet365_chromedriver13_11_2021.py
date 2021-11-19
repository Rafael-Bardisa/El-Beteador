from selenium import webdriver
import pandas
import time

driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
bet365tenis = "https://www.bet365.es/#/AC/B13/C1/D50/E2/F163/"
codere = "https://www.codere.es/"

#rip path ("/html/body/div[1]/div/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div[29]")

def go(driver):
    driver.get(bet365tenis)



def scrap(driver):
    cuotas = driver.find_elements_by_class_name("sgl-ParticipantOddsOnly80_Odds")

    for i in range(len(cuotas)):
        cuotas[i] = pandas.to_numeric(cuotas[i].get_attribute("innerText"))
    
    Datos = pandas.DataFrame()    

    Datos["Cuota1"] = cuotas[1:52]

    cuotas[102]
    
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]").get_attribute("innerText")

    #pillar cuotas y 1 y 2. Despues, para distinguir los 1 de los 2, recordar la posicion en la que estan los 1 en el loop; los 2 con la misma posicion son falsos.
    
    


go(driver=driv)


#de aqui sacas cuotas
clase1 = driv.find_elements_by_class_name("gl-MarketGroupContainer ")

clase1[0].get_attribute("innerText")
clase1[1].get_attribute("innerText")

#de aqui sacas jugadores
clase2 = driv.find_elements_by_class_name("rcl-ParticipantFixtureDetails_TeamAndScoresContainer")
clase2[0].get_attribute("innerText")
clase2[1].get_attribute("innerText")


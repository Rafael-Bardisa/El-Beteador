from selenium import webdriver
import pandas
import time

driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
bet365tenis = "https://www.bet365.es/#/AC/B13/C1/D50/E2/F163/"
codere = "https://www.codere.es/"
william = "https://sports.williamhill.es/betting/es-es/en-directo/tenis"



def scrap(driver):
    cuotas = driver.find_elements_by_class_name("sgl-ParticipantOddsOnly80_Odds")

    for i in range(len(cuotas)):
        cuotas[i] = pandas.to_numeric(cuotas[i].get_attribute("innerText"))
    
    Datos = pandas.DataFrame()    

    Datos["Cuota1"] = cuotas[1:52]

    cuotas[102]
    
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]").get_attribute("innerText")

    #pillar cuotas y 1 y 2. Despues, para distinguir los 1 de los 2, recordar la posicion en la que estan los 1 en el loop; los 2 con la misma posicion son falsos.
    

driv.get("https://sports.williamhill.es/betting/es-es/en-directo/tenis")

williamcuotas = driv.find_elements_by_class_name("betbutton__odds")
williamcuotas[0].text
williamnames  = driv.find_elements_by_class_name("btmarket__content")
williamnames[0].text

datos_william = pandas.DataFrame()


for i in range(len(williamcuotas)):
        williamcuotas[i] = pandas.to_numeric(williamcuotas[i].text)



for i in range(len(williamcuotas)):
    if i % 2 == 0:
        datos_william[(i//2),datos_william.iloc(1)] = williamcuotas[i]
        
    else:
        datos_william[(i//2)-1,datos_william.iloc(2)] = williamcuotas[i]
        


        

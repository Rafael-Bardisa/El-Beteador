from selenium import webdriver
import pandas
import time

# driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
bet365tenis = "https://www.bet365.es/#/AC/B13/C1/D50/E2/F163/"
codere = "https://www.codere.es/"
william = "https://sports.williamhill.es/betting/es-es/en-directo/tenis"

def apellido(str):  # corta str en el primer caracter no alfanumerico que encuentre
    for i in range(len(str)):
        if not (str[i].isalnum()):
            return str[0:i-1]
    return str

def scrap(driver):
    # pillar cuotas y 1 y 2. Despues, para distinguir los 1 de los 2, recordar la posicion en la que estan los 1 en el loop; los 2 con la misma posicion son falsos.
    
    # TODO esto en algun momento se va fuera pero de momento es conveniente
    driver.get("https://sports.williamhill.es/betting/es-es/en-directo/tenis")

    williamcuotas = driver.find_elements_by_class_name("betbutton__odds")
    williamnames = driver.find_elements_by_class_name("btmarket__content")

    # quita el texto garbage y deja los nombres de los broskis del tenis
    truewilliamnames = []
    for i in range(len(williamnames)):
        william = williamnames[i].text
        if ('Ganador' not in william) and (william != ''):
            truewilliamnames.append(william)

    # divide el nombre de la match en los dos jugadores
    splitnames = []
    for i in range(len(truewilliamnames)):
        names = truewilliamnames[i].split(' v ')
        splitnames.append(names[0])
        splitnames.append(names[1])

    # print(repr(splitnames[0]))

    # reformatea los nombres como apellido, inicial del nombre
    truenames = []
    for i in range(len(splitnames)):
        data = splitnames[i].split(" ")
        name = data[0][0]
        surname = apellido(data[1])
        nombre = surname + " " + name
        truenames.append(nombre)

    # une los nombres para identificar el partido
    for i in range(len(truenames)//2):
        truewilliamnames[i] = truenames[i*2] + " " + truenames[i*2 + 1]

    # convierte los elementos de las cuotas a numeros
    for i in range(len(williamcuotas)):
        williamcuotas[i] = pandas.to_numeric(williamcuotas[i].text)

    #print(repr(truewilliamnames[0]))
    #print(len(truewilliamnames))
    #print(splitnames)

    # crea el diccionario magico que usa el main para crear la dataframe final
    william_dict = {}
    for i in range(len(truewilliamnames)):
        william_dict[truewilliamnames[i]] = [williamcuotas[i*2], williamcuotas[(i*2) + 1]]
    return william_dict
        


        

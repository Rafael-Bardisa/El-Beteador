from selenium import webdriver
import pandas
import chromedriver
import time

# driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
#bet365tenis = "https://www.bet365.es/#/AC/B13/C1/D50/E2/F163/"
#codere = "https://www.codere.es/"
#william = "https://sports.williamhill.es/betting/es-es/tenis/partidos"

# TODO arreglar los nombres para que salgan bien las colisiones
def apellido(str):  # corta str en el primer caracter no alfanumerico que encuentre
    surname = str.split('\n')


    #for i in range(len(str)):
    #    if not (str[i].isalnum()):
    #        return str[0:i-1]
    return surname[0]

def scrap(driver):

    williamcuotas = driver.find_elements_by_class_name("betbutton__odds")
    williamnames = driver.find_elements_by_class_name("btmarket__content")

    # convierte los elementos de las cuotas a numeros
    for i in range(len(williamcuotas)):
        williamcuotas[i] = pandas.to_numeric(williamcuotas[i].text)

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

    # reformatea los nombres como apellido, inicial del nombre
    truenames = []
    drop_idx = []
    for i in range(len(splitnames)):
        if splitnames[i][0].isnumeric():#ignora la fecha si existe
            splitnames[i] = splitnames[i].split('\n')[1]
        data = splitnames[i].split(" ")
        if (len(data) == 1):
            #lmaol
            truenames.append(str(data))
        else:
            name = data[0][0]
            surname = apellido(data[1])
            nombre = surname + " " + name
            truenames.append(nombre)

    # une los nombres para identificar el parotid
    for i in range(len(truenames)//2):
        truewilliamnames[i] = truenames[i*2] + " " + truenames[i*2 + 1]



    #print(repr(truewilliamnames[0]))
    #print(len(truewilliamnames))
    #print(splitnames)

    # crea el diccionario magico que usa el main para crear la dataframe final
    william_dict = {}
    for i in range(len(truewilliamnames)):
        william_dict[truewilliamnames[i]] = [williamcuotas[i*2], williamcuotas[(i*2) + 1]]
    return william_dict
        
if __name__ == '__main__':
        driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
        a = input('wait')
        scrap(driver)

        

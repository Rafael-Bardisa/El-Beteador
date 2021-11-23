from selenium import webdriver
import pandas
import chromedriver

#driv = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
#betway = "https://betway.es/es/sports/sct/tennis/challenger"

def scrap(driver):

    betwaycuotas = driver.find_elements_by_class_name("oddsDisplay")
    betwaynames = driver.find_elements_by_class_name("scoreboardInfoNames")

    # quita el texto garbage y deja los nombres de los broskis del tenis
    truebetwaynames = []
    for i in range(len(betwaynames)):
        betway = betwaynames[i].text
        truebetwaynames.append(betway)

    # divide el nombre de la match en los dos jugadores
    splitnames = []
    for i in range(len(truebetwaynames)):
        names = truebetwaynames[i].split(' -')
        splitnames.append(names[0])
        splitnames.append(names[1])

    # print(repr(splitnames[0]))

    # reformatea los nombres como apellido, inicial del nombre
    truenames = []
    for i in range(len(splitnames)):
        data = splitnames[i].split(" ")
        if data[0][0] == '√':   #un clasico
            name = data[1][0]
            surname = data[2]
        else:
            name = data[0][0]
            surname = data[1]
        nombre = surname + " " + name
        truenames.append(nombre)

    # une los nombres para identificar el partido
    for i in range(len(truenames) // 2):
        truebetwaynames[i] = truenames[i * 2] + " " + truenames[i * 2 + 1]

    # convierte los elementos de las cuotas a numeros
    for i in range(len(betwaycuotas)):
        cuota = betwaycuotas[i].text.replace(',', '.')
        if cuota == '-':
            betwaycuotas[i] = 0.5
        else:
            betwaycuotas[i] = pandas.to_numeric(cuota)

    # print(repr(truewilliamnames[0]))
    # print(len(truewilliamnames))
    # print(splitnames)

    # crea el diccionario magico que usa el main para crear la dataframe final
    betway_dict = {}
    for i in range(len(truebetwaynames)):
        betway_dict[truebetwaynames[i]] = [betwaycuotas[i * 2], betwaycuotas[(i * 2) + 1]]
    return betway_dict


if __name__ == '__main__':
        driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
        a = input('wait')
        scrap(driver)
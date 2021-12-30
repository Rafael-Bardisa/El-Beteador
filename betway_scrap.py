from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas


# driv = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())

def test():
    url = "https://betway.es/es/sports/sct/tennis/challenger"
    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver",
                              chrome_options=chromedriver.camo())
    input(f'{url = !s}')
    print(scrap(driver))

# TODO cuando hay destacados coge containers que no son de partidos. Se arregla eligiendo un unico torneo pero eso reduce mucho lo que cogemos
def scrap(driver):
    betway_cuotas = driver.find_elements(By.CLASS_NAME, "oddsDisplay")
    betway_names = driver.find_elements(By.CLASS_NAME, "scoreboardInfoNames")

    # quita el texto garbage y deja los nombres de los broskis del tenis
    string_betway_names = [name.text for name in betway_names]
    # for i in range(len(betwaynames)):
    #    betway = betwaynames[i].text
    #    truebetwaynames.append(betway)

    # convierte los elementos de las cuotas a numeros
    # for i in range(len(betway_cuotas)):
    #    cuota = betway_cuotas[i].text.replace(',', '.')
    #    if cuota == '-':
    #        betway_cuotas[i] = 0.5
    #    else:
    #        betway_cuotas[i] = pandas.to_numeric(cuota)

    betway_cuotas[:] = [pandas.to_numeric(cuota.text.replace(',','.')) if cuota != '-' else 0.5 for cuota in betway_cuotas]

    # divide el nombre de la match en los dos jugadores
    split_names = []
    for bet_name in string_betway_names:
        names = bet_name.split(' -')
        split_names.append(names[0])
        split_names.append(names[1])

    # print(repr(splitnames[0]))

    # reformatea los nombres como apellido, inicial del nombre
    true_names = []
    for split_name in split_names:
        data = split_name.split(" ")
        if data[0][0] == '√':  # un clasico
            name = data[1][0]
            surname = data[2]
        else:
            name = data[0][0]
            surname = data[1]
        nombre = f'{surname} {name}'
        true_names.append(nombre)

    # une los nombres para identificar el partido
    true_betway_names = []
    for local, visitor in zip(true_names[::2], true_names[1::2]):
        true_betway_names.append(f'{local} {visitor}')

    # print(repr(truewilliamnames[0]))
    # print(len(truewilliamnames))
    # print(splitnames)

    # crea el diccionario magico que usa el main para crear la dataframe final
    betway_dict = {}
    # for i in range(len(string_betway_names)):
    #    betway_dict[string_betway_names[i]] = [betway_cuotas[i * 2], betway_cuotas[(i * 2) + 1]]

    for name, cuotas in zip(true_betway_names, map(list, zip(betway_cuotas[::2], betway_cuotas[1::2]))):
        betway_dict[name] = cuotas

    return betway_dict


if __name__ == '__main__':  # testea solo el scrapper de betway
    import chromedriver

    test()
    input('exit')

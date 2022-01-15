from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas

url = "https://sports.williamhill.es/betting/es-es/tenis/partidos"


# driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
# bet365tenis = "https://www.bet365.es/#/AC/B13/C1/D50/E2/F163/"
# codere = "https://www.codere.es/"


# TODO arreglar los nombres para que salgan bien las colisiones
def apellido(surnamedata):  # corta str en el primer caracter no alfanumerico que encuentre
    surname = surnamedata.split('\n')
    return surname[0]


# TODO a veces salen cuotas nan y desaparejan las cuotas de los nombres, no se como se arregla pero bastante importante
def scrap(driver) -> dict:
    """
    Scrapea la pagina william y recoge las cuotas de los partidos de tenis
    :param driver: referencia a un driver de selenium
    :return william_dict: diccionario estilo {match: [cuota 1, cuota 2]
    """
    william_cuotas = driver.find_elements(By.CLASS_NAME, "betbutton__odds")
    william_names = driver.find_elements(By.CLASS_NAME, "btmarket__content")

    # convierte los elementos de las cuotas a numeros
    william_cuotas[:] = [pandas.to_numeric(cuota.text) for cuota in william_cuotas]

    # quita el texto garbage y deja los nombres de los broskis del tenis
    true_william_names = []
    for elem in william_names:
        william = elem.text
        if ('Ganador' not in william) and (william != ''):
            true_william_names.append(william)

    # divide el nombre de la match en los dos jugadores
    split_names = []
    for elem in true_william_names:
        names = elem.split(' v ')
        split_names.append(names[0])
        split_names.append(names[1])
    # reformatea los nombres como apellido, inicial del nombre
    true_names = []
    drop_idx = []

    for idx, splitname in enumerate(split_names):
        if splitname[0].isnumeric():  # ignora la fecha si existe (dd mmm)
            splitname = splitname.split('\n')[1]
        data = splitname.split(" ")
        if len(data) == 1:  # si es doble, skippea
            drop_idx.append(idx)
        else:
            name = data[0][0]
            surname = apellido(data[1])
            # nombre = str(surname) + " " + str(name)
            nombre = f'{surname} {name}'
            true_names.append(nombre)

    # elimina las cuotas de los dobles
    for idx, idx_to_drop in enumerate(drop_idx):
        william_cuotas.pop(idx_to_drop - idx)

    # une los nombres para identificar el partido
    truer_william_names = []
    # for i in range(len(true_names) // 2):
    #    truer_william_names.append(f'{true_names[i * 2]} {true_names[i * 2 + 1]}')

    for local, visitor in zip(true_names[::2], true_names[1::2]):
        truer_william_names.append(f'{local} {visitor}')
    # print(len(truer_williamnames))
    # print(len(williamcuotas))
    # crea el diccionario magico que usa el main para crear la dataframe final
    william_dict = {}
    # for i in range(len(truer_william_names)):
    #    william_dict[truer_william_names[i]] = [william_cuotas[i * 2], william_cuotas[(i * 2) + 1]]

    for name, cuotas in zip(truer_william_names, map(list, zip(william_cuotas[::2], william_cuotas[1::2]))):
        william_dict[name] = cuotas

    return william_dict


def main():
    import chromedriver

    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver",
                                chrome_options=chromedriver.camo())
    input(f'{url = !s}')
    print(scrap(driver))
    input('exit')


if __name__ == '__main__':  # testea solo el scrapper de william
    main()

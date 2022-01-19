from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas

url = "https://betway.es/es/sports/sct/tennis/challenger"


# driv = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())


def format_name(split_name):
    data = split_name.split(" ")
    if data[0][0] == '√':  # un clasico, filtra algunas matches invalidas
        name = data[1][0]
        surname = data[2]
    else:
        name = data[0][0]
        surname = data[1]
    return f'{surname} {name}'


def split_betway_names(betway_names):
    # divide el nombre de la match en los dos jugadores
    split_names = []
    bet_name: str
    for bet_name in betway_names:
        if bet_name.startswith(' '):
            bet_name = bet_name[1:]
        names = bet_name.split(' -')
        split_names.append(names[0])
        split_names.append(names[1])
    return split_names


# TODO cuando hay destacados coge containers que no son de partidos. Se arregla eligiendo un unico torneo pero eso
#  reduce mucho lo que cogemos
def scrap(driver) -> dict:
    """
    Scrapea la pagina betway y recoge las cuotas de los partidos de tenis
    :param driver: referencia a un driver de selenium
    :return william_dict: diccionario estilo {match: [cuota 1, cuota 2]
    """

    jScript_cuotas = """const willmatches = Array.prototype.slice.call(document.getElementsByClassName("oddsDisplay"))
    return willmatches.map(function (match){return match.innerText})"""

    jScript_names = """const willmatches = Array.prototype.slice.call(document.getElementsByClassName("scoreboardInfoNames"))
    return willmatches.map(function (match){return match.innerText})"""

    betway_cuotas = driver.execute_script(jScript_cuotas)
    betway_names = driver.execute_script(jScript_names)

    betway_cuotas[:] = [pandas.to_numeric(cuota.replace(',', '.')) if cuota != '-' else 0.5 for cuota in
                        betway_cuotas]

    split_names = split_betway_names(betway_names)
    # reformatea los nombres como apellido, inicial del nombre
    true_names = [format_name(split_name) for split_name in split_names]

    # une los nombres para identificar el partido
    true_betway_names = [f'{local} {visitor}' for local, visitor in zip(true_names[::2], true_names[1::2])]

    # crea el diccionario magico que usa el main para crear la dataframe final
    betway_dict = {name: cuotas for name, cuotas in
                   zip(true_betway_names, map(list, zip(betway_cuotas[::2], betway_cuotas[1::2])))}

    return betway_dict


def print_dict(dict):
    for key, val in dict.items():
        print(f'{key}: {val}')

def main():
    import chromedriver

    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver",
                              chrome_options=chromedriver.camo())
    input(f'{url = !s}')
    print_dict(scrap(driver))
    input('exit')
    driver.close()

if __name__ == '__main__':  # testea solo el scrapper de betway
    main()

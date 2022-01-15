from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas

url = "https://sports.bwin.es/es/sports/tenis-5/apuestas"


# driv = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())


def extract_matches(bwin_matches):
    # Extrae cuotas y nombres
    bwin_cuotas = []
    bwin_names = []
    for bwin_match in bwin_matches:
        match = bwin_match.text.split('\n')
        if '/' not in match[0]:
            bwin_cuotas.append(match[(len(match) - 2)])
            bwin_cuotas.append(match[(len(match) - 1)])
            bwin_names.append(match[0])
            bwin_names.append(match[1])
    return bwin_cuotas, bwin_names


def format_name(elem):
    """
    devuelve el nombre de un tenista en formato "apellido inicial"
    tambien quita los tags de los paises
    :param elem: nombre del tenista
    :return: f'{surname}, {name[0]}
    """
    fullname = elem.split()
    name_size = len(fullname)
    name = fullname[0][0]
    if name_size == 2:
        surname = fullname[1][0:-3]
    else:
        surname = fullname[1]
    return f'{surname} {name}'


# TODO mas tests para asegurarse de que es robusto
def scrap(driver) -> dict:
    """
    Scrapea la pagina bwin y recoge las cuotas de los partidos de tenis
    :param driver: referencia a un driver de selenium
    :return william_dict: diccionario estilo {match: [cuota 1, cuota 2]
    """
    bwin_matches = driver.find_elements(By.CLASS_NAME, "grid-event-wrapper")

    # extrae la info de las matches
    bwin_cuotas, bwin_names = extract_matches(bwin_matches)

    bwin_cuotas[:] = [pandas.to_numeric(cuota) for cuota in bwin_cuotas]
    # formatea los nombres correctamente
    true_bwin_names = [format_name(elem) for elem in bwin_names]
    # empareja los rivales
    truer_bwin_names = [f'{local} {visitor}' for local, visitor in zip(true_bwin_names[::2], true_bwin_names[1::2])]

    # crea el diccionario magico que usa el main para crear la dataframe final
    bwin_dict = {name: cuotas for name, cuotas in
                 zip(truer_bwin_names, map(list, zip(bwin_cuotas[::2], bwin_cuotas[1::2])))}

    return bwin_dict


def main():
    import chromedriver

    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver",
                              chrome_options=chromedriver.camo())
    input(f'{url = !s}')
    print(scrap(driver))
    input('exit')


if __name__ == '__main__':  # testea solo el scrapper de bwin
    main()

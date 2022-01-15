from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas

url = "https://sports.bwin.es/es/sports/tenis-5/apuestas"


# driv = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())


# TODO mas tests para asegurarse de que es robusto
def scrap(driver) -> dict:
    """
    Scrapea la pagina bwin y recoge las cuotas de los partidos de tenis
    :param driver: referencia a un driver de selenium
    :return william_dict: diccionario estilo {match: [cuota 1, cuota 2]
    """
    bwin_matches = driver.find_elements(By.CLASS_NAME, "grid-event-wrapper")
    # bwinmatch[0].text

    # Extrae cuotas y nombres
    bwin_cuotas = []
    bwin_names = []
    for i in range(len(bwin_matches) * 2):
        match = bwin_matches[i // 2].text.split('\n')
        if '/' not in match[0]:
            if i % 2 == 0:
                bwin_cuotas.append(match[(len(match) - 2)])
                bwin_names.append(match[0])
            else:
                bwin_cuotas.append(match[(len(match) - 1)])
                bwin_names.append(match[1])

    for bwin_match in bwin_matches:
        match = bwin_match.text.split('\n')
        if '/' not in match[0]:
            bwin_cuotas.append(match[(len(match) - 2)])
            bwin_cuotas.append(match[(len(match) - 1)])
            bwin_names.append(match[0])
            bwin_names.append(match[1])

    # for i in range(len(bwin_cuotas)):
    #    convierte los elementos de las cuotas a numeros
    #    bwin_cuotas[i] = pandas.to_numeric(bwin_cuotas[i])

    bwin_cuotas[:] = [pandas.to_numeric(cuota) for cuota in bwin_cuotas]

    # print(bwincuotas)
    # print(bwinnames)
    # print(len(bwincuotas))
    true_bwin_names = []
    for elem in bwin_names:
        fullname = elem.split()
        name_size = len(fullname)

        name = fullname[0][0]
        if name_size == 2:
            surname = fullname[1][0:-3]
        else:
            surname = fullname[1]
        true_bwin_names.append(f'{surname} {name}')

    truer_bwin_names = []
    for local, visitor in zip(true_bwin_names[::2], true_bwin_names[1::2]):
        truer_bwin_names.append(f'{local} {visitor}')

    # print(truerbwinnames)
    # print(len(truerbwinnames))
    # crea el diccionario magico que usa el main para crear la dataframe final
    bwin_dict = {}
    # for i in range(len(truer_bwin_names)):
    #    bwin_dict[truer_bwin_names[i]] = [bwin_cuotas[i * 2], bwin_cuotas[(i * 2) + 1]]

    for name, cuotas in zip(truer_bwin_names, map(list, zip(bwin_cuotas[::2], bwin_cuotas[1::2]))):
        bwin_dict[name] = cuotas
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

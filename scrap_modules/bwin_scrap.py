from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas
import benchmarking

url = "https://sports.bwin.es/es/sports/tenis-5/apuestas"




# 'Pavel KotovRUS
# Denis IstominUZB
# Comienza en 56 min
# 1.25  <- cuota 1
# 3.60  <- cuota 2
# Set 1
# 1.33
# Set 1
# 3.00'

# 'Jazmin OrtenziARG
# Emily Matias Da Silva ChangBRA
# EN VIVO
# 1er set
# 40
# 30
# P
# 2
# 0
# J
# 0
# 0
# Sets
# Apostar ahora'    <- aqui iria cuota 1 y debajo cuota 2

# TODO desapareja mal las matches por algun motivo
# @benchmarking.benchmark
def extract_matches(bwin_matches):
    # Extrae cuotas y nombres
    bwin_cuotas = []
    bwin_names = []
    for bwin_match in bwin_matches:
        match = bwin_match.split('\n')
        if '/' not in match[0]:  # elimina los dobles
            handle_bwin_match(bwin_cuotas, bwin_names, match)

    return bwin_cuotas, bwin_names

# TODO desapareja mal las matches por algun motivo
def handle_bwin_match(bwin_cuotas, bwin_names, match):
    cond = map(lambda x: '.' in x, match[-2:])  # mira si los dos elementos del final tienen un punto
    if all(cond):
        cuotas = pandas.to_numeric(match[-2:])
        bwin_cuotas.extend(list(cuotas))
        bwin_names.extend(match[0:2])

        # print(f'error at {match[0]}')

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
    :return betway_dict: diccionario estilo {match: [cuota 1, cuota 2]
    """
    # El bicho magico de la velocidad
    jScript = """const bwinmatches = Array.prototype.slice.call(document.getElementsByClassName("grid-event-wrapper"))
return bwinmatches.map(function (match){
    return match.innerText
})"""
    # bwin_matches = driver.find_elements(By.CLASS_NAME, "grid-event-wrapper")
    bwin_matches = driver.execute_script(jScript)
    # extrae la info de las matches
    bwin_cuotas, bwin_names = extract_matches(bwin_matches)

    # bwin_cuotas[:] = [pandas.to_numeric(cuota) for cuota in bwin_cuotas]
    # formatea los nombres correctamente
    true_bwin_names = [format_name(elem) for elem in bwin_names]
    # empareja los rivales
    truer_bwin_names = [f'{local} {visitor}' for local, visitor in zip(true_bwin_names[::2], true_bwin_names[1::2])]

    # crea el diccionario magico que usa el main para crear la dataframe final
    bwin_dict = {name: cuotas for name, cuotas in
                 zip(truer_bwin_names, map(list, zip(bwin_cuotas[::2], bwin_cuotas[1::2])))}
    return bwin_dict


def print_dict(dict_to_str):
    for key, val in dict_to_str.items():
        print(f'{key}: {val}')

def main():
    import chromedriver

    driver = webdriver.Chrome(chromedriver.get_path(local=False),
                              chrome_options=chromedriver.camo())
    input(f'{url = !s}')
    print_dict(scrap(driver))
    input('exit')
    driver.close()


if __name__ == '__main__':  # testea solo el scrapper de bwin
    main()

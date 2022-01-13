# from selenium import webdriver
import time

import pandas as pd
# import sys
# TODO hacer un paquete chido para que todo se importe solo
# mágicamente coge los archivos del subdirectorio, pycharm no detecta que se use pero es mentira
from scrap_modules import *


red = '\33[91m'
yellow = '\33[93m'
blue = '\33[94m'
reset = '\33[0m'


# encuentra todos los scrappers y los pone en un diccionario {modulo: url}
dictardo = {mod: mod.url for ref, mod in globals().items() if '_scrap' in ref}
#diccionario vacio para guardar los modulos filtrados
modulos = {}
# TODO que casas usamos
nombre_casas = []

# quita el _scrap del nombre de los archivos
def format_name(string):
    return string.split('.')[1].split('_')[0]


# para testeo, ignorable
if __name__ == '__main__':
    print(f'{dir()}\n{globals()}')
    droplist = input(
        f'Modulos importados: {[format_name(mod.__name__) for mod in dictardo]}\ndroplist: (space separated):').split()
    modulos.update({key: val for key, val in dictardo.items() if format_name(key.__name__) not in droplist})
    nombre_casas[:] = [format_name(mod.__name__) for mod in modulos]
    print(f'{modulos}\n{nombre_casas}\n{dictardo}')


# inicia ventanas automaticamente para que los handles esten en orden:
def init_browser(driver):
    n_casas = len(modulos) - 1
    for i in range(n_casas):
        driver.switch_to.window(driver.window_handles[i])
        driver.execute_script("window.open()")


# comprueba si vale la pena apostar si hay cuotas a, b
def z(a, b):
    return a * b - (a + b)


# {partido: [cuota1, cuota2]} -> {partido: cuota1}, {partido: cuota2}. dict_cuotas == cuotas de *una* casa
def split_cuotas(dict_cuotas):
    keys = [key for key in dict_cuotas.keys()]
    values_1 = [cuotas[0] for cuotas in dict_cuotas.values()]
    values_2 = [cuotas[1] for cuotas in dict_cuotas.values()]

    cuota_1 = dict(zip(keys, values_1))  # {partido: cuota1}
    cuota_2 = dict(zip(keys, values_2))  # {partido: cuota2}

    return cuota_1, cuota_2


# dataframe de una sola cuota, hay que pasarle listado de nombres de casas en el orden que las scrapeamos
def build_dataframe(casas_cuota):
    cuota_frame = pd.DataFrame()
    for idx, casa in enumerate(casas_cuota):  # por cada data de cada casa
        series = pd.Series(casa)  # convierte la data a series

        # chapuza para coger el numbre de la casa
        # TODO arreglar la chapuza para que sea mas automatico
        nombre = nombre_casas[idx]

        # añade al dataframe, hay que hacer reassign because pandas
        cuota_frame = cuota_frame.merge(series.rename(nombre), left_index=True, right_index=True, how='outer')

    return cuota_frame


# une los maximos e indices en un dataframe para tener la info ordenada
def big_merge(cuota_1, cuota_2, casa_1, casa_2):
    cuota_summary = pd.concat([cuota_1, cuota_2], axis=1)
    casa_summary = pd.concat([casa_1, casa_2], axis=1)
    data_summary = cuota_summary.merge(casa_summary, left_index=True, right_index=True, how='outer')
    data_summary.columns = ['cuota 1', 'cuota 2', 'mejor casa 1', 'mejor casa 2']
    return data_summary


def big_scrap(driver):
    casas = []  # lista vacia donde guardar los datos de las casas
    # listas para guardar dicts de {partido: una cuota}
    casas_cuota_1 = []
    casas_cuota_2 = []

    # TODO scrapea las paginas
    # asume data: {partido: [cuota 1, cuota 2]}

    # TODO quitar el range, necesita testear
    # for i in range(len(URLs)):
    #    driver.switch_to.window(driver.window_handles[i])
    #    data = modulos[i].scrap(driver)
    #    casas.append(data)

    for idx, modulo in enumerate(modulos):
        driver.switch_to.window(driver.window_handles[idx])
        data = modulo.scrap(driver)
        casas.append(data)

    # unir datas en dataframe
    for casa in casas:
        cuota_1, cuota_2 = split_cuotas(casa)
        casas_cuota_1.append(cuota_1)
        casas_cuota_2.append(cuota_2)

    data_cuota_1 = build_dataframe(casas_cuota_1)
    data_cuota_2 = build_dataframe(casas_cuota_2)

    # columnas para saber si hay arbitraje
    mejor_cuota_1 = data_cuota_1.max(axis=1, skipna=True)  # mejor cuota 1 para cada partido
    mejor_casa_1 = data_cuota_1.idxmax(axis=1, skipna=True)  # que casa ofrece la mejor cuota

    mejor_cuota_2 = data_cuota_2.max(axis=1, skipna=True)  # mejor cuota 2 para cada partido
    mejor_casa_2 = data_cuota_2.idxmax(axis=1, skipna=True)  # que casa ofrece la mejor cuota

    data_final = big_merge(mejor_cuota_1, mejor_cuota_2, mejor_casa_1, mejor_casa_2)
    data_final['z'] = z(data_final['cuota 1'], data_final['cuota 2'])
    # printear oportunidades
    print(data_final.sort_values(by='z', ascending=False).head(10))
    return data_final


def BETI(driver):
    droplist = input(
        f'Modulos importados: {[format_name(mod.__name__) for mod in dictardo]}\ndroplist: (space separated):').split()
    modulos.update({mod: mod_url for mod, mod_url in dictardo.items() if format_name(mod.__name__) not in droplist})
    nombre_casas[:] = [format_name(mod.__name__) for mod in modulos]

    print(f'\nScrapeadores activos: {blue}{nombre_casas}\n{red}ELIMINA LOS DOBLES{reset}\nURLs por orden:\n{str(list(modulos.values()))}')

    init_browser(driver)  # abre las paginas en orden
    dineros = int(input('Enter bet cuando las pestañas: '))

    # loop principal del programa
    while dineros > 0:
        data_final = big_scrap(driver)

        # TODO calcular margenes para apostar usando dineros y data final

        # volver a ejecutar loop o salir (<0)
        dineros = int(input('nueva bet:'))

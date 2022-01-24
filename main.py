# from selenium import webdriver
import time

import pandas as pd
import bet_calc as calc
# import sys
# mágicamente coge los archivos del subdirectorio, pycharm no detecta que se use pero es mentira
from scrap_modules import *

red = '\33[91m'
yellow = '\33[93m'
blue = '\33[94m'
reset = '\33[0m'

# mas width para los dataframes
pd.set_option('display.width', 160)

# encuentra todos los scrappers y los pone en un diccionario {modulo: url}
dictardo = {mod: mod.url for ref, mod in globals().items() if '_scrap' in ref}
# diccionario vacio para guardar los modulos filtrados
modulos = {}
# que casas usamos
nombre_casas = []


# quita el _scrap del nombre de los archivos
def format_name(string):
    return string.split('.')[1].split('_')[0]


# inicia ventanas automaticamente para que los handles esten en orden:
def init_browser(driver):
    n_casas = len(modulos) - 1
    for i in range(n_casas):
        driver.switch_to.window(driver.window_handles[i])
        driver.execute_script("window.open()")


# comprueba si vale la pena apostar si hay cuotas a, b
def z(a, b) -> float:
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
def build_dataframe(casas_cuota) -> pd.DataFrame:
    cuota_frame = pd.DataFrame()
    for idx, casa in enumerate(casas_cuota):  # por cada data de cada casa
        series = pd.Series(casa)  # convierte la data a series

        # chapuza para coger el numbre de la casa
        nombre = nombre_casas[idx]

        # añade al dataframe, hay que hacer reassign because pandas
        cuota_frame = cuota_frame.merge(series.rename(nombre), left_index=True, right_index=True, how='outer')

    return cuota_frame


# une los maximos e indices en un dataframe para tener la info ordenada
def big_merge(cuota_1, cuota_2, casa_1, casa_2) -> pd.DataFrame:
    cuota_summary = pd.concat([cuota_1, cuota_2], axis=1)
    casa_summary = pd.concat([casa_1, casa_2], axis=1)
    data_summary = cuota_summary.merge(casa_summary, left_index=True, right_index=True, how='outer')
    data_summary.columns = ['cuota 1', 'cuota 2', 'mejor casa 1', 'mejor casa 2']
    return data_summary


# scrapea las paginas como todo un chad
def big_scrap(driver) -> pd.DataFrame:
    # lista vacia donde guardar los datos de las casas
    casas = []
    # listas para guardar dicts de {partido: una cuota}
    casas_cuota_1 = []
    casas_cuota_2 = []

    # scrapea las paginas usando los modulos
    for idx, modulo in enumerate(modulos):
        driver.switch_to.window(driver.window_handles[idx])
        try:
            data = modulo.scrap(driver)
        except Exception:  # intento de evitar que el programa pete, seguramente mejorable
            print(
                f'{red}Unexpected error using {modulo.__name__}!{reset} Check browser page or run module in isolation to debug')
            data = {}
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


def enter_bet(msg):
    try:
        dineros = int(input(msg))
    except ValueError:
        print(f'{red}Invalid amount. Executing with default value: {yellow}100{reset}')
        dineros = 100
    return dineros


def url_display():
    display = ''
    for idx, url in enumerate(list(modulos.values()), start=1):
        display = f'{display}{idx}: {url!s}\n'
    return display


def BETI(driver):
    beti_list = input(
        f'Modulos importados: {[format_name(mod.__name__) for mod in dictardo]}\ndroplist (space separated): ').split()
    modulos.update({mod: mod_url for mod, mod_url in dictardo.items() if format_name(mod.__name__) not in beti_list})
    nombre_casas[:] = [format_name(mod.__name__) for mod in modulos]

    print(
        f'\nScrapeadores activos: {blue}{nombre_casas}\n{red}ELIMINA LOS DOBLES{reset}\nURLs por orden:\n{url_display()}')

    init_browser(driver)  # abre las paginas en orden
    dineros = enter_bet(f'{yellow}Enter bet cuando las pestañas:{reset} ')

    # loop principal del programa
    while dineros > 0:
        data_final = big_scrap(driver)

        # TODO calcular margenes para apostar usando dineros y data final
        arbiter = calc.bet_frame(data_final, dineros)
        if not arbiter.empty:
            print(f'\n\n{yellow}Posibilidades de arbitraje:\n{reset}{arbiter}\n')
        # volver a ejecutar loop o salir (<0)
        dineros = enter_bet(f'{yellow}nueva bet:{reset} ')

    # TODO esto solo cierra una ventana lol
    for i in range(len(modulos)):
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()


if __name__ == '__main__':
    print(f'{dir()}\n{globals()}')
    droplist = input(
        f'Modulos importados: {[format_name(mod.__name__) for mod in dictardo]}\ndroplist (space separated):').split()
    modulos.update({key: val for key, val in dictardo.items() if format_name(key.__name__) not in droplist})
    nombre_casas[:] = [format_name(mod.__name__) for mod in modulos]
    print(f'{modulos}\n{nombre_casas}\n{dictardo}')

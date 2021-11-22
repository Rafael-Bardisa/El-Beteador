# from selenium import webdriver
import pandas as pd
# import time
# import sys
import bet365_chromedriver13_11_2021 as bet  # import scrapping para bet365
import william_scrap as will # import scrapping para william hill
import betway_scrap as bway # import scrapping para betway

URLs = ["https://sports.williamhill.es/betting/es-es/en-directo/tenis",
        "https://betway.es/es/sports/sct/tennis/challenger"]


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
def build_dataframe(casas_cuota, nombre_casas):
    cuota_frame = pd.DataFrame()
    for casa in casas_cuota:  # por cada data de cada casa
        series = pd.Series(casa)  # convierte la data a series

        # chapuza para coger el numbre de la casa
        # TODO arreglar la chapuza para que sea mas automatico
        nombre = nombre_casas[casas_cuota.index(casa)]

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


def BETI(driver):


    # TODO que casas usamos
    nombre_casas = ['william', 'betway']

    # llevar a los drivers a las casas
    action = '0'  # valor inicial random
    #bet.go(driver)
    print('ELIMINA LOS DOBLES')
    print('URLs por orden:\n' + str(URLs))
    ejecutar = input('Enter cuando las pestañas:')
    # loop principal del programa
    while 1:

        casas = []  # lista vacia donde guardar los datos de las casas
        # listas para guardar dicts de {partido: una cuota}
        casas_cuota_1 = []
        casas_cuota_2 = []

        # TODO scrapea las paginas

        # asume data: {partido: [cuota 1, cuota 2]}
        driver.switch_to.window(driver.window_handles[0])
        data = will.scrap(driver)
        casas.append(data)
        driver.switch_to.window(driver.window_handles[1])
        data = bway.scrap(driver)
        casas.append(data)

        # unir datas en dataframe
        for i in range(0, len(casas)):
            cuota_1, cuota_2 = split_cuotas(casas[i])
            casas_cuota_1.append(cuota_1)
            casas_cuota_2.append(cuota_2)

        data_cuota_1 = build_dataframe(casas_cuota_1, nombre_casas)
        data_cuota_2 = build_dataframe(casas_cuota_2, nombre_casas)

        # columnas para saber si hay arbitraje
        mejor_cuota_1 = data_cuota_1.max(axis=1, skipna=True)  # mejor cuota 1 para cada partido
        mejor_casa_1 = data_cuota_1.idxmax(axis=1, skipna=True)  # que casa ofrece la mejor cuota

        mejor_cuota_2 = data_cuota_2.max(axis=1, skipna=True)  # mejor cuota 2 para cada partido
        mejor_casa_2 = data_cuota_2.idxmax(axis=1, skipna=True)  # que casa ofrece la mejor cuota

        data_final = big_merge(mejor_cuota_1, mejor_cuota_2, mejor_casa_1, mejor_casa_2)
        data_final['z'] = z(data_final['cuota 1'], data_final['cuota 2'])
        # printear oportunidades
        print(data_final.sort_values( by ='z', ascending = False).head(10))

        # volver a ejecutar loop o salir (0)
        action = input(action)
        if action == '0':
            return 0


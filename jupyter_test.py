# imports
import numpy as np
import pandas as pd
import random as rd


def z(a, b):  # el testeador
    return a * b - (a + b)


# lista de partidos random, importante estandarizar para todas las casas xd
partidos = ['partido_1', 'partido_2', 'partido_3', 'partido_4', 'partido_5', 'partido_6', 'partido_7']

cuotas = [[1.2, 3], [1.1, 10], [1.6, 2.1], [2, 1.8], [1.3, 3.3], [3, 1.3], [5, 1.3], [1.4, 2.9], [5, 1.25], [1.7, 1.9], [1.3, 2.7], [3.1, 1.4],
          [1.8, 2.5], [11, 1.05], [7, 1.5]]  # lista de cuotas random, multilinea por ser muy larga


def rand_data():
    data_dict = {}
    j = rd.randrange(5) + 1  # random [1,5]
    for i in range(0, j):  # repite j veces
        partido = partidos[rd.randrange(len(partidos))]  # partido random
        cuota = cuotas[rd.randrange(len(cuotas))]  # cuota random
        data_dict[partido] = cuota  # formato dict
    return data_dict


rand_data()  # data que una casa podria tener

# lista de datas de casas random
n = 9
casas = []
nombre_casas = ['bet365', 'william hill', 'codere', 'botemania', 'babeador', 'pickle', 'carlos', 'marcos', 'tiburon']
for i in range(0, n):  # repite n veces
    casas.append(rand_data())

#casas[3]  # check de la tercera casa por ejemplo

casas_cuota_1 = []
casas_cuota_2 = []


def split_cuotas(dict_cuotas):  # {partido: [cuota1, cuota2]} -> {partido: cuota1}, {partido: cuota2}

    keys = [key for key in dict_cuotas.keys()]
    values_1 = [cuotas[0] for cuotas in dict_cuotas.values()]
    values_2 = [cuotas[1] for cuotas in dict_cuotas.values()]

    cuota_1 = dict(zip(keys, values_1))  # {partido: cuota1}
    cuota_2 = dict(zip(keys, values_2))  # {partido: cuota2}

    return cuota_1, cuota_2


for i in range(0, len(casas)):
    cuota_1, cuota_2 = split_cuotas(casas[i])
    casas_cuota_1.append(cuota_1)
    casas_cuota_2.append(cuota_2)

#casas_cuota_1[3]


def build_dataframe(casas_cuota):  # dataframe de una sola cuota
    cuota_frame = pd.DataFrame()
    for casa in casas_cuota:  # por cada data de cada casa
        series = pd.Series(casa)  # convierte la data a series

        # chapuza para coger el numbre de la casa
        nombre = nombre_casas[casas_cuota.index(casa)]

        # añade al dataframe, hay que hacer reassign because pandas
        cuota_frame = cuota_frame.merge(series.rename(nombre), left_index=True, right_index=True, how='outer')

    return cuota_frame


data_cuota_1 = build_dataframe(casas_cuota_1)
#data_cuota_1

data_cuota_2 = build_dataframe(casas_cuota_2)
#data_cuota_2

mejor_cuota_1 = data_cuota_1.max(axis=1, skipna=True)  # mejor cuota 1 para cada partido
mejor_casa_1 = data_cuota_1.idxmax(axis=1, skipna=True)  # que casa ofrece la mejor cuota

mejor_cuota_2 = data_cuota_2.max(axis=1, skipna=True)  # mejor cuota 2 para cada partido
mejor_casa_2 = data_cuota_2.idxmax(axis=1, skipna=True)  # que casa ofrece la mejor cuota


def big_merge():  # une los maximos e indices en un dataframe para tener la info ordenada
    cuota_summary = pd.concat([mejor_cuota_1, mejor_cuota_2], axis=1)
    casa_summary = pd.concat([mejor_casa_1, mejor_casa_2], axis=1)
    data_summary = cuota_summary.merge(casa_summary, left_index=True, right_index=True, how='outer')
    data_summary.columns = ['cuota 1', 'cuota 2', 'mejor casa 1', 'mejor casa 2']
    return data_summary


data_final = big_merge()

#data_final

data_final['z'] = z(data_final['cuota 1'],
                    data_final['cuota 2'])  # chequear si vale la pena apostar, nombres scuffed xd

#data_final  # resumen final


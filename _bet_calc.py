from typing import Tuple
import pandas as pd


def f(quota: float) -> float:  # auxiliar
    '''
    Function that calculates the minimum quota such that the expected return of a bet is greater or equal to 0
    :param quota: The given quota to calculate the minimum value of the second quota in order not to lose money 
    :return: the needed quota for safe bets 
    '''
    return quota/(quota - 1)


def split(cuota_1: float, cuota_2: float) -> Tuple[float, float]:  # te hace split de que fraccion apostar segun las cuotas
    '''
    insert \"cuota_1\" and \"cuota_2\" as arguments, get cuota_2/sum, cuota_1/sum
    '''
    total = cuota_1 + cuota_2
    return cuota_2/total, cuota_1/total


def bet_range(cuota_1: float, cuota_2: float, bet) -> Tuple[str, str]:  # rangos en los que se puede apostar con arbitraje
    c_2_ast = f(cuota_1)  # cuota 2 si z fuese 0
    c_1_ast = f(cuota_2)  # cuota 1 si z fuese 0
    #  margenes en los que no se pierde dinero
    bet_given_1 = split(cuota_1, c_2_ast)
    bet_given_2 = split(c_1_ast, cuota_2)
    # strings para representar en el dataframe, no deja usar f strings :(
    margenes_bet_1 = f'[{bet * bet_given_1[0]:.3f} - {bet * bet_given_2[0]:.3f}]'
    margenes_bet_2 = f'[{bet * bet_given_1[1]:.3f} - {bet * bet_given_2[1]:.3f}]'
    # print(margenes_bet_1)
    # print(margenes_bet_2)
    # margenes_bet_1 = [bet_given_1[0], bet_given_2[0]]
    # margenes_bet_2 = [bet_given_1[1], bet_given_2[1]]
    return margenes_bet_1, margenes_bet_2


def bet_size(c_1: float, c_2: float, bet):
    profits=-1
    if c_1 <= c_2:
        while profits <= 0:
            bet = bet+1
            bet_1 = bet
            bet_2 = round(bet_1*(c_1/c_2))
            profits = (c_1*bet_1-bet_1-bet_2)*(c_2*bet_2-bet_1-bet_2)
    else:
        while profits <= 0:
            bet = bet+1
            bet_2 = bet
            bet_1 = round(bet_2*(c_2/c_1))
            profits = (c_1*bet_1-bet_1-bet_2)*(c_2*bet_2-bet_1-bet_2)
    return bet_1, bet_2

def bet_frame(data_frame: pd.DataFrame, bet) -> pd.DataFrame:  # con el dataframe final calcula las apuestas (si hay)
    # diccionario para construir series easy
    arbitraje = data_frame[data_frame['z'] > 0].copy(deep=True)
    bet_1 = {}
    bet_2 = {}
    for idx, row in arbitraje.iterrows():
        # calcula el rango de la bet
        bet_range_1, bet_range_2 = bet_range(row["cuota 1"], row["cuota 2"], bet)
        bet_1[idx] = bet_range_1
        bet_2[idx] = bet_range_2

    bet_1_series = pd.Series(bet_1)
    bet_2_series = pd.Series(bet_2)
    # junta todo y devuelve el dataframe
    arbitraje = arbitraje.merge(bet_1_series.rename('bet 1'), left_index=True, right_index=True)
    arbitraje = arbitraje.merge(bet_2_series.rename('bet 2'), left_index=True, right_index=True)

    return arbitraje

# TODO calcular bets dada bet maxima a la cuota mas baja
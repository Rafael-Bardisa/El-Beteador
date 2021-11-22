from selenium import webdriver
import pandas
import time
import sys
import bet365_scrap as bet #import scrapping para bet365
from multiprocessing import Process, Pipe

'''
def bet_scrap(driver, proc_pipe):
    data = bet.scrap(driver)
    proc_pipe.send(data)
    proc_pipe.close()

'''

# comprueba si vale la pena apostar si hay cuotas a, b
def z(a, b):
    return a*b - (a+b)


def BETEADOR(driver):
    #llevar a los drivers a las casas
    action = '0'
    bet.go(driver)

    #loop principal del programa
    while 1:
        #scrapea las paginas

        #asume data: {partido: [cuota 1, cuota 2]}
        data = bet.scrap(driver)

        #unir datas en dataframe


        #columnas para saber si hay arbitraje


        #printear oportunidades
        print(data)

        #volver a ejecutar loop o salir (0)
        action = input(action)
        if action == '0':
            return 0



# dos subprocesses, uno para cada casa
# loop hasta cerrar el programa:
'''
procesos devuelven data scrapeada
usar pandas dataframe para unir los mismos partidos
comprobar arbitraje segun cuotas
'''
# cerrar subprocesses

#opciones de chrome para intentar camuflar el driver
def camo():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery");
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=RealBeti")


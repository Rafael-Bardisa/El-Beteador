#from selenium import webdriver
import pandas
import time
import sys
from multiprocessing import Process, Pipe


def placeholder(driver):
    #driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver")
    bet365 = "https://www.bet365.es/#/OF/"
    codere = "https://www.codere.es/"

    #Entra en Bet365
    driver.get(bet365)

    #Espera y entra en tenis
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div[29]").click()

    #Espera y entra en la lista de partidos
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div[1]/span").click()


    databet365 = pandas.DataFrame()

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()

# dos subprocesses, uno para cada casa
#loop hasta cerrar el programa:
'''
procesos devuelven data scrapeada
usar pandas dataframe para unir los mismos partidos
comprobar arbitraje segun cuotas
'''
#cerrar subprocesses





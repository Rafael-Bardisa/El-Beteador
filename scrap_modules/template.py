def write_template(name):   # xd moment
    with open(f'{name}_scrap.py', 'x') as scrapper:
        imports = f'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nimport pandas\n'
        url = f"# url de la pagina:\nurl = ''\n"
        formato = '{match: [cuota 1, cuota 2]}'
        docstring = f'\t"""\n\tScrapea la pagina {name} y recoge las cuotas de los partidos de tenis\n\t:param driver: referencia a un driver de selenium\n\t:return william_dict: diccionario estilo {formato}\n\t"""'
        nuldict = '{}'
        scrap = f'def scrap(driver):\n'
        func = f'{scrap}{docstring}\n\t# diccionario a llenar con las datas scrapeadas\n\t{name}_dict = {nuldict}\n\t\n\treturn {name}_dict\n'
        furl = "f'{url = !s}'"
        driver = f'driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver",\n\t\t\t\t\t\t\t\tchrome_options=chromedriver.camo())\n\t'
        testfunc = f"def main(): # de testeo para comprobar que la funcion va bien\n\timport chromedriver\n\t\n\t{driver}input({furl})\n\tprint(scrap(driver))\n\tinput('exit')\n"
        nameguard = f"if __name__ == '__main__':  # testea solo el scrapper de william\n\tmain()"
        print(f'{imports}\n\n{url}\n\n{func}\n\n{testfunc}\n\n{nameguard}', file=scrapper)


def main():
    red = '\33[91m'
    reset = '\33[0m'
    blue = '\33[94m'

    teststring = input(f'Enter module name\nExample: {blue}william{reset}_scrap.py\n\nModule: ')
    try:
        write_template(teststring)
    except FileExistsError:
        print(f'{red}File already exists!{reset}')
    else:
        print(f'{blue}File created!{reset}')


if __name__ == '__main__':
    main()

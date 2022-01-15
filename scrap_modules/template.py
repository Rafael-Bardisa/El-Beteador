def write_template(name):  # xd moment
    """
    Crea el template de un archivo de scraper con solo darle el nombre
    peta si el archivo que va a crear ya existe
    :param name: {name}_scrap.py el nombre del archivo
    """
    with open(f'{name}_scrap.py', 'x') as scrapper:
        imports = f'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nimport pandas\n'
        url = f"# url de la pagina:\nurl = ''\n"
        formato = '{match: [cuota 1, cuota 2]}'
        docstring = f'\t"""\n\tScrapea la pagina {name} y recoge las cuotas de los partidos de tenis\n\t:param driver: referencia a un driver de selenium\n\t:return william_dict: diccionario estilo {formato}\n\t"""'
        nuldict = '{}'
        scrap = f'def scrap(driver) -> dict:\n'
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


    new_files = input(f'Enter module names (space separated)\nExample name: {blue}william{reset}_scrap.py\n\nModule: ').split()
    for new_file in new_files:
        try:
            write_template(new_file)
        except FileExistsError:  # pilla que la funcion ha petado y te lo dice en rojo
            print(f'{red}{new_file}_scrap file already exists!{reset}')
        else:  # pilla que la funcion NO ha petado y te lo dice en azul
            print(f'{blue}{new_file}_scrap file created!{reset}')


if __name__ == '__main__':
    main()

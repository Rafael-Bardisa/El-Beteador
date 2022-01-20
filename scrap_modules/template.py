def write_template(name):  # xd moment
    """
    Crea el template de un archivo de scraper con solo darle el nombre
    peta si el archivo que va a crear ya existe
    :param name: {name}_scrap.py el nombre del archivo
    """
    with open(f'{name}_scrap.py', 'x') as scrapper:
        imports = f'from selenium import webdriver\nfrom selenium.webdriver.common.by import By\nimport pandas\n'
        url = "# url de la pagina:\nurl = ''\n"
        formato = '{match: [cuota 1, cuota 2]}'
        docstring = f'\t"""\n\tScrapea la pagina {name} y recoge las cuotas de los partidos de tenis\n\t:param driver: referencia a un driver de selenium\n\t:return {name}_dict: diccionario estilo {formato}\n\t"""'
        j_map = '{return match.innerText}'
        jScript = f'jScript = """const {name}matches = Array.prototype.slice.call(document.getElementsBy########("########"))\nreturn {name}matches.map(function (match){j_map})"""\n\t'
        scrap_data = f'{name}_data = driver.execute_script(jScript)\n\t'
        nuldict = '{}'
        scrap = 'def scrap(driver) -> dict:\n'
        func = f'{scrap}{docstring}\n\t# replacea los ######## por lo que usarias con el driver find elements\n\t{jScript}\n\t{scrap_data}\n\t# diccionario a llenar con las datas scrapeadas\n\t{name}_dict = {nuldict}\n\n\treturn {name}_dict\n'
        furl = "f'{url = !s}'"
        print_statement = "f'{key}: {val}'"
        print_dict = f"def print_dict(dict_to_str):\n\tfor key, val in dict_to_str.items():\n\t\tprint({print_statement})\n"
        driver = f'driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver",\n\t\t\t\t\t\t\t\tchrome_options=chromedriver.camo())\n\t'
        testfunc = f"def main(): # de testeo para comprobar que la funcion va bien\n\timport chromedriver\n\n\t{driver}input({furl})\n\tprint_dict(scrap(driver))\n\tinput('exit')\n\tdriver.close()\n"
        nameguard = f"if __name__ == '__main__':  # testea solo el scrapper de william\n\tmain()"
        print(f'{imports}\n\n{url}\n\n{func}\n\n{print_dict}\n\n{testfunc}\n\n{nameguard}', file=scrapper)


def main():
    red = '\33[91m'
    reset = '\33[0m'
    blue = '\33[94m'


    new_files = input(f'Enter module names (space separated)\nExample name: {blue}william{reset}_scrap.py\n\nModule: ').split()
    for new_file in new_files:
        try:
            if '_scrap.py' in new_file:  # permite escribir tambien la extension
                new_file = new_file.split('_')[0]
            write_template(new_file)
        except FileExistsError:  # pilla que la funcion ha petado y te lo dice en rojo
            print(f'{red}{new_file}_scrap file already exists!{reset}')
        else:  # pilla que la funcion NO ha petado y te lo dice en azul
            print(f'{blue}{new_file}_scrap file created!{reset}')


if __name__ == '__main__':
    main()

def write_template(name, local=False):  # xd moment
    """
    Crea el template de un archivo de scraper con solo darle el nombre
    peta si el archivo que va a crear ya existe
    :param local: whether file is executed locally or not
    :param name: {name}_scrap.py el nombre del archivo
    """
    scope = "scrap_modules" if not local else "."

    beti_template_path = f"{scope}/template_scrap.txt"
    javascript_scrap_template_path = f"{scope}/javascript_scrapers/template_scrap.txt"
    javascript_hydrater_template_path = f"{scope}/javascript_hydraters/template_hydrater.txt"

    file_path = f"{scope}/{name}_scrap.py"
    javascript_scraper_path = f"{scope}/javascript_scrapers/{name}_scrap.js"
    javascript_hydrater_path = f"{scope}/javascript_hydraters/{name}_hydrater.js"


    with open(beti_template_path, 'r') as template_file:
        beti_template = template_file.read()

    with open(javascript_scrap_template_path, 'r') as template_file:
        javascript_scraper_template = template_file.read()

    with open(javascript_hydrater_template_path, 'r') as template_file:
        javascript_hydrater_template = template_file.read()


    with open(file_path, 'x') as scraper_file:
        beti_script = beti_template.format(
            name=name,
            dict="{}",
            match_format="{match: [odd 1, odd 2]}",
            js_script="{js_script}",
            raw_data=f"{{{name}_data}}",
            parsed_data=f"{{{name}_dict}}",
            key="{key}",
            val="{val}",
            url_fmt = "{url = !s}"
        )
        print(beti_script, file=scraper_file)

    with open(javascript_scraper_path, 'x') as js_scraper_file:
        js_script = javascript_scraper_template.format(
            name=name,
            script_return="{return match.innerText}"
        )
        print(js_script, file=js_scraper_file)

    with open(javascript_hydrater_path, 'x') as js_hydrater_file:
        js_script = javascript_hydrater_template
        print(js_script, file=js_hydrater_file)



def gen_file(local=False):
    red = '\33[91m'
    reset = '\33[0m'
    blue = '\33[94m'


    new_files = input(f'Enter module names (space separated)\nExample name: {blue}william{reset}_scrap.py\n\nModule: ').split()
    for new_file in new_files:
        try:
            if '_scrap.py' in new_file:  # permite escribir tambien la extension
                new_file = new_file.split('_')[0]
            write_template(new_file, local=local)
        except FileExistsError:  # pilla que la funcion ha petado y te lo dice en rojo
            print(f'{red}{new_file}_scrap module already exists!{reset}')
        else:  # pilla que la funcion NO ha petado y te lo dice en azul
            print(f'{blue}{new_file}_scrap module created!{reset}')


if __name__ == '__main__':
    gen_file(local=True)

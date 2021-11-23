from selenium import webdriver
import pandas
import chromedriver

#driv = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
#bwin = "https://sports.bwin.es/es/sports/tenis-5/apuestas"

def scrap (driver):
    bwinmatch = driver.find_elements_by_class_name("grid-event-wrapper")
    # bwinmatch[0].text

    match = []
    # Extrae cuotas y nombres
    bwincuotas = []
    bwinnames = []
    for i in range(len(bwinmatch) * 2):
        match = bwinmatch[i // 2].text.split('\n')
        if i % 2 == 0:
            bwincuotas.append(match[(len(match) - 2)])
            bwinnames.append(match[0])
        else:
            bwincuotas.append(match[(len(match) - 1)])
            bwinnames.append(match[1])
        # convierte los elementos de las cuotas a numeros
        bwincuotas[i] = pandas.to_numeric(bwincuotas[i])

    print(bwincuotas)
    print(bwinnames)
    truebwinnames = []
    for elem in bwinnames:
        fullname = elem.split()
        name_size = len(fullname)

        name = fullname[0][0]
        if (name_size == 2):
            surname = fullname[1][0:-3]
        else:
            surname = fullname[1]
        truebwinnames.append(surname + " " + name)

    print(truebwinnames)

    # crea el diccionario magico que usa el main para crear la dataframe final
    bwin_dict = {}
    for i in range(len(truebwinnames)):
        bwin_dict[truebwinnames[i]] = [bwincuotas[i * 2], bwincuotas[(i * 2) + 1]]
    return bwin_dict

if __name__ == '__main__':
        driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
        a = input('wait')
        scrap(driver)
        

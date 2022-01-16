from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas


# url de la pagina:
url = 'https://www.betfred.es/ES/512/sports#bo-navigation=356554.1&action=market-group-list'



def split_match_names(names):
    
    split_names = []
    for elem in names:
        names1 = elem.split(' v ')
        match_names = []
        for i in names1:

            surnames, name = i.split(', ')
            surname = surnames.split()[0]
            name = name[0]
            match_names.append(f'{surname} {name}')
        split_names.append(f'{match_names[0]} {match_names[1]}')
    return split_names




def scrap(driver) -> dict:

    betfreddata = []
    betfredweb = driver.find_elements_by_tag_name("td")

    for webelem in betfredweb:
        betfreddata.append(webelem.text)

    data_filter = [dataelem for dataelem in betfreddata if not (dataelem == '' or dataelem[0] in ['-','+']) ]

    cuota1 = map(pandas.to_numeric, data_filter[2::4])
    cuota2 = map(pandas.to_numeric, data_filter[3::4])

    betfredrawnames = data_filter[1::4]

    betfrednames = split_match_names(betfredrawnames)
    
    betfred_dict = {name: cuotas for name, cuotas in
                    zip(betfrednames, map(list, zip(cuota1, cuota2)))}
     
    return betfred_dict


def main(): # de testeo para comprobar que la funcion va bien
    import chromedriver

    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver",
                                chrome_options=chromedriver.camo())
    input(f'{url = !s}')
    print(scrap(driver))
    input('exit')


if __name__ == '__main__':  # testea solo el scrapper de william
    main()

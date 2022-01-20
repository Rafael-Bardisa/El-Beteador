from selenium import webdriver
import pandas
import benchmarking

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

    # El bicho magico de la velocidad
    jScript = """const bfredmatches = Array.prototype.slice.call(document.getElementsByTagName("td"))
return bfredmatches.map(function (match){
    return match.innerText
})"""
    betfredjsdata = driver.execute_script(jScript)

    vs_pos = [idx for idx, elem in enumerate(betfredjsdata) if elem == '-']

    betfred_raw_names = [betfredjsdata[idx - 2] for idx in vs_pos]
    cuota_text_1 = [betfredjsdata[idx - 1] for idx in vs_pos]
    cuota_text_2 = [betfredjsdata[idx + 1] for idx in vs_pos]

    cuota_1 = list(pandas.to_numeric(cuota_text_1))
    cuota_2 = list(pandas.to_numeric(cuota_text_2))

    betfred_names = split_match_names(betfred_raw_names)
    
    betfred_dict = {name: cuotas for name, cuotas in
                    zip(betfred_names, map(list, zip(cuota_1, cuota_2)))}
     
    return betfred_dict


def print_dict(dict_to_str):
    for key, val in dict_to_str.items():
        print(f'{key}: {val}')

def main():
    import chromedriver

    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver",
                              chrome_options=chromedriver.camo())
    input(f'{url = !s}')
    print_dict(scrap(driver))
    input('exit')
    driver.close()

if __name__ == '__main__':  # testea solo el scrapper de william
    main()

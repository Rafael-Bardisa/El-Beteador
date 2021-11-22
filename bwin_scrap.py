from selenium import webdriver
import pandas

driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
bwin = "https://sports.bwin.es/es/sports/tenis-5/apuestas"


driv.get(bwin)

bwinmatch = driv.find_elements_by_class_name("grid-event-wrapper")
#bwinmatch[0].text

match = []

# Extrae cuotas    
bwincuotas = []
for i in range(len(bwinmatch)*2):
    match  = bwinmatch[i//2].text.split('\n')
    if i % 2 ==0:
        bwincuotas.append(match[(len(match)-2)])
    else:
        bwincuotas.append(match[(len(match)-1)])



# convierte los elementos de las cuotas a numeros
for i in range(len(bwincuotas)):
    bwincuotas[i] = pandas.to_numeric(bwincuotas[i].text)



# Extrae nombres
bwinnames = []
for i in range(2*len(bwinmatch)):
    match = bwinmatch[i//2].text.split('\n')
    if i % 2 ==0:
        bwinnames.append(match[0])
    else:
        bwinnames.append(match[1])

        
        
        

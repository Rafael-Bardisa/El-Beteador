from selenium import webdriver
import pandas

driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
bwin = "https://sports.bwin.es/es/sports/tenis-5/apuestas"


driv.get(bwin)

bwincuotas = driv.find_elements_by_class_name("grid-event-wrapper")
bwincuotas[1].text
bwincuotas[2].text
bwincuotas[3].text
bwincuotas[4].text
bwincuotas[5].text
bwincuotas[6].text
bwincuotas[7].text
bwincuotas[8].text


bwinnames  = driv.find_elements_by_class_name("scoreboardInfoNames")
bwinnames[0].text

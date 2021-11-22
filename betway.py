from selenium import webdriver
import pandas

driv = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96")
betway = "https://betway.es/es/sports/sct/tennis/challenger"


driv.get(betway)

betwaycuotas = driv.find_elements_by_class_name("oddsDisplay")
betwaycuotas[58].get_attribute("innerText")
betwaynames  = driv.find_elements_by_class_name("scoreboardInfoNames")
betwaynames[57].text

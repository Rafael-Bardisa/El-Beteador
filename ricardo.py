from selenium import webdriver
import chromedriver
import main as beteador

if __name__ == '__main__':
    driver = webdriver.Chrome("C:/Users/Usuario/Desktop/Bets/chromedriver96", chrome_options=chromedriver.camo())
    beteador.BETI(driver)

    

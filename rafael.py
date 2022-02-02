from selenium import webdriver
import chromedriver
import beti_scrap as beteador
# gracias Cerundolo JM

if __name__ == '__main__':

    #name = 'hola  buenas'
    #print(name.split(' '))
    #print(chromedriver.z(5.5, 1.2))
    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
    #driver_2 = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver")
    #driver.execute_script("window.open()")
    #driver.switch_to.window(driver.window_handles[3])
    #driver.get("https://youtube.com")

    beteador.betizador(driver)
    #driver.delete_all_cookies()
    #driver.set_window_size(800, 800)
    #driver.set_window_position(0, 0)
    #chromedriver.BETEADOR(driver)


    #driver.get("https://linkedin.com")
    # open new tab
    #driver.execute_script("window.open('https://twitter.com')")
    #g = input('continue')
    #print (driver.current_window_handle)

    # Switch to new window
    #driver.switch_to.window(driver.window_handles[-1])
    #print (" Twitter window should go to facebook ")
    #print ("New window ", driver.title)
    #driver.get("http://facebook.com")
    #print ("New window ", driver.title)

    # Switch to old window
    #driver.switch_to.window(driver.window_handles[0])
    #print (" Linkedin should go to gmail ")
    #print ("Old window ", driver.title)
    #driver.get("http://gmail.com")
    #print ("Old window ", driver.title)

    # Again new window
    #driver.switch_to.window(driver.window_handles[1])
    #print (" Facebook window should go to Google ")
    #print ("New window ", driver.title)
    #driver.get("http://google.com")
    #print ("New window ", driver.title)


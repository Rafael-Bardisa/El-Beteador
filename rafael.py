from selenium import webdriver
import chromedriver

if __name__ == '__main__':
    driver = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver", chrome_options=chromedriver.camo())
    #driver_2 = webdriver.Chrome("/Users/rafaelbardisarodes/Desktop/beteador/chromedriver")

    driver.delete_all_cookies()
    driver.set_window_size(800, 800)
    driver.set_window_position(0, 0)
    chromedriver.BETEADOR(driver)

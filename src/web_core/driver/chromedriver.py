from selenium import webdriver
from pathlib import Path
import os

from src.core.interfaces.driver_manager import typeWebDriver


# opciones de chrome para intentar camuflar el driver

def chrome_profile():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-minimized")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    #prefs = {'download.default_directory': os.path.abspath(DOWNLOAD_FOLDER)}
    #chrome_options.add_experimental_option('prefs', prefs)

    return chrome_options

def config_path(path_str):
    """
    writes the chromedriver path to the chromedriver_path.txt
    uses # to distinguish newlines
    :param path_str: the updated path to the chromedriver
    """
    try:
        with open("../../../chromedriver_path.txt", 'w') as dump:
            print(f'#{path_str}#', file=dump)
    except Exception:
        print(f'\33[91mError updating chromedriver path!')


def get_path(local=True):
    """
    reads from chromedriver_path.txt
    :return: path the string representing the path to the chromedriver
    """
    if local:
        path_txt = "../../../chromedriver_path.txt"
    else:
        path_txt = os.path.join(os.path.realpath('../../../..'), "../../../chromedriver_path.txt")

    with open(path_txt, "r") as source:
        path = source.read()
    return path.split('#')[1]


def chrome(*, js_framework_path: Path) -> typeWebDriver:
    with open(js_framework_path / "myQuery.js") as js_framework_file:
        js_framework = js_framework_file.read()

    driver = webdriver.Chrome(options=chrome_profile())
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js_framework})
    return driver

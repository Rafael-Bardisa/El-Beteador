try:
    import sys
    import pandas
    from selenium.common.exceptions import WebDriverException
    from driver_manager import chromedriver
    import beti_scrap
    from scrap_modules.template import gen_file
except ModuleNotFoundError:
    print("\33[91mError: required dependencies not found.\33[0m Install selenium, numpy and pandas in your python environment to execute this script.")


def beti_help():
    print("""\nUsage: python beti.py {option}\nPossible options:
    \33[94m[none]\33[0m: execute the program using the default path
    \33[94m-c {path}\33[0m: update the default path in chromedriver_path.txt
    \33[94m-p {path}\33[0m: run with custom path
    \33[94m-s\33[0m: run template.py to add new scrap templates to the project
    \33[94m-h\33[0m: display the help menu
            \nA valid chromedriver path may look like this: \33[94m'/Direct/Path/To/chromedriver'\33[0m, where chromedriver is the executable
            """)



def handle_program_arguments(args):
    options_args = {'-c': chromedriver.config_path, '-p': run}
    options = {'-s': gen_file, '-h': beti_help}
    option = args[0]
    if option in options_args:
        options_args[option](args[1])
    elif option in options:
        options[option]()


def run(driver_path):
    try:
        driver = chromedriver.chrome()
        beti_scrap.betizador(driver)
    except WebDriverException:
        print(f"\33[91mError: {driver_path} does not lead to a chromedriver executable.\33[0m Run with -h flag for help\33[0m")


def main():
    """
    runs the scrapper program. Works when invoked from the command line
    :return:
    """
    try:
        assert len(sys.argv) < 4
        args = sys.argv[1:]
        if args:
            handle_program_arguments(args)
        else:
            run(chromedriver.get_path())
    except AssertionError:
        beti_help()
    except FileNotFoundError:
        print('\33[91mError: default path to chromedriver not configured.\33[0m Run with -h flag for help\33[0m')


if __name__ == '__main__':
    main()

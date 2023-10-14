from os.path import dirname, basename, isfile, join
import glob

# clasico stack overflow, escanea el directorio y mete todo al carro
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and f.endswith('scrap.py')]

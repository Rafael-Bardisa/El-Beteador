import time
import cProfile
# TODO import cProfile y hacer benchmark para acelerar el codigo
def benchmark(func):
    """
    Decorador que te mide el tiempo que tarda la funcion en ejecutarse.
    Se puede usar como cualquier funcion, e.g. benchmark(func),
    pero al ser un decorador la gracia que tiene es que al hacer
    @benchmark
    def func():...
    cada vez que uses func() estaras usando benchmark(func)()
    :param func: la funcion que quieres testear
    :return: la funcion original envuelta por el codigo de testeo
    """
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Time taken for {func.__name__}: {end - start}')
        return result

    return inner


def cprof(func):
    def replacement(*args, **kwargs):
        prof = cProfile.Profile()
        result = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(f'profiler_dumps/{func.__name__} {time.time()}')
        return result

    return replacement


@benchmark
def fib(n):
    return 1 if n in [1, 2] else (fib(n - 1) + fib(n - 2))


def col(n):
    return f'\33[{n}m'

dicto = {1:3, 2:4, 5:7, 8:9}

def fuckoff(item):
    dicto.pop(item)


if __name__ == '__main__':
    input(f'\33[9;30;43;51;21;3mlol\33[0m')
    for i in range(100):
        print(f'{col(i)}@: ', end=f'{col(0)}{i}\n')
    print(f'{col(0)}')
    print(f'{dicto}\n\n{globals()}')
    fuckoff(1)
    print(f'{dicto}')

    '''
    print(fibonacci.fibo(3))
    print(list(map(type, dir())))
    list1 = [2,3,4]
    list2 = [6,7,8]
    test_str = bway.__name__.split('_')
    dictardo = {'hola': 3, 'aaa': 4, 'lol':5}
    droplist = input(f'Modulos: {dictardo}\ndroplist: (space separated):').split()
    test = {key: val for key, val in dictardo.items() if key not in droplist}
    print(f'{test}\n{dictardo}\n{test_str}\n\n\n{dict(zip(list1, list2))}')
    mod = __import__('fibonacci')
    print(f'{mod.__name__}, {mod.fibo(4)}, {fibonacci.fibo(5)}')
    print(dir())
    '''
    '''
    listarda = [5, 6, 7, 3, 2, 4]
    droplist = list(map(int, input(f'droplist (space separated):').split()))
    print(f'{droplist}')
    lista = [listelem for idx, listelem in enumerate(listarda) if idx not in droplist]
    print(f'lista dropeada: {lista}\nLista Og: {listarda}')
    '''

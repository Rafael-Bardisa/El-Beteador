import time
import cProfile


# TODO import cProfile y hacer benchmark para acelerar el codigo
def benchmark(func):

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
    return 1 if n in [1, 2] else (fib(n-1) + fib(n-2))

if __name__ == '__main__':
    print(fib(20))
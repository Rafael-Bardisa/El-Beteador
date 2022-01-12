def fibo(n):
    return 1 if n in [1, 2] else (fibo(n - 1) + fibo(n - 2))

if __name__ == '__main__':
    print(dir())
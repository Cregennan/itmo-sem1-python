import multiprocessing as mp
import threading as th
from typing import Callable
import time

def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

def loadtest_simple(n):
    for i in range(10):
        fib(n)

def loadtest_by_processes(n):
    processes = [mp.Process(target=fib, args=(n,)) for _ in range(10)]
    for process in processes:
        process.start()
        process.join()

def loadtest_by_threads(n):
    threads = [th.Thread(target=fib, args=(n,)) for _ in range(10)]
    for thread in threads:
        thread.start()
        thread.join()

def measure(f: Callable[[int], None], n) -> time:
    begin = time.time()
    f(n)
    end = time.time()
    return end - begin


def main():
    n = 30

    with open('artifacts/4.1.txt', 'w') as file:
        file.write(f'Синхронно: {measure(loadtest_simple, n):.3f} с\n')
        file.write(f'На процессах: {measure(loadtest_by_processes, n):.3f} с\n')
        file.write(f'На потоках: {measure(loadtest_by_threads, n):.3f} с\n')

if __name__ == '__main__':
    main()
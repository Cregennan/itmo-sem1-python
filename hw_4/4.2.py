import logging
import math
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Union, Type
import logging as log

def integrate_subroutine(call, begin, end, iterations):
    acc = 0
    step = (end - begin) / iterations
    for i in range(iterations):
        acc += call(begin + i * step) * step
    return acc

def integrate(f, a, b, base_executor: Union[Type[ThreadPoolExecutor], Type[ProcessPoolExecutor]], n_jobs=1, n_iter=10000000):
    step = (b - a) / n_jobs
    bounds = [(a + x * step, a + (x + 1) * step) for x in range(n_jobs)]
    executor = base_executor(max_workers=n_jobs)
    tasks = []
    for bound in bounds:
        logging.info(f'Диапазон {bound} в {base_executor.__name__}')
        tasks.append(executor.submit(integrate_subroutine, f, bound[0], bound[1], n_iter // n_jobs))
    return sum([task.result() for task in tasks])


def main():
    log_filename = 'artifacts/4.2.txt'
    stats_filename = 'artifacts/4.2.stats.txt'
    log.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s.%(msecs)03d %(message)s')
    a = 0
    b = math.pi / 2
    f = math.cos
    n_iter = 10000000

    stats = open(stats_filename, 'w')

    for n_jobs in range(1, os.cpu_count() * 2 + 1):
        for base_executor in [ThreadPoolExecutor, ProcessPoolExecutor]:
            begin = time.time()
            result = integrate(f, a, b, base_executor, n_jobs=n_jobs, n_iter=n_iter)
            elapsed = time.time() - begin
            stats.write(f'executor={base_executor.__name__}, n_jobs={n_jobs}, time={elapsed:.4f} s\n')
    stats.close()

if __name__ == '__main__':
    main()
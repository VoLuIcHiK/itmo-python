import math
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

def chunk_integrate(f, a, step, start, end):
    """Вычисляет часть интеграла для заданного диапазона"""
    partial = 0.0
    for i in range(start, end):
        x = a + i * step
        partial += f(x) * step
    return partial

def parallel_integrate(f, a, b, n_jobs=1, executor_type='thread', n_iter=10000000):
    """Параллельное вычисление интеграла"""
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs
    
    ranges = [
        (i * chunk_size, 
         (i + 1) * chunk_size if i != n_jobs - 1 else n_iter)
        for i in range(n_jobs)
    ]
    
    if executor_type == 'thread':
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = [executor.submit(chunk_integrate, f, a, step, start, end) 
                      for start, end in ranges]
            total = sum(f.result() for f in futures)
    else:
        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            futures = [executor.submit(chunk_integrate, f, a, step, start, end) 
                      for start, end in ranges]
            total = sum(f.result() for f in futures)
    
    return total

def benchmark():
    """Сравнение производительности"""
    cpu_count = multiprocessing.cpu_count()
    max_workers = cpu_count * 2
    func = math.cos
    a, b = 0, math.pi / 2
    
    print(f"Тестируем на {cpu_count} ядрах CPU (макс. workers: {max_workers})")
    
    results = []
    
    # Последовательное выполнение для сравнения
    start = time.time()
    result = parallel_integrate(func, a, b, 1, 'thread')
    seq_time = time.time() - start
    results.append(('Single-threaded', 1, seq_time))
    
    for workers in range(1, max_workers + 1):
        # ThreadPool
        start = time.time()
        result = parallel_integrate(func, a, b, workers, 'thread')
        thread_time = time.time() - start
        results.append((f'Thread', workers, thread_time))
        
        # ProcessPool
        start = time.time()
        result = parallel_integrate(func, a, b, workers, 'process')
        process_time = time.time() - start
        results.append((f'Process', workers, process_time))

    # Сохраняем результаты
    with open('hw4/artifacts/integrate_results.csv', 'w') as f:
        f.write("Method\tWorkers\tTime (сек)\n")
        for method, workers, duration in results:
            f.write(f"{method}\t{workers}\t{duration:.6f}\n")
    
    print("\nРезультаты сохранены в benchmark_results.csv")

if __name__ == '__main__':
    benchmark()
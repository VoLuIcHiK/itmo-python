import time
import threading
import multiprocessing

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def synch_execution(n, times=10):
    stime = time.time()
    for _ in range(times):
        fibonacci(n)
    return time.time() - stime

def thread_execution(n, times=10):
    threads = []
    stime = time.time()
    for _ in range(times):
        thread = threading.Thread(target=fibonacci, args=(n,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return time.time() - stime

def multiprocess_execution(n, times=10):
    processes = []
    stime = time.time()
    for _ in range(times):
        process = multiprocessing.Process(target=fibonacci, args=(n,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    return time.time() - stime


if __name__ == "__main__":
    n = 35  
    times = 10
    sync_time = synch_execution(n, times)
    threads_time = thread_execution(n, times)
    multiprocessing_time = multiprocess_execution(n, times)
    results = f"""
    Результаты выполнения функции fibonacci({n}) {times} раз:
    - Синхронное выполнение: {sync_time:.2f} секунд
    - Потоки (threading): {threads_time:.2f} секунд
    - Процессы (multiprocessing): {multiprocessing_time:.2f} секунд
    """
    with open("hw4/artifacts/results.txt", "w+") as file:
        file.write(results)
    
    print(results)
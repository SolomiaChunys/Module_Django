from time import time
import requests
from threading import Thread
from multiprocessing import Process


def power_numb(numb):
    return numb ** 1000000


def sync_power(numbs):
    start = time()

    for numb in numbs:
        power_numb(numb)

    end = time()
    return f'Synchronous request time: {end - start}'


def multithreading_power(numbs):
    start = time()

    threads = []
    for numb in numbs:
        thread = Thread(target=power_numb, args=(numb,))
        thread.start()
        threads.append(thread)

    end = time()

    for thread in threads:
        thread.join()

    return f'Multithreading request time: {end - start}'


def multiprocess_power(numbs):
    start = time()

    processes = []
    for numb in numbs:
        process = Process(target=power_numb, args=(numb,))
        process.start()
        processes.append(process)

    end = time()

    for process in processes:
        process.join()

    return f'Multiprocessing request time: {end - start}'


if __name__ == "__main__":
    urls = [2, 3, 5]

    print(sync_power(urls))
    print(multithreading_power(urls))
    print(multiprocess_power(urls))


# Synchronous request time: 0.1870
# Multithreading request time: 0.1670
# Multiprocessing request time: 0.0169

# Висновок: для такого завдання варто використовувати Багатопроцесорний спосіб,
# адже він найшвидший в паралельному виконанні обчислень.
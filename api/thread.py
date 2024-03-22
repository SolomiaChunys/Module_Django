import threading
from time import time
import requests
from threading import Thread
from multiprocessing import Process


def sync(urls):
    start = time()

    for url in urls:
        requests.get(url)

    end = time()
    return f'Synchronous request time: {end - start}'


def multithreading(urls):
    start = time()

    threads = []
    for url in urls:
        thread = Thread(target=requests.get, args=(url,))
        thread.start()
        threads.append(thread)

    end = time()

    for thread in threads:
        thread.join()

    return f'Multithreading request time: {end - start}'


def multiprocess(urls):
    start = time()

    processes = []
    for url in urls:
        process = Process(target=requests.get, args=(url,))
        process.start()
        processes.append(process)

    end = time()

    for process in processes:
        process.join()

    return f'Multiprocessing request time: {end - start}'


if __name__ == "__main__":
    urls = ['https://google.com', 'https://amazon.com', 'https://microsoft.com']

    print(sync(urls))
    print(multithreading(urls))
    print(multiprocess(urls))


# Synchronous request time: 3.5606
# Multithreading request time: 0.0029
# Multiprocessing request time: 0.0157

# Висновок: Порівняно з Синхронним способом,
# Багатопроцесорний способи є значно швидшими,
# А Багатопоточний виявився ще швидшим.
import aiohttp
import asyncio
from time import time


async def power_numb(numb):
    return numb ** 1000000


async def main(numbs):
    start = time()
    tasks = []

    for numb in numbs:
        task = asyncio.create_task(power_numb(numb))
        tasks.append(task)

    await asyncio.gather(*tasks)

    end = time()
    return f'Async request time: {end - start}'


if __name__ == "__main__":
    numbs = [2, 3, 5]
    print(asyncio.run(main(numbs)))


# Async request time: 0.1999

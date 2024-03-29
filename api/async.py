import aiohttp
import asyncio
from time import time


async def get_page(session, url):
    async with session.get(url) as resp:
        return await resp.text()


async def main(urls):
    start = time()

    async with aiohttp.ClientSession() as session:
        tasks = []

        for url in urls:
            for _ in range(5):
                task = asyncio.create_task(get_page(session, url))
                tasks.append(task)

        await asyncio.gather(*tasks)

    end = time()
    return f'Async request time: {end - start}'


if __name__ == "__main__":
    urls = [
        'https://google.com',
        'https://amazon.com',
        'https://microsoft.com'
    ]
    print(asyncio.run(main(urls)))


# Async request time: 1.9171

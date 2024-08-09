import os
import requests
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import time
import argparse
import aiofiles

def save_image(url):
    try:
        start = time()
        response = requests.get(url)
        response.raise_for_status()
        
        file_name = os.path.basename(url)
        
        with open(file_name, 'wb') as file:
            file.write(response.content)
        
        end = time()
        print(f"скачалось {filename} за {end - start:.2f} секунд")
    except Exception as error:
        print(f"Ошибка")

async def async_save_image(url):
    try:
        start = time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                
                file_name = os.path.basename(url)
                
                async with aiofiles.open(file_name, 'wb') as file:
                    content = await response.read()
                    await file.write(content)
                
                end = time()
                print(f"скачалось {filename} за {end - start:.2f} секунд")
    except Exception as error:
        print(f"Ошибка")

async def async_download_all(urls):
    tasks = [async_save_image(url) for url in urls]
    await asyncio.gather(*tasks)

def threaded_download(urls):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(save_image, urls)

def multiprocess_download(urls):
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(save_image, urls)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачка")
    parser.add_argument('urls', nargs='+', help='Список')
    args = parser.parse_args()
    
    start_time = time()

    asyncio.run(async_download_all(args.urls))

    threaded_download(args.urls)
    multiprocess_download(args.urls)
    
    end_time = time()
    print(f"получилось времени: {end_time - start_time:.2f} секунд")

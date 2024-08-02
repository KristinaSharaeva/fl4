import os
import requests
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import time
import argparse

def download_image(url):
    try:
        start_time = time()
        response = requests.get(url)
        response.raise_for_status()
        
        filename = os.path.basename(url)
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        end_time = time()
        print(f"скачалось нормалек {filename} потрачено {end_time - start_time:.2f} секунд")
    except Exception as e:
        print(f"ошибка тут {url}: {e}")

async def async_download_image(url):
    try:
        start_time = time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                
                filename = os.path.basename(url)
                
                with open(filename, 'wb') as f:
                    content = await response.read()
                    f.write(content)
                
                end_time = time()
                print(f"скачалось {filename} за {end_time - start_time:.2f} секунд")
    except Exception as e:
        print(f"ошибка вылезла тут {url}: {e}")

def main(urls):
    start_time = time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_image, urls)
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(download_image, urls)
    
    asyncio.run(async_download_images(urls))
    
    end_time = time()
    print(f"получилось времени: {end_time - start_time:.2f} секунд")

async def async_download_images(urls):
    tasks = [async_download_image(url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from URLs")
    parser.add_argument('urls', nargs='+', help='List of image URLs')
    args = parser.parse_args()
    
    main(args.urls)

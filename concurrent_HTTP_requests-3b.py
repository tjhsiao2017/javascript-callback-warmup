import asyncio
import httpx
import backoff
import time
from typing import List, Tuple, Union

@backoff.on_exception(backoff.expo, (httpx.TimeoutException, httpx.HTTPStatusError), max_tries=5, max_time=60)

async def http_get(client, url: str, timeout: int = 15) -> Tuple[Union[int, str], str]:
    try:
        response = await client.get(url, timeout=timeout)
        return response.status_code, response.text
    except httpx.TimeoutException:
        return f"TimeoutError: Request to {url} timed out.", ""

async def http_get_parallel(urls: List[str], timeout: int = 10) -> List[Tuple[Union[int, str], str]]:
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = []
            for url in urls:
                task = tg.create_task(http_get(client, url, timeout))
                tasks.append(task)

            responses = []
            for task in tasks:
                try:
                    response = await task
                    responses.append(response)
                except Exception as e:
                    responses.append((f"Error: {str(e)}", ""))

        return responses

async def http_get_serial(urls: List[str], timeout: int = 10) -> List[Tuple[Union[int, str], str]]:
    responses = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            try:
                response = await http_get(client, url, timeout)
                responses.append(response)
            except httpx.TimeoutException:
                responses.append((f"TimeoutError: Request to {url} timed out.", ""))
            except Exception as e:
                responses.append((f"Error: An error occurred while requesting {url}. Error: {str(e)}", ""))
    return responses

async def test_async():
    urls = [
            'https://httpbin.org/delay/1',
            'https://httpbin.org/delay/2',
            'https://httpbin.org/delay/3',
            'https://httpbin.org/delay/4',
            'https://httpbin.org/delay/5',
            'https://httpbin.org/delay/6',      
            'https://httpbin.org/delay/7',
            'https://httpbin.org/delay/8',
            'https://httpbin.org/delay/9',
            'https://httpbin.org/delay/10',
            'https://httpbin.org/delay/1',
            'https://httpbin.org/delay/2',
            'https://httpbin.org/delay/3',
            'https://httpbin.org/delay/4',
            'https://httpbin.org/delay/5',
            'https://httpbin.org/delay/6',
            'https://httpbin.org/delay/7',
            'https://httpbin.org/delay/8',
            'https://httpbin.org/delay/9',
            'https://httpbin.org/delay/10',
            'https://httpbin.org/delay/1',
            'https://httpbin.org/delay/2',
            'https://httpbin.org/delay/3',
            'https://httpbin.org/delay/4',
            'https://httpbin.org/delay/5',
            'https://httpbin.org/delay/6',
            'https://httpbin.org/delay/7',
            'https://httpbin.org/delay/8',
            'https://httpbin.org/delay/9',
            'https://httpbin.org/delay/10',
            'https://httpbin.org/delay/1',
            'https://httpbin.org/delay/2',
            'https://httpbin.org/delay/3',
            'https://httpbin.org/delay/4',
            'https://httpbin.org/delay/5',
            'https://httpbin.org/delay/6',
            'https://httpbin.org/delay/7',
            'https://httpbin.org/delay/8',
            'https://httpbin.org/delay/9',
            'https://httpbin.org/delay/10',
            'https://httpbin.org/delay/1',
            'https://httpbin.org/delay/2',
            'https://httpbin.org/delay/3',
            'https://httpbin.org/delay/4',
            'https://httpbin.org/delay/5',
            'https://httpbin.org/delay/6',
            'https://httpbin.org/delay/7',
            'https://httpbin.org/delay/8',
            'https://httpbin.org/delay/9',
            'https://httpbin.org/delay/10',
            ]

    start_time = time.monotonic()
    print('Trying httpGetParallel...')
    parallel_responses = await http_get_parallel(urls, timeout=10)
    parallel_duration = time.monotonic() - start_time
    print(f"Parallel execution time: {parallel_duration} seconds")
    print("Parallel responses:")
    for response in parallel_responses:
        print(f"Status Code: {response[0]}, Response Text: {response[1]}")

    start_time = time.monotonic()
    print('Trying httpGetSerial...')
    serial_responses = await http_get_serial(urls, timeout=10)
    serial_duration = time.monotonic() - start_time
    print(f"Serial execution time: {serial_duration} seconds")
    print("Serial responses:")
    for response in serial_responses:
        print(f"Status Code: {response[0]}, Response Text: {response[1]}")

if __name__ == '__main__':
    asyncio.run(test_async())
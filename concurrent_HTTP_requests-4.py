import asyncio
import httpx
import backoff
import time
import json
from typing import List, Tuple
from pathlib import Path
from datetime import datetime, timezone

@backoff.on_exception(backoff.expo, (httpx.TimeoutException, httpx.HTTPStatusError), max_tries=5, max_time=60)
    
async def http_get(client, url: str, timeout: int = 15) -> Tuple[int, str, float, str, datetime]:
    try:
        start_time = time.time()
        response = await client.get(url, timeout=timeout)
        end_time = time.time()
        response_time = end_time - start_time
        timestamp = datetime.now(timezone.utc)
        return response.status_code, response.text, response_time, url, timestamp
    except httpx.TimeoutException:
        response_time = timeout
        timestamp = datetime.now(timezone.utc)
        return -1, f"TimeoutError: Request to {url} timed out.", response_time, url, timestamp

# async def http_get_parallel(urls: List[str], timeout: int = 10) -> List[Tuple[int, str, float, str]]:
#     async with httpx.AsyncClient() as client:
#         async with asyncio.TaskGroup() as tg:
#             tasks = []
#             for url in urls:
#                 task = tg.create_task(http_get(client, url, timeout))
#                 tasks.append(task)

#             responses = []
#             for task in tasks:
#                 try:
#                     response = await task
#                     responses.append(response)
#                 except Exception as e:
#                     responses.append((-1, f"Error: {str(e)}", 0.0, ""))

#         return responses
    
async def http_get_parallel(urls: List[str], timeout: int = 10) -> List[Tuple[int, str, float, str]]:
    async with httpx.AsyncClient() as client:
        timeout_groups = [(5, []), (8, []), (12, [])]  # Define timeout groups

        # Distribute URLs among the timeout groups
        for i, url in enumerate(urls):
            group_index = i % len(timeout_groups)
            timeout_groups[group_index][1].append(url)

        results = []

        for timeout, group_urls in timeout_groups:
            async with asyncio.TaskGroup() as tg:
                tasks = []
                for url in group_urls:
                    task = tg.create_task(http_get(client, url, timeout))
                    tasks.append(task)

                for task in tasks:
                    try:
                        response = await task
                        results.append(response)
                    except Exception as e:
                        results.append((-1, f"Error: {str(e)}", 0.0, ""))

        return results


async def http_get_serial(urls: List[str], timeout: int = 10) -> List[Tuple[int, str, float, str]]:
    responses = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            try:
                response = await http_get(client, url, timeout)
                responses.append(response)
            except httpx.TimeoutException:
                response_time = timeout
                responses.append((-1, f"TimeoutError: Request to {url} timed out.", response_time, url))
            except Exception as e:
                responses.append((-1, f"Error: An error occurred while requesting {url}. Error: {str(e)}", 0.0, url))
    return responses

def save_to_json(responses: List[Tuple[int, str, float, str, datetime]], output_path: Path):
    data = []
    for response in responses:
        status_code, response_text, response_time, url, timestamp = response
        data.append({
            "timestamp": timestamp.isoformat(),
            "status_code": status_code,
            "url": url,
            "response_time": round(response_time, 2),
            "response_body": response_text
        })

    try:
        with output_path.open("w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error writing to file {output_path}: {str(e)}")

async def test_async(parallel_output: Path, serial_output: Path, timeout: int):
    start_time = time.monotonic()
    print('Trying httpGetParallel...')
    parallel_responses = await http_get_parallel(urls, timeout=timeout)
    parallel_duration = time.monotonic() - start_time
    print(f"Parallel execution time: {parallel_duration} seconds")
    save_to_json(parallel_responses, parallel_output)

    start_time = time.monotonic()
    print('Trying httpGetSerial...')
    serial_responses = await http_get_serial(urls, timeout=timeout)
    serial_duration = time.monotonic() - start_time
    print(f"Serial execution time: {serial_duration} seconds")
    save_to_json(serial_responses, serial_output)

if __name__ == '__main__':
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

    parallel_output = Path('http_get_parallel.json')
    serial_output = Path('http_get_serial.json')
    timeout = 10

    asyncio.run(test_async(parallel_output, serial_output, timeout))
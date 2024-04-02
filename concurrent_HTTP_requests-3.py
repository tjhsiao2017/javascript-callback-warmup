import asyncio
import aiohttp
import backoff
import time
import httpx

# @backoff.on_exception(backoff.expo,
#                       aiohttp.ClientError,
#                       max_tries=5,
#                       max_time=60)
# async def http_get(session, url, timeout=15):
#     async with session.get(url, timeout=timeout) as response:
#         returnCode = response.status
#         print(f"URL: {url}, Response: {returnCode}")
#         return returnCode

# @backoff.on_exception(backoff.expo,
#                       aiohttp.ClientError,
#                       max_tries=5,
#                       max_time=60)
# async def http_get(session, url, timeout=15):
#     try:
#         async with session.get(url, timeout=timeout) as response:
#             returnCode = response.status
#             print(f"URL: {url}, Response: {returnCode}")
#             return returnCode
#     except asyncio.TimeoutError:
#         return f"TimeoutError: Request to {url} timed out."

#HTTPX
@backoff.on_exception(backoff.expo,
                      (httpx.TimeoutException, httpx.HTTPStatusError),
                       max_tries=5,
                       max_time=60)
async def http_get(client, url, timeout=15):
    try:
        response = await client.get(url, timeout=timeout)
        return response.status_code
    except httpx.TimeoutException:
        return f"TimeoutError: Request to {url} timed out."

#HTTPX
async def http_get_parallel(urls, timeout=10):
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
                    responses.append(f"Error: {str(e)}")

        return responses

#USING TaskGroups
# async def http_get_parallel(urls, timeout=10):
#     async with aiohttp.ClientSession() as session:
#         async with asyncio.TaskGroup() as tg:
#             tasks = []
#             for url in urls:
#                 task = tg.create_task(http_get(session, url, timeout))
#                 tasks.append(task)

#             responses = []
#             for task in tasks:
#                 try:
#                     response = await task
#                     responses.append(response)
#                 except Exception as e:
#                     responses.append(f"Error: {str(e)}")

#         return responses

# async def http_get_parallel(urls, timeout=10):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for url in urls:
#             task = asyncio.create_task(http_get(session, url, timeout))
#             tasks.append(task)

#         responses = []
#         for coro in asyncio.as_completed(tasks):
#             response = await coro
#             responses.append(response)
#         return responses

async def http_get_serial(urls, timeout=10):
    responses = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                response = await http_get(session, url, timeout)
                responses.append(response)
            except asyncio.TimeoutError:
                responses.append(f"TimeoutError: Request to {url} timed out.")
            except Exception as e:
                responses.append(f"Error: An error occurred while requesting {url}. Error: {str(e)}")
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
    await http_get_parallel(urls, timeout=10)
    parallel_duration = time.monotonic() - start_time
    print(f"Parallel execution time: {parallel_duration} seconds")

    start_time = time.monotonic()
    print('Trying httpGetSerial...')
    await http_get_serial(urls, timeout=10)
    serial_duration = time.monotonic() - start_time
    print(f"Serial execution time: {serial_duration} seconds")

if __name__ == '__main__':
    asyncio.run(test_async())
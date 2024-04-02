import asyncio
import aiohttp
import backoff
import time
import multiprocessing

#WORKING
@backoff.on_exception(backoff.expo,
                      aiohttp.ClientError,  # Retry on client errors
                      max_tries=5,          # Maximum number of retries
                      max_time=60)          # Maximum total retry time in seconds
async def http_get(session, url, timeout=15):
    """Make an asynchronous HTTP GET request with timeout and automatic retry."""
    async with session.get(url, timeout=timeout) as response:
        # text = await response.text()
        returnCode = response.status
        print(f"URL: {url}, Response: {returnCode}")
        return returnCode

async def http_get_parallel(urls, timeout=10):
    """Make concurrent asynchronous HTTP GET requests with timeout and exception handling."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(http_get(session, url, timeout))
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return [str(response) if isinstance(response, Exception) else response for response in responses]

#WORKING
async def http_get_serial(urls, timeout=10):
    """Make serial asynchronous HTTP GET requests with timeout and exception handling."""
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

async def run_async_tasks(urls, timeout=10):
    start_time = time.monotonic()
    print('Trying httpGetParallel...')
    await http_get_parallel(urls, timeout=timeout)
    parallel_duration = time.monotonic() - start_time
    print(f"Parallel execution time: {parallel_duration} seconds")

def run_parallel(urls, timeout=10):
    asyncio.run(run_async_tasks(urls, timeout=timeout))

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

    num_processes = multiprocessing.cpu_count()
    chunk_size = len(urls) // num_processes
    print(f"num_processes: {num_processes}, chunk_size: {chunk_size}")
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    processes = []
    for chunk in url_chunks:
        process = multiprocessing.Process(target=run_parallel, args=(chunk, 10))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
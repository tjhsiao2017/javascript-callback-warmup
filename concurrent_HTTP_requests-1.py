import asyncio
import aiohttp
import backoff
import time

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

# Test functions
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
    asyncio.run(test_async(), debug=True)
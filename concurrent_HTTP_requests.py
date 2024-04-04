# import aiohttp
# import asyncio

# # List of URLs to send requests to
# urls = ["http://www.google.com", "http://www.bing.com", "http://www.yahoo.com"]

# async def load_url(session, url):
#     async with session.get(url) as response:
#         return await response.read()

# async def main():
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for url in urls:
#             tasks.append(load_url(session, url))
#         pages = await asyncio.gather(*tasks)

#         for url, page in zip(urls, pages):
#             print('%r page is %d bytes' % (url, len(page)))

# # Python 3.7+
# asyncio.run(main())
# import asyncio
# import aiohttp

# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.json()

# async def main():
#     urls = [
#         'https://jsonplaceholder.typicode.com/posts',
#         'https://jsonplaceholder.typicode.com/users',
#         'https://jsonplaceholder.typicode.com/comments',
#     ]

#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(session, url) for url in urls]
#         responses = await asyncio.gather(*tasks)
#         for response in responses:
#             print(response[0])  # Print the first item from each response

# if __name__ == '__main__':
#     asyncio.run(main())
# import asyncio
# import aiohttp
# import backoff
# import json

# #Define a backoff strategy for retries
# @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=5)
# async def fetch(session, url, timeout=5):
#     async with session.get(url, timeout=timeout) as response:
#         return await response.json()

# async def main():
#     urls = [
#         'https://jsonplaceholder.typicode.com/posts',
#         'https://jsonplaceholder.typicode.com/users',
#         'https://jsonplaceholder.typicode.com/comments',
#     ]

#     results = []

#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(session, url) for url in urls]
#         responses = await asyncio.gather(*tasks)

#         for response in responses:
#             print(response[0])  # Print the first item from each response
#             results.append(response)

#     # Persist the results to a JSON file
#     with open('api_results.json', 'w') as f:
#         json.dump(results, f)

# if __name__ == '__main__':
#     asyncio.run(main())
import asyncio
import aiohttp
import backoff
import time
import api
import httpx

# async def http_get(session, url, timeout=5):
#     """Make an asynchronous HTTP GET request with timeout."""
#     async with session.get(url, timeout=timeout) as response:
#         return await response.text()

# async def http_get_parallel(urls, timeout=10):
#     """Make concurrent asynchronous HTTP GET requests with timeout."""
#     async with aiohttp.ClientSession() as session:
#         tasks = [http_get(session, url, timeout) for url in urls]
#         return await asyncio.gather(*tasks)

#WORKING
@backoff.on_exception(backoff.expo,
                      aiohttp.ClientError,  # Retry on client errors
                      max_tries=5,          # Maximum number of retries
                      max_time=60)          # Maximum total retry time in seconds
async def http_get(session, url, timeout=15):
    """Make an asynchronous HTTP GET request with timeout and automatic retry."""
    async with session.get(url, timeout=timeout) as response:
        return await response.text()

#WORKING
# @backoff.on_exception(backoff.expo,
#                       (httpx.HTTPError, asyncio.TimeoutError),
#                       max_tries=5,
#                       max_time=60)

# async def http_get(url, timeout=10):
#     """Make an asynchronous HTTP GET request using httpx."""
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, timeout=timeout)
#             return response.text
#         except httpx.RequestError as e:
#             return f"RequestError: {str(e)}"
#         except httpx.HTTPStatusError as e:
#             return f"HTTPStatusError: {str(e)}"

#WORKING
# async def http_get_parallel(urls, timeout=10):
#     """Make concurrent asynchronous HTTP GET requests using httpx."""
#     async with httpx.AsyncClient() as client:
#         tasks = [http_get(url, timeout) for url in urls]
#         responses = await asyncio.gather(*tasks, return_exceptions=True)
#         return responses

# async def http_get_serial(urls, timeout=10):
#     """Make serial asynchronous HTTP GET requests using httpx."""
#     responses = []
#     for url in urls:
#         try:
#             print(f"Requesting {url}")
#             response = await http_get(url, timeout)
#             responses.append(response)
#             print(f"Received response from {url}")
#         except Exception as e:
#             print(f"Error requesting {url}: {e}")
#             responses.append(f"Error: {str(e)}")
#     return responses

# async def http_get(url, timeout=10):
#     """Make an asynchronous HTTP GET request with timeout and automatic retry."""
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, timeout=timeout) as response:
#             return await response.text()


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
# async def http_get_parallel(urls, timeout=10):
#     """Make concurrent asynchronous HTTP GET requests using as_completed."""
#     async with aiohttp.ClientSession() as session:
#         tasks = [asyncio.create_task(http_get(session, url, timeout)) for url in urls]
#         responses = []

#         for completed_task in asyncio.as_completed(tasks):
#             try:
#                 response = await completed_task
#                 responses.append(response)
#             except asyncio.TimeoutError:
#                 responses.append("TimeoutError: Request timed out.")
#             except Exception as e:
#                 responses.append(f"Error: {str(e)}")

#     return responses

# async def http_get_parallel(urls, timeout=10):
#     """Make concurrent asynchronous HTTP GET requests using an async generator."""
#     async with aiohttp.ClientSession() as session:
#         async def response_generator():
#             for url in urls:
#                 yield asyncio.create_task(http_get(session, url, timeout))

#         responses = []
#         async for response in response_generator():
#             responses.append(await response)
#         return responses

#WORKING
# async def http_get_parallel(urls, timeout=10):
#     """Make concurrent asynchronous HTTP GET requests using task groups."""
#     async with aiohttp.ClientSession() as session:
#         async with asyncio.TaskGroup() as tg:  # Create a task group
#             for url in urls:
#                 tg.create_task(http_get(session, url, timeout))  # Add tasks to the group

#         # The tasks are automatically awaited when exiting the 'async with' block

#     # Collect results after the 'async with' block to ensure all tasks are completed
#     responses = [task.result() for task in tg._tasks]  # Use tg._tasks to access the tasks

#     return responses

# async def http_get_serial(urls, timeout=10):
#     """Make serial asynchronous HTTP GET requests with timeout."""
#     responses = []
#     async with aiohttp.ClientSession() as session:
#         for url in urls:
#             response = await http_get(session, url, timeout)
#             responses.append(response)
#     return responses

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
        # JSON Placeholder (Fake Online REST API):
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/users/1',
        'https://jsonplaceholder.typicode.com/todos/1',
        # ReqRes (A hosted REST API for testing):

        'https://reqres.in/api/users/2',
        'https://reqres.in/api/users?page=2',
        'https://reqres.in/api/unknown/2',

        # Dog API (Random dog images):

        'https://dog.ceo/api/breeds/image/random',
        'https://dog.ceo/api/breeds/list/all',
        'https://dog.ceo/api/breed/hound/images',

        # Cat Facts API:

        'https://catfact.ninja/fact',
        'https://catfact.ninja/breeds',

        # Public APIs for Testing:

        'https://api.publicapis.org/entries',
        'https://api.publicapis.org/random',

        # The Rick and Morty API (Information about the show):

        'https://rickandmortyapi.com/api/character/1',
        'https://rickandmortyapi.com/api/location/1',
        'https://rickandmortyapi.com/api/episode/1',

        # OpenWeatherMap API (Weather data):

        # https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY
        # Replace YOUR_API_KEY with your actual API key from OpenWeatherMap.
        # GitHub API (GitHub user information):

        # https://api.github.com/users/octocat
        # https://api.github.com/repos/octocat/Hello-World
        #
        'https://example.com',
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
        'https://httpbin.org/delay/11',
        'https://httpbin.org/delay/12',
        'https://httpbin.org/delay/13',
        'https://httpbin.org/delay/14',
        'https://httpbin.org/delay/15',
        'https://httpbin.org/delay/16',
        'https://httpbin.org/delay/17',
        'https://httpbin.org/delay/18',
        'https://httpbin.org/delay/19',
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

# if __name__ == '__main__':
#     asyncio.run(test_async())

if __name__ == '__main__':
    asyncio.run(test_async(), debug=True)
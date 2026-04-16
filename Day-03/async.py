import asyncio       
import httpx        
import time

async def fetch_post(client, url):
    response = await client.get(url)
    data = response.json()
    return data

async def main():
    start = time.time()
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            fetch_post(client, "https://jsonplaceholder.typicode.com/posts/1"),
            fetch_post(client, "https://jsonplaceholder.typicode.com/posts/2"),
            fetch_post(client, "https://jsonplaceholder.typicode.com/posts/3"),
        )
    print(f"Time: {time.time() - start:.2f}s")
    return results

asyncio.run(main())
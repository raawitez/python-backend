import httpx


urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
]

for url in urls:
    response = httpx.get(url)
    data = response.json()
    print(f"Post {data['id']}: {data['title'][:40]}")
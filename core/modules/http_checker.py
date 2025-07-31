import aiohttp
import asyncio

async def fetch_status(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as resp:
                print(f"{url} - Status: {resp.status}")
        except Exception as e:
            print(f"{url} - Error: {str(e)}")

if __name__ == "__main__":
    url = input("Enter URL: ")
    asyncio.run(fetch_status(url))

import aiohttp

url = "https://nominatim.openstreetmap.org/search?format=json&q="


async def check(name: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}{name}") as response:
            ans = await response.json()
            if len(ans) > 0:
                return True
    return False
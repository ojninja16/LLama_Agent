import httpx
import cachetools
from config import CRYPTO_API_URL, CACHE_TTL

cache = cachetools.TTLCache(maxsize=100, ttl=300)
class CryptoService:
        async def get_crypto_price(self,symbol: str) -> float:
            if "price" in cache:
                return cache["price"]
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{CRYPTO_API_URL}/{symbol}")
                    response.raise_for_status()
                    res_json=response.json()
                    price = response.json().get("data", {}).get("priceUsd", "N/A")
                    cache[symbol] = price
                    return float(price)
            except httpx.RequestError:
                    return "Error fetching cryptocurrency prices"

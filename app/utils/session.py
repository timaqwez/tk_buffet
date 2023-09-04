from httpx import AsyncClient, Client

from config import API_URL


class Config:
    API_URL: str

class Session:
    product_extended_info: list[dict]
    categories: list[dict]
    current_products: list[dict]
    favorite_ids: list[int]
    search_queries: list[str]
    config: Config

    def __init__(self):
        with Client(base_url=API_URL) as client:
            response = client.get('all')
            self.products_extended_info = response.json()['products_extended']
            self.categories = [category for category in response.json()['categories']]
            self.favorite_ids = []
            self.current_products = self.products_extended_info
            self.search_queries = []

    async def update_info(self):
        async with AsyncClient(base_url=API_URL) as client:
            response = await client.get('all')
            self.products_extended_info = response.json()['products_extended']
            self.categories = [category for category in response.json()['categories']]

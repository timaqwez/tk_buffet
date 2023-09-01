from httpx import AsyncClient, Client


class Session:
    product_extended_info: list[dict]
    categories: list[dict]
    current_products: list[dict]
    favorite_ids: list[int]
    search_queries: list[str]

    def __init__(self):
        with Client(base_url='http://127.0.0.1:8000/') as client:
            response = client.get('all')
            self.products_extended_info = response.json()['products_extended']
            self.categories = [category for category in response.json()['categories']]
            self.favorite_ids = []
            self.current_products = self.products_extended_info
            self.search_queries = []

    async def update_info(self):
        async with AsyncClient(base_url='http://127.0.0.1:8000/') as client:
            response = await client.get('all')
            self.products_extended_info = response.json()['products_extended']
            self.categories = [category for category in response.json()['categories']]

    async def save_favorite_ids(self):
        pass
        # try:
        #     favorite_ids = await self.app.page.client_storage.get_async('favorite_ids')
        #     if self.favorite_ids == favorite_ids:
        #         return
        #     else:
        #         await self.app.page.client_storage.set_async('favorite_ids', self.favorite_ids)
        # except NotImplementedError:
        #     self.favorite_ids = []
        #     await self.app.page.client_storage.set_async('favorite_ids', self.favorite_ids)

    async def load_favorite_ids(self):
        pass
        # try:
        #     favorite_ids = await self.app.page.client_storage.get_async('favorite_ids')
        #     if self.favorite_ids == favorite_ids:
        #         return
        #     else:
        #         await self.app.page.client_storage.get_async('favorite_ids')
        # except NotImplementedError:
        #     self.favorite_ids = []
        #     await self.app.page.client_storage.set_async('favorite_ids', self.favorite_ids)

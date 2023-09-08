from asyncio import sleep

import flet
from flet_core import BottomSheet, Checkbox, Column, Container, Row, Text, TextField, TextThemeStyle, alignment, \
    border_radius, \
    margin, padding, Image, Stack
from flet_core import ListView, ResponsiveRow
from httpx import AsyncClient

from app.controls import ProductCard, View
from app.controls.category_menu import CategoryMenu
from app.views import ProductView
from app.views.search import SearchView
# from config import API_URL
from config import API_URL


class MainView(View):
    route = '/'
    products: ListView
    bottom_sheet: BottomSheet
    is_header_extended: bool = True
    is_header_activated: bool = True
    is_navbar: bool = True
    header_text: str = 'Меню ТК ГрГУ'

    products_current: list[int]

    def __init__(self, **kwargs):
        super().__init__(
            on_search_click=self.open_search_view,
            on_menu_click=self.open_bottom_sheet,
            on_navbar_menu_click=self.on_navbar_menu_click,
            on_navbar_favorite_click=self.on_navbar_favorite_click,
            **kwargs
        )

    async def open_bottom_sheet(self, e):
        self.bottom_sheet.open = True
        await self.bottom_sheet.update_async()

    async def open_product_view(self, e):
        await self.app.view_change(
            view=ProductView(
                product_id=e.control.product_id,
                update_products=self.update_products
            )
        )

    async def open_search_view(self, e):
        await self.app.view_change(
            view=SearchView(
                main_view=self,
                on_search_submit=self.on_search_submit
            ),
        )

    async def reset_category(self, e):
        self.products.controls[0] = CategoryMenu(
            app=self.app,
            categories=self.app.session.categories,
            is_active=False,
            on_category_button_click=self.select_category,
            on_close_button_click=self.reset_category,
        )
        self.app.session.current_products = self.app.session.products_extended_info
        await self.update_products(e)
        await self.update_async()

    async def select_category(self, e):
        if e.control.is_active:
            await self.reset_category(e)
            await self.update_products(e)
            return
        self.products.controls[0] = CategoryMenu(
            app=self.app,
            categories=self.app.session.categories,
            is_active=True,
            active_id=e.control.category_id,
            on_category_button_click=self.select_category,
            on_close_button_click=self.reset_category,
        )
        await self.loading()
        async with AsyncClient(base_url=API_URL) as client:
            response = await client.get(f'products/{e.control.category_id}')
            category_products = response.json()['values']
        self.app.session.current_products = [product for product in category_products]
        await self.update_products(e)

    async def update_products(self, e):
        self.products.controls[1] = ResponsiveRow(
            controls=[
                ProductCard(
                    app=self.app,
                    product=product,
                    on_click=self.open_product_view,
                    on_favorite_button_click=self.favorite_button_click,
                    is_favorite=product['id'] in self.app.session.favorite_ids
                ) for product in self.app.session.current_products
            ],
            columns=3,
        )
        await self.update_async()

    async def on_navbar_menu_click(self, e):
        self.products.controls[0] = CategoryMenu(
            app=self.app,
            is_active=False,
            categories=self.app.session.categories,
            on_category_button_click=self.select_category,
            on_close_button_click=self.reset_category,
        )
        self.navbar.menu_tab.content.controls[0].selected = True
        self.navbar.favorite_tab.content.controls[0].selected = False
        self.navbar.menu_tab.content.controls[1].color = self.app.theme.primary_color
        self.navbar.favorite_tab.content.controls[1].color = self.app.theme.secondary_color_dark
        self.app.session.current_products = self.app.session.products_extended_info
        await self.update_products(e)

    async def on_navbar_favorite_click(self, e):
        favorite_ids = self.app.session.favorite_ids
        self.navbar.menu_tab.content.controls[0].selected = False
        self.navbar.favorite_tab.content.controls[0].selected = True
        self.navbar.menu_tab.content.controls[1].color = self.app.theme.secondary_color_dark
        self.navbar.favorite_tab.content.controls[1].color = self.app.theme.primary_color
        if not favorite_ids:
            self.products.controls[0] = Container(height=0)
            self.products.controls[1] = Container(
                content=Text(
                    value='У вас нет избранного',
                    style=TextThemeStyle.BODY_LARGE,
                    color=self.app.theme.secondary_color_dark
                ),
                alignment=alignment.center
            )
            await self.update_async()
            return
        self.products.controls[0] = Container(height=0)
        self.app.session.current_products = [
            product for product in self.app.session.products_extended_info if product['id'] in favorite_ids
        ]
        await self.update_products(e)

    async def zhuravskaya_mode_change(self, e):
        self.app.theme = await self.app.theme.zhuravskaya_mode_switch(e)
        await self.bottom_sheet.update_async()
        await self.restart()
        await self.app.page.update_async()

    async def dark_mode_change(self, e):
        self.app.theme = await self.app.theme.dark_mode_switch(e)
        self.bottom_sheet.open = False
        await self.restart()
        await self.app.page.update_async()

    async def on_search_submit(self, e):
        self.products.controls[0] = Container(
            height=0
        )
        query = e.control.value if type(e.control) == TextField else e.control.data
        await self.app.view_change(
            go_back=True,
        )
        products = self.app.session.products_extended_info
        self.app.session.current_products = [
            product for product in products if query.lower() in product['name'].lower()
        ]
        await self.update_products(e)
        if query not in self.app.session.search_queries:
            self.app.session.search_queries.append(query)
        if len(self.app.session.search_queries) > 10:
            queries = self.app.session.search_queries.copy()
            queries.pop(0)
            self.app.session.search_queries = queries
        if len(self.products.controls[1].controls) == 0:
            self.products.controls[1].controls.insert(
                0,
                Container(
                    content=Text(
                        value='Ничего не найдено',
                        style=TextThemeStyle.BODY_LARGE,
                        color=self.app.theme.secondary_color_dark,
                    ),
                    margin=margin.only(
                        left=20,
                        right=20,
                    )
                )
            )
        self.products.controls[1].controls.insert(
            0,
            Container(
                content=Text(
                    value='Результаты по запросу ' + f'"{query}":',
                    style=TextThemeStyle.BODY_LARGE,
                    color=self.app.theme.secondary_color_dark,
                ),
                margin=margin.only(
                    left=20,
                    right=20,
                )
            )
        )
        await self.save_search_queries()
        await self.update_async()

    async def loading(self):
        pizza = Container(
            content=Image(
                src=r'assets/icons/pizza_no_piece.svg',
                color=self.app.theme.primary_color,
                animate_rotation=300,
                height=200,
            ),
        )
        pizza_piece = Container(
            content=Image(
                src=r'assets/icons/pizza_piece.svg',
                color=self.app.theme.primary_color,
                height=200,
            ),
            animate_opacity=600,
            animate_scale=800,
            opacity=1,
            scale=1
        )
        self.products.controls[1] = Container(
            content=Stack(
                controls=[
                    pizza,
                    pizza_piece
                ],
            ),
            alignment=alignment.center
        )
        await self.products.update_async()
        pizza_piece.opacity = 1 if pizza_piece.opacity == 0.5 else 0.5
        pizza_piece.scale = 1 if pizza_piece.scale == 0.7 else 0.7
        await self.products.update_async()

    async def build(self):
        await self.load_search_queries()
        await self.load_favorite_ids()
        self.products = ListView(
            controls=[
                CategoryMenu(app=self.app,
                             is_active=False,
                             categories=self.app.session.categories,
                             on_category_button_click=self.select_category,
                             on_close_button_click=self.reset_category,
                             ),
                ResponsiveRow(
                    controls=[
                        ProductCard(
                            app=self.app,
                            product=product,
                            on_click=self.open_product_view,
                            on_favorite_button_click=self.favorite_button_click,
                            is_favorite=product['id'] in self.app.session.favorite_ids
                        ) for product in self.app.session.products_extended_info
                    ],
                    columns=3,
                ),
            ],
            expand=True,
            padding=padding.only(
                top=20,
            )
        )

        self.bottom_sheet = BottomSheet(
            Container(
                Column(
                    [
                        Container(
                            content=Row(
                                controls=[
                                    Text(
                                        value='Режим Журавской',
                                        style=TextThemeStyle.BODY_LARGE,
                                        color=self.app.theme.primary_color
                                    ),
                                    Checkbox(
                                        value=self.app.theme.is_zhur_mode,
                                        on_change=self.zhuravskaya_mode_change,
                                    )
                                ]
                            ),
                            alignment=alignment.center
                        ),
                        Container(
                            content=Row(
                                controls=[
                                    Text(
                                        value='Темная Тема',
                                        style=TextThemeStyle.BODY_LARGE,
                                        color=self.app.theme.primary_color
                                    ),
                                    Checkbox(
                                        value=self.app.theme.is_dark_mode,
                                        on_change=self.dark_mode_change,
                                    )
                                ]
                            ),
                            alignment=alignment.center
                        ),
                    ],
                    tight=True,
                ),
                padding=30,
                bgcolor=self.app.theme.bg_color,
                border_radius=border_radius.only(
                    top_left=15,
                    top_right=15
                ),
            ),
        )
        self.app.page.overlay.append(self.bottom_sheet)
        self.controls = [
            self.products,
        ]
        await self.create()


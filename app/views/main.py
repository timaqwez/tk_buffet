from flet_core import BottomSheet, Column, Container, Text, TextField, TextThemeStyle, alignment, border_radius, margin
from flet_core import ListView, ResponsiveRow
from httpx import AsyncClient

from app.controls import ProductCard, View
from app.controls.category_menu import CategoryMenu
from app.controls.menu_item import MenuItem
from app.views import ProductView
from app.views.search import SearchView


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
        self.bottom_sheet.open = not self.bottom_sheet.open
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
        async with AsyncClient(base_url='http://127.0.0.1:8000/') as client:
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
        await self.app.session.load_favorite_ids()

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
        await self.app.session.load_favorite_ids()
        favorite_ids = self.app.session.favorite_ids
        self.navbar.menu_tab.content.controls[0].selected = False
        self.navbar.favorite_tab.content.controls[0].selected = True
        self.navbar.menu_tab.content.controls[1].color = self.app.theme.secondary_color_dark
        self.navbar.favorite_tab.content.controls[1].color = self.app.theme.primary_color
        if not favorite_ids:
            self.products.controls[0] = Container(height=40)
            self.products.controls[1] = Container(
                content=Text(
                    value='У вас нет избранного',
                    style=TextThemeStyle.BODY_MEDIUM,
                    color=self.app.theme.secondary_color_dark
                ),
                alignment=alignment.center
            )
            await self.update_async()
            return
        self.products.controls[0] = Container(height=40)
        self.app.session.current_products = [
            product for product in self.app.session.products_extended_info if product['id'] in favorite_ids
        ]
        await self.update_products(e)

    async def zhuravskaya_mode_change(self, e):
        if e.control.value is True:
            self.app.theme.text_style_small_regular.font_family = 'Times New Roman'
            self.app.theme.text_style_medium_regular.font_family = 'Times New Roman'
            self.app.theme.text_style_large_regular.font_family = 'Times New Roman'
            self.app.theme.text_style_semi_bold.font_family = 'Times New Roman'
        else:
            self.app.theme.text_style_small_regular.font_family = 'Regular'
            self.app.theme.text_style_medium_regular.font_family = 'Regular'
            self.app.theme.text_style_large_regular.font_family = 'Regular'
            self.app.theme.text_style_semi_bold.font_family = 'SemiBold'
        await self.app.page.update_async()

    async def dark_mode_change(self, e):
        self.app.theme = await self.app.theme.switch_theme(self.app.theme)
        await self.restart()
        await self.app.page.update_async()
        print('changed dark mode')

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
                        style=TextThemeStyle.BODY_MEDIUM,
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
                    style=TextThemeStyle.BODY_MEDIUM,
                    color=self.app.theme.secondary_color_dark,
                ),
                margin=margin.only(
                    left=20,
                    right=20,
                )
            )
        )
        await self.update_async()

    async def build(self):
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
        )

        self.bottom_sheet = BottomSheet(
            Container(
                Column(
                    [
                        MenuItem(self.app, 'Режим Журавской', self.zhuravskaya_mode_change),
                        MenuItem(self.app, 'Темная тема', self.dark_mode_change)
                    ],
                    tight=True,
                ),
                padding=30,
                bgcolor=self.app.theme.bg_color,
                border_radius=border_radius.only(
                    top_left=15,
                    top_right=15
                )
            ),
            open=False
        )
        self.controls = [
            self.products,
            self.bottom_sheet,
        ]
        await self.create()

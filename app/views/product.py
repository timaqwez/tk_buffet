from flet_core import BorderSide, Column, Container, CrossAxisAlignment, IconButton, Image, ImageFit, ImageRepeat, \
    ListView, MainAxisAlignment, Row, Stack, Text, TextThemeStyle, alignment, border, icons, margin, padding

from app.controls import InfoText
from app.controls import View
from app.controls.available_container import AvailableContainer
from config import API_URL


class ProductView(View):
    route = '/product'
    is_header_extended: bool = False
    is_header_activated: bool = True
    is_navbar: bool = False
    header_text: str = 'Меню ТК ГрГУ'
    product_id: int
    product: dict
    favorite_ids: list

    async def build(self):
        self.favorite_ids = self.params.get('favorite_ids')
        self.product_id = self.params.get('product_id')
        self.product = self.client.page.session.get('products_extended_info')[self.product_id-1]
        name = self.product['name']
        price = self.product['price']
        description = self.product['description']
        weight = self.product['weight']
        composition = self.product['composition']
        expiration_date = self.product['expiration_date']
        manufacturer = self.product['manufacturer']
        kcal = self.product['kcal']
        carb = self.product['carb']
        image_name = self.product['image_name']
        available_count = self.product['count']
        self.controls = [
            ListView(
                controls=[
                    Container(
                        content=Row(
                            controls=[
                                Container(
                                    content=Stack(
                                        controls=[
                                            Container(
                                                content=Image(
                                                    src=API_URL+f'images/{image_name}',
                                                    fit=ImageFit.FIT_WIDTH,
                                                    repeat=ImageRepeat.NO_REPEAT,
                                                    border_radius=10,
                                                    height=300,
                                                    width=500
                                                ),
                                                alignment=alignment.center,
                                                margin=margin.only(
                                                    left=20,
                                                    right=20,
                                                ),
                                            ),
                                            AvailableContainer(client=self.client, count=available_count),
                                            Container(
                                                content=IconButton(
                                                    icon=icons.FAVORITE_OUTLINE_SHARP,
                                                    selected_icon=icons.FAVORITE_OUTLINED,
                                                    selected=self.product_id in self.client.page.session.get('favorite_ids'),
                                                    icon_color=self.client.theme.secondary_color_dark,
                                                    selected_icon_color=self.client.theme.secondary_color_dark,
                                                    on_click=self.favorite_button_click,
                                                    icon_size=40,
                                                    data=self.product_id
                                                ),
                                                alignment=alignment.top_right,

                                            ),
                                        ],
                                    ),
                                    bgcolor=self.client.theme.secondary_color,
                                    border_radius=10,
                                    margin=margin.only(
                                        left=20,
                                        right=20,
                                        bottom=0
                                    ),
                                    padding=0,
                                ),
                                Stack(
                                    controls=[
                                        Column(
                                            controls=[
                                                Container(
                                                    content=Text(
                                                        value=name,
                                                        no_wrap=False,
                                                        style=TextThemeStyle.BODY_LARGE,
                                                        color=self.client.theme.primary_color
                                                    ),
                                                    alignment=alignment.bottom_left,
                                                    height=40,
                                                    margin=margin.only(
                                                        left=17,
                                                        right=20,
                                                    ),
                                                ),
                                                Container(
                                                    content=Text(
                                                        value=str(price) + ' BYN',
                                                        style=TextThemeStyle.BODY_MEDIUM,
                                                        color=self.client.theme.primary_color
                                                    ),
                                                    alignment=alignment.top_left,
                                                    border=border.only(
                                                        bottom=BorderSide(
                                                            width=1,
                                                            color=self.client.theme.secondary_color
                                                        )
                                                    ),
                                                    margin=margin.only(
                                                        left=20,
                                                        right=20,
                                                    ),
                                                    padding=padding.only(
                                                        bottom=8
                                                    ),
                                                )
                                            ],
                                            spacing=0,
                                        ),
                                        Container(
                                            content=Text(
                                                value=str(weight) + ' г',
                                                no_wrap=False,
                                                style=TextThemeStyle.BODY_LARGE,
                                                color=self.client.theme.secondary_color
                                            ),
                                            alignment=alignment.center_right,
                                            height=40,
                                            margin=margin.only(
                                                left=17,
                                                right=20,
                                            ),
                                        ),
                                    ]
                                ),
                                InfoText(self.client, 'Описание', description),
                                Column(
                                    controls=[
                                        Container(
                                            content=Text(
                                                value='В 100 граммах',
                                                no_wrap=False,
                                                style=TextThemeStyle.BODY_LARGE,
                                                color=self.client.theme.secondary_color,
                                            ),
                                            alignment=alignment.bottom_left,
                                            margin=margin.only(
                                                left=20,
                                                right=20,
                                            ),
                                        ),
                                        Container(
                                            content=Row(
                                                controls=[
                                                    Column(
                                                        controls=[
                                                            Text(
                                                                value=kcal,
                                                                style=TextThemeStyle.BODY_LARGE,
                                                                no_wrap=False,
                                                                color=self.client.theme.primary_color
                                                            ),
                                                            Text(
                                                                value='ккал',
                                                                style=TextThemeStyle.BODY_MEDIUM,
                                                                no_wrap=False,
                                                                color=self.client.theme.primary_color,
                                                            ),
                                                        ],
                                                        spacing=0
                                                    ),
                                                    Column(
                                                        controls=[
                                                            Text(
                                                                value=str(carb)+' г',
                                                                style=TextThemeStyle.BODY_LARGE,
                                                                no_wrap=False,
                                                                color=self.client.theme.primary_color
                                                            ),
                                                            Text(
                                                                value='углеводы',
                                                                style=TextThemeStyle.BODY_MEDIUM,
                                                                no_wrap=False,
                                                                color=self.client.theme.primary_color,
                                                            ),
                                                        ],
                                                        spacing=0

                                                    ),
                                                ],
                                                spacing=30
                                            ),
                                            alignment=alignment.top_left,
                                            border=border.only(
                                                bottom=BorderSide(
                                                    width=1,
                                                    color=self.client.theme.secondary_color
                                                )
                                            ),
                                            padding=padding.only(
                                                bottom=10
                                            ),
                                            margin=margin.only(
                                                left=20,
                                                right=20,
                                            ),
                                        )
                                    ],
                                    spacing=0,
                                ),
                                InfoText(self.client, 'Состав', composition),
                                InfoText(self.client, 'Срок годности', str(expiration_date) + ' ч'),
                                InfoText(self.client, 'Производитель', manufacturer),

                            ],
                            vertical_alignment=CrossAxisAlignment.START,
                            alignment=MainAxisAlignment.CENTER,
                            spacing=0,
                            wrap=True
                        ),
                    )
                ],
                expand=True,
                padding=padding.only(
                    top=20
                )
            )
        ]
        await self.create()

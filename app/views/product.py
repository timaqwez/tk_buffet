from flet_core import BorderSide, Column, Container, CrossAxisAlignment, IconButton, Image, ImageFit, ImageRepeat, \
    ListView, MainAxisAlignment, Row, Stack, Text, alignment, border, icons, margin, padding

from app.controls import InfoText
from app.controls import View
from app.controls.available_container import AvailableContainer


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
        self.product = self.app.session.products_extended_info[self.product_id-1]
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
                                                    src=f'assets/images/{image_name}',
                                                    fit=ImageFit.FIT_WIDTH,
                                                    repeat=ImageRepeat.NO_REPEAT,
                                                    border_radius=10,
                                                    width=500,
                                                    height=350
                                                ),
                                                alignment=alignment.center,
                                                margin=margin.only(
                                                    left=20,
                                                    right=20,
                                                ),
                                            ),
                                            AvailableContainer(app=self.app, count=available_count),
                                            Container(
                                                content=IconButton(
                                                    icon=icons.FAVORITE_OUTLINE_SHARP,
                                                    selected_icon=icons.FAVORITE_OUTLINED,
                                                    selected=self.product_id in self.app.session.favorite_ids,
                                                    icon_color=self.app.theme.secondary_color_dark,
                                                    selected_icon_color=self.app.theme.secondary_color_dark,
                                                    on_click=self.favorite_button_click,
                                                    icon_size=40,
                                                    data=self.product_id
                                                ),
                                                alignment=alignment.top_right,

                                            ),
                                        ],
                                    ),
                                    bgcolor=self.app.theme.secondary_color,
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
                                                        size=30,
                                                        color=self.app.theme.primary_color
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
                                                        size=25,
                                                        color=self.app.theme.primary_color
                                                    ),
                                                    alignment=alignment.top_left,
                                                    border=border.only(
                                                        bottom=BorderSide(
                                                            width=1,
                                                            color=self.app.theme.secondary_color
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
                                                size=30,
                                                color=self.app.theme.secondary_color
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
                                InfoText(self.app, 'Описание', description),
                                Column(
                                    controls=[
                                        Container(
                                            content=Text(
                                                value='В 100 граммах',
                                                no_wrap=False,
                                                size=30,
                                                color=self.app.theme.secondary_color,
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
                                                                size=22,
                                                                no_wrap=False,
                                                                color=self.app.theme.primary_color
                                                            ),
                                                            Text(
                                                                value='ккал',
                                                                size=18,
                                                                no_wrap=False,
                                                                color=self.app.theme.primary_color,
                                                            ),
                                                        ],
                                                        spacing=0
                                                    ),
                                                    Column(
                                                        controls=[
                                                            Text(
                                                                value=str(carb)+' г',
                                                                size=22,
                                                                no_wrap=False,
                                                                color=self.app.theme.primary_color
                                                            ),
                                                            Text(
                                                                value='углеводы',
                                                                size=18,
                                                                no_wrap=False,
                                                                color=self.app.theme.primary_color,
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
                                                    color=self.app.theme.secondary_color
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
                                InfoText(self.app, 'Состав', composition),
                                InfoText(self.app, 'Срок годности', str(expiration_date) + ' ч'),
                                InfoText(self.app, 'Производитель', manufacturer),

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

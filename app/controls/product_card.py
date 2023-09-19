from flet_core import Column, Container, CrossAxisAlignment, IconButton, Image, ImageFit, ImageRepeat, \
    MainAxisAlignment, Stack, Text, TextThemeStyle, alignment, icons, margin

from config import API_URL
from flet_manager import App

from app.controls.available_container import AvailableContainer
from flet_manager.controls import Client


class ProductCard(Container):
    client: Client
    product_id: int
    is_favorite: bool
    product: dict

    def __init__(self, client: Client, product: dict, is_favorite: bool, on_click, on_favorite_button_click, **kwargs):
        super().__init__(
            **kwargs,
        )
        self.client = client
        self.on_click = on_click
        self.is_favorite = is_favorite
        self.product = product
        self.on_favorite_button_click = on_favorite_button_click
        self.create()

    def create(self):
        self.product_id = self.product['id']
        name = self.product['name']
        price = self.product['price']
        count = self.product['count']
        image_name = self.product['image_name']
        card = Column(
            controls=[
                Container(
                    content=Stack(
                        controls=[
                            Container(
                                content=Image(
                                    src=API_URL + f'images/{image_name}',
                                    fit=ImageFit.FIT_WIDTH,
                                    repeat=ImageRepeat.NO_REPEAT,
                                    border_radius=10,
                                    aspect_ratio=2.2
                                ),
                                alignment=alignment.center,
                            ),
                            AvailableContainer(client=self.client, count=count),
                            Container(
                                content=IconButton(
                                    icon=icons.FAVORITE_OUTLINE_SHARP,
                                    selected_icon=icons.FAVORITE_OUTLINED,
                                    selected=self.is_favorite,
                                    icon_color=self.client.theme.secondary_color_dark,
                                    selected_icon_color=self.client.theme.secondary_color_dark,
                                    on_click=self.on_favorite_button_click,
                                    icon_size=40,
                                    data=self.product_id
                                ),
                                alignment=alignment.top_right,

                            ),
                        ],
                    ),
                    bgcolor=self.client.theme.secondary_color,
                    border_radius=10
                ),
                Stack(
                    controls=[
                        Container(
                            content=Text(
                                value=name,
                                no_wrap=True,
                                color=self.client.theme.primary_color,
                                style=TextThemeStyle.BODY_LARGE,
                            ),
                            alignment=alignment.bottom_left,
                        ),
                        Container(
                            content=Text(
                                value=str(price) + ' BYN',
                                style=TextThemeStyle.BODY_LARGE,
                                color=self.client.theme.primary_color
                            ),
                            alignment=alignment.bottom_right,
                        )
                    ],
                )
            ],
            horizontal_alignment=CrossAxisAlignment.START,
            alignment=MainAxisAlignment.CENTER,
            spacing=1,
        )

        self.padding = 0
        self.content = card
        self.ink = True
        self.margin = margin.only(
            left=20,
            right=20,
        )
        self.ink = True
        self.alignment = alignment.center
        self.col = {
            'xs': 100,
            'xl': 1
        }
        self.data = id

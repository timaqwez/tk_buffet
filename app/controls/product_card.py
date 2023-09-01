from flet_core import Column, Container, CrossAxisAlignment, IconButton, Image, ImageFit, ImageRepeat, \
    MainAxisAlignment, Stack, Text, alignment, icons, margin
from flet_manager import App

from app.controls.available_container import AvailableContainer


class ProductCard(Container):
    app: App
    product_id: int
    is_favorite: bool
    product: dict

    def __init__(self, app: App, product: dict, is_favorite: bool, on_click, on_favorite_button_click, **kwargs):
        super().__init__(
            **kwargs,
        )
        self.app = app
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
                Stack(
                    controls=[
                        Container(
                            content=Image(
                                src=f'assets/images/{image_name}',
                                fit=ImageFit.FIT_WIDTH,
                                repeat=ImageRepeat.NO_REPEAT,
                                border_radius=10,
                                width=500,
                                height=200,

                            ),
                            alignment=alignment.center
                        ),
                        AvailableContainer(app=self.app, count=count),
                        Container(
                            content=IconButton(
                                icon=icons.FAVORITE_OUTLINE_SHARP,
                                selected_icon=icons.FAVORITE_OUTLINED,
                                selected=self.is_favorite,
                                icon_color=self.app.theme.secondary_color_dark,
                                selected_icon_color=self.app.theme.secondary_color_dark,
                                on_click=self.on_favorite_button_click,
                                icon_size=40,
                                data=self.product_id
                            ),
                            alignment=alignment.top_right,

                        ),
                    ],
                ),
                Stack(
                    controls=[
                        Container(
                            content=Text(
                                value=name,
                                no_wrap=False,
                                size=25,
                                color=self.app.theme.primary_color
                            ),
                            alignment=alignment.bottom_left,
                        ),
                        Container(
                            content=Text(
                                value=str(price) + ' BYN',
                                size=25,
                                color=self.app.theme.primary_color
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

        self.bgcolor = self.app.theme.secondary_color
        self.padding = 0
        self.content = card
        self.ink = True
        self.border_radius = 10
        self.margin = margin.only(
            left=20,
            right=20,
            bottom=50
        )
        self.height = 200
        self.ink = True
        self.alignment = alignment.center
        self.col = {'xs': 100, 'xl': 1}
        self.data = id

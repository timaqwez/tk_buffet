from flet_core import BoxShadow, Container, IconButton, MainAxisAlignment, Row, Stack, Text, TextAlign, \
    TransparentPointer, alignment, \
    icons, padding, Image
from flet_manager import App
from flet_manager.controls import Client


class Header(Container):
    client: Client
    logo: Row
    search_button: IconButton
    menu_button: IconButton

    def __init__(self,
                 client: Client,
                 text: str,
                 on_search_click,
                 on_menu_click,
                 on_logo_click,
                 update_products,
                 is_extended: bool,
                 **kwargs):
        super().__init__(
            **kwargs
        )
        self.back_button = None
        self.client = client
        self.on_search_click = on_search_click
        self.on_menu_click = on_menu_click
        self.on_logo_click = on_logo_click
        self.update_products = update_products
        self.text = text
        self.is_extended = is_extended
        self.create()

    async def get_back(self, e):
        await self.client.view_change(
            go_back=True,
        )
        await self.update_products(e)

    def create(self):
        self.search_button = IconButton(
            icon=icons.SEARCH_OUTLINED,
            icon_color=self.client.theme.primary_color,
            selected_icon=icons.CLOSE_OUTLINED,
            selected_icon_color=self.client.theme.primary_color,
            selected=False,
            icon_size=40,
            style=self.client.theme.icon_button_style,
            on_click=self.on_search_click,
        )
        self.menu_button = IconButton(
            icon=icons.MENU,
            icon_color=self.client.theme.primary_color,
            selected=False,
            icon_size=40,
            style=self.client.theme.icon_button_style,
            on_click=self.on_menu_click
        )
        self.back_button = IconButton(
            icon=icons.ARROW_BACK_IOS_ROUNDED,
            icon_color=self.client.theme.primary_color,
            icon_size=30,
            style=self.client.theme.icon_button_style,
            on_click=self.get_back
        )
        self.logo = Row(
            controls=[
                Image(
                    src=r'assets/icons/loading_animation.svg',
                    width=50,
                    color=self.client.theme.primary_color
                ),
                Text(
                    value=self.text,
                    no_wrap=True,
                    text_align=TextAlign.CENTER,
                    color=self.client.theme.primary_color,
                    size=40 if self.client.page.window_width > 1000 else 20
                ),
            ],
            wrap=True
        )

        self.height = 70
        self.bgcolor = self.client.theme.bg_color
        content = Stack(
            controls=[
                TransparentPointer(
                    content=Container(
                        content=self.logo,
                        alignment=alignment.center_left if self.is_extended else alignment.center,
                        on_click=self.on_logo_click
                    ),
                )
            ]
        )
        if self.is_extended:
            row = Row(
                controls=[
                    Container(
                        content=self.search_button,
                        alignment=alignment.center
                    ),
                    Container(
                        content=self.menu_button,
                        alignment=alignment.center
                    ),
                ],
                alignment=MainAxisAlignment.END,
                spacing=0,
            )
            content.controls.append(row)
        else:
            content.controls.append(
                Container(
                    content=self.back_button,
                    alignment=alignment.center_left
                )
            )
        self.content = content
        self.alignment = alignment.center
        self.padding = padding.only(
            left=17,
            right=9
        )
        self.shadow = BoxShadow(
            color=self.client.theme.bg_color if self.client.theme.is_dark_mode else self.client.theme.secondary_color,
            spread_radius=3,
            blur_radius=10
        )

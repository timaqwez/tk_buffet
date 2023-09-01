from flet_core import BoxShadow, Column, Container, CrossAxisAlignment, IconButton, \
    MainAxisAlignment, Row, \
    Text, TextThemeStyle, \
    icons
from flet_manager import App


class NavBar(Container):
    app: App
    menu_tab: Container
    favorite_tab: Container

    def __init__(self,
                 on_navbar_menu_click,
                 on_navbar_favorite_click,
                 app: App,
                 is_activated: bool,
                 on_change,
                 **kwargs):
        super().__init__(
            **kwargs
        )
        self.app = app
        self.on_navbar_menu_click = on_navbar_menu_click
        self.on_navbar_favorite_click = on_navbar_favorite_click
        self.is_activated = is_activated
        self.on_change = on_change
        self.create()

    def create(self):
        if self.is_activated:
            self.height = 90
            self.bgcolor = self.app.theme.bg_color
            self.menu_tab = Container(
                content=Column(
                    controls=[
                        IconButton(
                            icon=icons.MENU_ROUNDED,
                            selected_icon=icons.MENU_ROUNDED,
                            icon_color=self.app.theme.secondary_color_dark,
                            selected_icon_color=self.app.theme.primary_color,
                            icon_size=40,
                            height=50,
                            selected=True,
                            disabled=True,
                        ),
                        Text(
                            style=TextThemeStyle.BODY_SMALL,
                            size=20,
                            value='Меню',
                            color=self.app.theme.primary_color
                        )
                    ],
                    spacing=0,
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                bgcolor=self.app.theme.bg_color,
                expand=True,
                on_click=self.on_navbar_menu_click,
                ink=True
            )
            self.favorite_tab = Container(
                content=Column(
                    controls=[
                        IconButton(
                            icon=icons.FAVORITE_OUTLINE_SHARP,
                            selected_icon=icons.FAVORITE_OUTLINED,
                            icon_color=self.app.theme.secondary_color_dark,
                            selected_icon_color=self.app.theme.primary_color,
                            icon_size=40,
                            height=50,
                            selected=False,
                            disabled=True
                        ),
                        Text(
                            style=TextThemeStyle.BODY_SMALL,
                            size=20,
                            value='Избранное',
                            color=self.app.theme.secondary_color_dark
                        )
                    ],
                    spacing=0,
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                bgcolor=self.app.theme.bg_color,
                expand=True,
                on_click=self.on_navbar_favorite_click,
            )
            self.content = Row(
                controls=[
                    self.menu_tab,
                    self.favorite_tab,
                ],
                spacing=0,
                vertical_alignment=CrossAxisAlignment.CENTER,
                alignment=MainAxisAlignment.CENTER,
            )
            self.shadow = BoxShadow(
                color=self.app.theme.bg_color if self.app.theme.is_dark_mode else self.app.theme.secondary_color,
                spread_radius=3,
                blur_radius=10
            )
        else:
            self.height = 40
            self.bgcolor = self.app.theme.bg_color



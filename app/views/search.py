from flet_core import BorderSide, Column, Container, CrossAxisAlignment, Icon, IconButton, InputBorder, \
    Row, \
    Stack, Text, TextField, \
    TextStyle, TextThemeStyle, alignment, border, icons, margin, padding

from app.controls.view import View


class SearchView(View):
    route = '/search'
    is_navbar: bool = False
    is_header_activated: bool = False
    is_header_extended: bool = False
    header_text: str = 'Меню ТК ГрГУ'
    search_field: TextField
    back_button: IconButton

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs
        )

    async def get_back(self, e):
        await self.app.view_change(
            go_back=True,
        )

    async def build(self):
        queries = self.app.session.search_queries.copy()
        queries.reverse()
        self.search_field = TextField(
            border_color=self.app.theme.primary_color,
            focused_color=self.app.theme.primary_color,
            cursor_color=self.app.theme.primary_color,
            cursor_width=2,
            label='Поиск',
            label_style=TextStyle(
                font_family=self.app.theme.text_style_small_regular.font_family,
                color=self.app.theme.primary_color,
                size=self.app.theme.text_style_medium_regular.size,
            ),
            focused_bgcolor='black',
            text_style=TextStyle(
                font_family=self.app.theme.text_style_small_regular.font_family,
                color=self.app.theme.primary_color,
                size=self.app.theme.text_style_large_regular.size,
            ),
            border=InputBorder.NONE,
            visible=True,
            autofocus=True,
            on_submit=self.params.get('on_search_submit'),
        )
        self.back_button = IconButton(
            icon=icons.CLOSE_OUTLINED,
            icon_color=self.app.theme.primary_color,
            icon_size=40,
            on_click=self.get_back,
        )
        self.controls = [
            Container(
                content=Row(
                    controls=[
                        Container(
                            content=self.search_field,
                            expand=True,
                        ),
                        Container(
                            content=self.back_button,
                            alignment=alignment.bottom_right,
                            padding=padding.only(
                                bottom=10
                            )
                        )
                    ],
                    vertical_alignment=CrossAxisAlignment.END,
                    spacing=0,
                ),
                margin=margin.only(
                    left=20,
                    right=20,
                    bottom=10
                ),
                border=border.only(
                    bottom=BorderSide(
                        width=1,
                        color=self.app.theme.secondary_color_dark
                    )
                ),
            ),
            Container(
                content=Column(
                    controls=[
                        Container(
                            content=
                            Stack(
                                controls=[
                                    Container(
                                        content=Text(
                                            value=query,
                                            style=TextThemeStyle.BODY_MEDIUM,
                                            no_wrap=False,
                                            color=self.app.theme.primary_color
                                        ),
                                        alignment=alignment.center_left,
                                    ),
                                    Container(
                                        content=Icon(
                                            name=icons.ACCESS_TIME_ROUNDED,
                                            size=30,
                                            color=self.app.theme.primary_color,
                                        ),
                                        alignment=alignment.center_right,
                                    ),
                                ],
                            ),
                            alignment=alignment.center,
                            border=border.only(
                                bottom=BorderSide(
                                    width=1,
                                    color=self.app.theme.secondary_color
                                )
                            ),
                            padding=padding.only(
                                bottom=10,
                            ),
                            margin=margin.only(
                                left=20,
                                right=20,
                            ),
                            on_click=self.params.get('on_search_submit'),
                            data=query,
                        ) for query in queries
                    ]
                )
            )
        ]
        await self.create()

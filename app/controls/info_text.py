from flet_core import BorderSide, Column, Container, Text, TextThemeStyle, alignment, border, margin, padding
from flet_manager import App


class InfoText(Column):
    def __init__(self, app: App, text_1: str, text_2: str, **kwargs):
        super().__init__(
            **kwargs
        )
        self.app = app
        self.text_1 = text_1
        self.text_2 = text_2
        self.create()

    def create(self):
        self.controls = [
            Container(
                content=Text(
                    value=self.text_1,
                    no_wrap=False,
                    style=TextThemeStyle.BODY_LARGE,
                    color=self.app.theme.secondary_color
                ),
                alignment=alignment.bottom_left,
                margin=margin.only(
                    left=20,
                    right=20,
                ),
            ),
            Container(
                content=Text(
                    value=self.text_2,
                    style=TextThemeStyle.BODY_MEDIUM,
                    no_wrap=False,
                    color=self.app.theme.primary_color
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
        ]
        self.spacing = 0

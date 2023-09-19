from flet_core import ButtonStyle, Container, ElevatedButton, Icon, MaterialState, RoundedRectangleBorder, Row, Text, \
    TextThemeStyle, colors, \
    icons, \
    padding
from flet_manager import App
from flet_manager.controls import Client


class AvailableContainer(Container):
    client: Client
    count: int

    def __init__(self, client: Client, count: int):
        self.client = client
        self.count = count
        super().__init__()
        self.create()

    def create(self):
        self.content = ElevatedButton(
            content=Row(
                controls=[
                    Container(
                        content=Icon(
                            name=icons.CHECK_CIRCLE_ROUNDED if self.count > 0 else icons.DO_NOT_DISTURB_ON_SHARP,
                            color=self.client.theme.bg_color,
                        ),
                    ),
                    Container(
                        content=Text(
                            value='В наличии' if self.count > 15 else 'Мало' if self.count > 0 else 'Закончилось',
                            color=self.client.theme.bg_color,
                            style=TextThemeStyle.BODY_SMALL
                        ),
                        padding=padding.only(
                            right=2
                        ),
                    ),
                ],
                spacing=3,
                wrap=True
            ),
            disabled=True,
            style=ButtonStyle(
                shape={
                    MaterialState.DEFAULT: RoundedRectangleBorder(radius=6),
                },
                padding={
                    MaterialState.DEFAULT: padding.all(4),
                },
                bgcolor={
                    MaterialState.DEFAULT:
                        colors.GREEN_500 if self.count > 15
                        else colors.ORANGE_400 if self.count > 0
                        else colors.RED_400,
                },
                overlay_color={
                    MaterialState.HOVERED: self.client.theme.secondary_color_light},
            ),
        )
        self.padding = 10
        self.expand = False


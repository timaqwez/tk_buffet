from flet_core import ButtonStyle, Container, ElevatedButton, Icon, MaterialState, RoundedRectangleBorder, Row, Text, \
    colors, \
    icons, \
    padding
from flet_manager import App


class AvailableContainer(Container):
    app: App
    count: int

    def __init__(self, app: App, count: int):
        self.app = app
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
                            color=self.app.theme.bg_color,
                            size=25,
                        ),
                    ),
                    Container(
                        content=Text(
                            value='В наличии' if self.count > 15 else 'Мало' if self.count > 0 else 'Закончилось',
                            color=self.app.theme.bg_color,
                            size=14,
                        ),
                        padding=padding.only(
                            right=2
                        )
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
                    MaterialState.HOVERED: self.app.theme.secondary_color_light},
            ),
        )
        self.padding = 10
        self.expand = False

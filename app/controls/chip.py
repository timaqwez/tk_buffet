from flet_core import ButtonStyle, FilledButton, MaterialState, RoundedRectangleBorder, Text, TextAlign, TextThemeStyle, \
    padding
from flet_manager import App


class Chip(FilledButton):
    category_id: int
    text: str
    is_active: bool

    def __init__(self, app: App, text: str, is_active: bool, category_id: int, **kwargs):
        super().__init__(
            **kwargs
        )
        self.app = app
        self.text = text
        self.is_active = is_active
        self.category_id = category_id
        self.create()

    def create(self):
        self.height = 25
        self.style = ButtonStyle(
            shape={MaterialState.DEFAULT: RoundedRectangleBorder(radius=6)},
            padding={MaterialState.DEFAULT: padding.symmetric(horizontal=5)},
            overlay_color={
                MaterialState.HOVERED: self.app.theme.primary_color if self.is_active
                else self.app.theme.secondary_color_light,
            },
            bgcolor={
                MaterialState.DISABLED: self.app.theme.secondary_color_dark if self.is_active
                else self.app.theme.secondary_color
            }
        )
        self.content = Text(
            value=self.text,
            style=TextThemeStyle.BODY_MEDIUM,
            text_align=TextAlign.LEFT,
            color=self.app.theme.bg_color if self.is_active else self.app.theme.primary_color
        )
        if self.app.theme.is_dark_mode and self.is_active:
            self.bgcolor = self.app.theme.secondary_color
        elif self.app.theme.is_dark_mode:
            self.bgcolor = self.app.theme.secondary_color_dark
        elif not self.app.theme.is_dark_mode and self.is_active:
            self.bgcolor = self.app.theme.secondary_color_dark
        elif not self.app.theme.is_dark_mode:
            self.bgcolor = self.app.theme.secondary_color


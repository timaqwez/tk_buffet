from flet_core import Checkbox, Container, Row, Text, TextThemeStyle, alignment
from flet_manager import App
from flet_manager.controls import Client


class MenuItem(Container):
    label: Text
    checkbox: Checkbox
    text: str

    def __init__(self, client: Client, text: str, on_checkbox_change, **kwargs):
        super().__init__(
            **kwargs
        )
        self.client = client
        self.text = text
        self.on_checkbox_change = on_checkbox_change
        self.create()

    def create(self):
        self.label = Text(
            value=self.text,
            style=TextThemeStyle.BODY_MEDIUM,
            color=self.client.theme.primary_color
        )
        self.checkbox = Checkbox(
            value=self.client.theme.is_dark_mode,
            on_change=self.on_checkbox_change,
            fill_color=self.client.theme.primary_color,
            check_color=self.client.theme.bg_color,
        )
        self.content = Row(
            controls=[
                self.label,
                self.checkbox
            ]
        )
        self.alignment = alignment.center

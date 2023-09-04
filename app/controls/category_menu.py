from flet_core import ButtonStyle, Container, ElevatedButton, Icon, MaterialState, Row, \
    alignment, \
    icons, padding
from flet_manager import App
from app.controls.chip import Chip


class CategoryMenu(Container):
    categories: list
    is_active: bool
    active_id: int
    close_button: ElevatedButton
    app: App

    def __init__(self,
                 on_category_button_click,
                 on_close_button_click,
                 categories: list,
                 app: App,
                 is_active: bool,
                 active_id: int = 0,
                 **kwargs):
        super().__init__(
            **kwargs
        )
        self.app = app
        self.categories = categories
        self.is_active = is_active
        self.active_id = active_id
        self.on_category_button_click = on_category_button_click
        self.on_close_button_click = on_close_button_click
        self.create()

    def create(self):
        self.close_button = ElevatedButton(
            style=ButtonStyle(
                padding={MaterialState.DEFAULT: padding.symmetric(horizontal=0)},
                overlay_color={
                    MaterialState.DEFAULT: self.app.theme.secondary_color,
                },
                bgcolor={
                    MaterialState.DEFAULT: self.app.theme.secondary_color
                }

            ),
            content=Icon(
                name=icons.CLOSE_OUTLINED,
                color=self.app.theme.primary_color,
                size=25,
            ),
            height=25,
            width=25,
            on_click=self.on_close_button_click
        )
        self.content = Row(
            controls=[
                Chip(app=self.app,
                     text=category['name'].capitalize(),
                     is_active=True if category['id'] == self.active_id else False,
                     category_id=category['id'],
                     on_click=self.on_category_button_click)
                for category in self.categories
            ],
            wrap=True,
        )
        self.padding = padding.only(
            left=20,
            right=20,
            bottom=20
        )
        self.alignment = alignment.top_left
        if self.active_id != 0:
            self.content.controls.append(
                self.close_button
            )

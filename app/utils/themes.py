from enum import Enum

import flet
from flet_core import ButtonStyle, ColorScheme, ScrollbarTheme, TextStyle, TextTheme, Theme, colors


class WhiteTheme:
    primary_color: str = 'black'
    bg_color: str = 'white'
    secondary_color: str = colors.GREY_300
    secondary_color_dark: str = colors.GREY_500
    secondary_color_light: str = colors.GREY_200
    is_dark_mode = False
    is_zhur_mode = False

    text_style_small_regular = TextStyle(
        font_family='Regular',
        color=primary_color,
        size=10
    )
    text_style_medium_regular = TextStyle(
        font_family='Regular',
        color=primary_color,
        size=17
    )
    text_style_large_regular = TextStyle(
        font_family='Regular',
        color=primary_color,
        size=22
    )
    text_style_semi_bold = TextStyle(
        font_family='SemiBold',
        color=primary_color
    )
    app_theme = Theme(
        color_scheme=ColorScheme(
            surface=bg_color,
            surface_tint=bg_color,
            primary=secondary_color,
            on_surface=primary_color,
            on_primary=primary_color,
            secondary_container=bg_color,
            on_secondary_container=primary_color,
            on_secondary=bg_color,
            outline=primary_color,
            outline_variant='',
        ),
        text_theme=TextTheme(
            label_medium=TextStyle(
                font_family='Regular',
                color=primary_color,
                size=15
            ),
            label_large=text_style_large_regular,
            label_small=text_style_small_regular,
            body_small=text_style_small_regular,
            body_medium=text_style_medium_regular,
            body_large=text_style_large_regular,
        ),
        scrollbar_theme=ScrollbarTheme(
            track_color=primary_color,
            track_border_color=primary_color,
            thickness=0
        )
    )
    icon_button_style = ButtonStyle(
        bgcolor=bg_color,
        overlay_color=bg_color,
        color=bg_color,
        surface_tint_color=bg_color,
    )

    async def dark_mode_switch(self, e):
        self.is_dark_mode = not self.is_dark_mode
        self.primary_color = 'white' if self.is_dark_mode else 'black'
        self.bg_color = 'black' if self.is_dark_mode else 'white'
        self.secondary_color = colors.GREY_500 if self.is_dark_mode else colors.GREY_300
        self.secondary_color_dark = colors.GREY_700 if self.is_dark_mode else colors.GREY_500
        self.secondary_color_light = colors.GREY_400 if self.is_dark_mode else colors.GREY_200
        self.icon_button_style = ButtonStyle(
            bgcolor=self.bg_color,
            overlay_color=self.bg_color,
            color=self.bg_color,
            surface_tint_color=self.bg_color,
        )
        return self

    async def zhuravskaya_mode_switch(self, e):
        self.is_zhur_mode = not self.is_zhur_mode
        if self.is_zhur_mode:
            self.text_style_small_regular.font_family = 'Times New Roman'
            self.text_style_medium_regular.font_family = 'Times New Roman'
            self.text_style_large_regular.font_family = 'Times New Roman'
            self.text_style_semi_bold.font_family = 'Times New Roman'
        else:
            self.text_style_small_regular.font_family = 'Regular'
            self.text_style_medium_regular.font_family = 'Regular'
            self.text_style_large_regular.font_family = 'Regular'
            self.text_style_semi_bold.font_family = 'SemiBold'
        return self


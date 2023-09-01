from typing import List, Optional

from flet_core import Control
from flet_manager.views import BaseView

from app.controls import Header, NavBar


class View(BaseView):
    main_controls: Optional[List[Control]] = None
    is_header_extended: bool
    is_header_activated: bool
    is_navbar: bool
    header_text: str
    navbar: NavBar

    async def favorite_button_click(self, e):
        favorite_ids = self.app.session.favorite_ids
        if e.control.data in favorite_ids:
            favorite_ids.remove(e.control.data)
            favorite_ids.sort()
        else:
            favorite_ids.append(e.control.data)
            favorite_ids.sort()
        self.app.session.favorite_ids = favorite_ids
        await self.app.session.save_favorite_ids()
        e.control.selected = not e.control.selected
        if self.is_navbar and self.navbar.favorite_tab.content.controls[0].selected:
            await self.params.get('on_navbar_favorite_click')(e)
        else:
            await e.control.update_async()
        await self.app.page.update_async()
        print(favorite_ids)

    async def create(self):
        await self.app.session.save_favorite_ids()
        self.app.page.fonts = {
            'Bold': r'assets\fonts\Montserrat\Bold.ttf',
            'SemiBold': r'assets\fonts\Montserrat\SemiBold.ttf',
            'Medium': r'assets\fonts\Montserrat\Medium.ttf',
            'Regular': r'assets\fonts\Montserrat\Regular.ttf',
        }
        self.padding = 0
        self.spacing = 0
        self.bgcolor = self.app.theme.bg_color
        if self.is_header_activated:
            self.controls.insert(
                0,
                Header(
                    app=self.app,
                    is_extended=self.is_header_extended,
                    text=self.header_text,
                    on_search_click=self.params.get('on_search_click'),
                    on_menu_click=self.params.get('on_menu_click'),
                    on_logo_click=self.params.get('on_navbar_menu_click'),
                    update_products=self.params.get('update_products')
                )
            )
        self.navbar = NavBar(
                app=self.app,
                is_activated=self.is_navbar,
                on_change=self.params.get('on_navbar_change'),
                on_navbar_menu_click=self.params.get('on_navbar_menu_click'),
                on_navbar_favorite_click=self.params.get('on_navbar_favorite_click')
            )
        self.controls.append(
            self.navbar
        )


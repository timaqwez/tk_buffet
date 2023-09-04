from typing import List, Optional

from flet_core import Control, PageTransitionTheme
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
        await self.save_favorite_ids()
        e.control.selected = not e.control.selected
        await e.control.update_async()
        await self.app.page.update_async()
        print(favorite_ids)

    async def save_favorite_ids(self):
        favorite_ids = self.app.session.favorite_ids
        await self.app.page.client_storage.set_async('favorite_ids', favorite_ids)

    async def load_favorite_ids(self):
        try:
            favorite_ids = await self.app.page.client_storage.get_async('favorite_ids')
            if favorite_ids is None:
                self.app.session.favorite_ids = []
            else:
                self.app.session.favorite_ids = favorite_ids

        except NotImplementedError:
            self.app.session.favorite_ids = []
            await self.app.page.client_storage.set_async('favorite_ids', self.app.session.favorite_ids)

    async def save_search_queries(self):
        search_queries = self.app.session.search_queries
        await self.app.page.client_storage.set_async('search_queries', search_queries)

    async def load_search_queries(self):
        try:
            search_queries = await self.app.page.client_storage.get_async('search_queries')
            if search_queries is None:
                self.app.session.search_queries = []
            else:
                self.app.session.search_queries = search_queries
        except NotImplementedError:
            self.app.session.search_queries = []
            await self.app.page.client_storage.set_async('search_queries', self.app.session.search_queries)

    async def create(self):
        self.app.page.theme.page_transitions.windows = PageTransitionTheme.CUPERTINO
        self.app.page.fonts = {
            'Bold': r'assets\fonts\Montserrat\Bold.ttf',
            'SemiBold': r'assets\fonts\Montserrat\SemiBold.ttf',
            'Medium': r'assets\fonts\Montserrat\Medium.ttf',
            'Regular': r'assets\fonts\Montserrat\Regular.ttf',
            'Times New Roman': r'assets\fonts\times-new-roman.ttf'
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


#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Any

from flet_core import Page
from flet_runtime import app as app_flet
from flet_fastapi import app as app_fastapi

from flet_manager.controls import Client
from flet_manager.views import MainView, ErrorView


class AppType:
    FLET = 'flet'
    FASTAPI = 'fastapi'


class App:
    routes: dict[str]

    def __init__(
            self,
            theme: Any,
            app_type: AppType = AppType.FASTAPI,
            view_main=MainView,
            view_error=ErrorView,
            views: list = None,
            **kwargs,
    ):
        self.view_main = view_main
        self.view_error = view_error
        self.theme = theme

        if not views:
            views = []
        self.routes = {}
        for view in views:
            self.routes[view.route] = view

        if app_type == AppType.FASTAPI:
            self.fastapi = app_fastapi(session_handler=self.start, **kwargs)
        elif app_type == AppType.FLET:
            app_flet(target=self.start, **kwargs)

    async def start(self, page: Page):
        self.client = Client(
            page=page,
            routes=self.routes,
            view_main=self.view_main,
            view_error=self.view_error,
            theme=self.theme
        )
        await self.client.change_view(
            view=self.view_main(),
        )

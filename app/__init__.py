from starlette.staticfiles import StaticFiles

from flet_manager import App

from app.views import views
from app.utils.themes import WhiteTheme
from app.views import MainView
from flet_manager.app import AppType


def app_start():
    app_type = AppType.FLET
    app = App(
        views=views,
        assets_dir='assets',
        view_main=MainView,
        theme=WhiteTheme(),
        port=53570,
        app_type=app_type
    )
    if app_type == AppType.FASTAPI:
        return app.fastapi

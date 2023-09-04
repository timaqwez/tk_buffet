from flet_manager import App

from app.utils.session import Session
from app.views import views
from app.utils.themes import WhiteTheme
from app.views import MainView


def app_start():
    # fastapi_app = App(
    #     title='Буфет',
    #     views=views,
    #     assets_dir='assets',
    #     main_view=MainView,
    #     theme=WhiteTheme(),
    #     session=Session()
    # )
    # return fastapi_app
    App(
        title='Буфет',
        views=views,
        assets_dir='assets',
        main_view=MainView,
        theme=WhiteTheme(),
        session=Session(),
        host='192.168.1.106',
        port='53570'
    )

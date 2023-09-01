from flet_manager import App

from app.utils.session import Session
from app.views import views
from app.utils.themes import WhiteTheme
from app.views import MainView


def app_start():
    App(
        title='Буфет',
        views=views,
        assets_dir='assets',
        main_view=MainView,
        theme=WhiteTheme(),
        session=Session()
    )

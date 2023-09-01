from app.views.product import ProductView
from app.views.main import MainView
from app.views.search import SearchView


views = [
    MainView,
    ProductView,
    SearchView
]

__all__ = [
    'views',
    'MainView',
    'ProductView',
    'SearchView',
]



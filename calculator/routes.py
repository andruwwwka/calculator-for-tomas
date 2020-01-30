"""Роуты приложения."""
from .views import calculate, frontend


def setup_routes(app):
    """Описание доступных роутов в приложении."""
    app.router.add_route('GET', '/', frontend.index)
    app.router.add_route('GET', '/api/calculate/', calculate.calculate_amount)

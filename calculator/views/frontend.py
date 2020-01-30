"""Модуль отвечающий за рендер главной страницы."""
from aiohttp_jinja2 import template

from ..services import fetch_discount, fetch_tax


@template('index.html')
async def index(request):
    """Метод рендера контекста главной страницы."""
    async with request.app['db'].acquire() as conn:
        discounts = await fetch_discount(conn)
        taxes = await fetch_tax(conn)
        return {'discounts': discounts, 'taxes': taxes}

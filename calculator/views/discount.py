"""Заготовки на развитие, которые позволят управляль таблицей скидок."""
import aiohttp
from webargs import fields
from webargs.aiohttpparser import use_args


@use_args(
    {
        'minimum_amount': fields.Int(required=True),
        'percentage': fields.Int(required=True),
    },
    error_status_code=400,
)
async def create_discount(request, args):
    """Представление создания скидки."""
    async with request.app['db'].acquire() as conn:
        return aiohttp.web.Response()


@use_args(
    {
        'minimum_amount': fields.Int(),
        'percentage': fields.Int(),
    },
    error_status_code=400,
)
async def update_discount(request, args):
    """Представление обновления скидки."""
    async with request.app['db'].acquire() as conn:
        return aiohttp.web.Response()


async def delete_discount(request, args):
    """Представление удаления скидки."""
    async with request.app['db'].acquire() as conn:
        return aiohttp.web.Response()

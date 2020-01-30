"""Заготовки на развитие, которые позволят управляль таблицей налогов."""
import aiohttp
from webargs import fields
from webargs.aiohttpparser import use_args


@use_args(
    {
        'rate': fields.Decimal(required=True),
        'state': fields.Str(required=True),
    },
    error_status_code=400,
)
async def create_tax(request, args):
    """Представление созадния записи с информацией о налогоах."""
    async with request.app['db'].acquire() as conn:
        return aiohttp.web.Response()


@use_args(
    {
        'rate': fields.Decimal(),
        'state': fields.Str(),
    },
    error_status_code=400,
)
async def update_tax(request, args):
    """Представление обновления записи в таблице с налогами."""
    async with request.app['db'].acquire() as conn:
        return aiohttp.web.Response()


async def delete_tax(request, args):
    """Представление удаления записи из таблицы налогов."""
    async with request.app['db'].acquire() as conn:
        return aiohttp.web.Response()

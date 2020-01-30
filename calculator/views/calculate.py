"""Реализация логики вьюшки калькулятора."""
import aiohttp
from marshmallow import Schema
from webargs import fields
from webargs.aiohttpparser import use_args

from .. import db
from ..services import calculate_total_amount

__all__ = ('calculate_amount', )


class CalculateResponse(Schema):
    """Схема для сериализации ответа."""

    amount_with_discount = fields.Number()
    total_amount = fields.Number()


@use_args(
    {
        'count': fields.Int(required=True),
        'price': fields.Decimal(required=True),
        'state': fields.Str(required=True),
    },
    error_status_code=400,
)
async def calculate_amount(request, args):
    """Представление для вычисления суммы с учетом скидки и с учетом налогов."""
    async with request.app['db'].acquire() as conn:
        try:
            amount_with_discount, total_amount = await calculate_total_amount(
                conn,
                args['state'],
                args['price'],
                args['count'],
            )
        except db.RecordNotFound:
            raise aiohttp.web.HTTPNotFound
        response = {
            'amount_with_discount': amount_with_discount,
            'total_amount': total_amount,
        }
        return aiohttp.web.json_response(CalculateResponse().dump(response))

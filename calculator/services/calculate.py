"""Реализация основного функционала приложения."""
from decimal import Decimal

from sqlalchemy.sql import select

from .. import db


async def calculate_total_amount(conn, state, price, count):
    """Вычисление суммы покупки с учетом скидки и с учетом налогов.

    :param conn: Соединение с БД
    :param state: ISO  код штата
    :param price: Цена за единицу товара
    :param count: Количество товаров
    :return: Сумма со скидкой и итоговая сумма.
    """
    raw_amount = price * count
    state_rate = await conn.fetchrow(
        select([db.tax.c.rate])
        .where(db.tax.c.state == state),
    )
    if not state_rate:
        raise db.RecordNotFound(f'State with code {state} not found')
    state_rate = state_rate.get('rate')
    discount = await conn.fetchrow(
        select([db.discount.c.percentage])
        .where(db.discount.c.minimum_amount <= float(raw_amount))
        .order_by(db.discount.c.minimum_amount.desc()),
    )
    if not discount:
        discount = 0
    else:
        discount = discount.get('percentage')
    one_percent = Decimal(10) ** -2
    amount_with_discount = raw_amount - (raw_amount * one_percent * discount)
    total_amount = amount_with_discount + (amount_with_discount * one_percent * state_rate)
    return amount_with_discount.quantize(one_percent), total_amount.quantize(one_percent)

"""Тест бизнес логики приложения."""
from decimal import Decimal

import pytest

from calculator import db
from calculator.services import calculate_total_amount, fetch_discount, fetch_tax


one_percent = Decimal(10) ** -2


async def test_with_discount_and_exists_state(tables_and_data, client):
    """Проверяем позитивные кейсы, когда существует налог для штата и достигнута сумма для скидки."""
    async with client.app['db'].acquire() as conn:
        amount_with_discount, total_amount = await calculate_total_amount(
            conn,
            'AR',
            Decimal(20),
            5,
        )
        assert amount_with_discount == Decimal(95).quantize(one_percent)
        assert total_amount == Decimal(100.42).quantize(one_percent)
        amount_with_discount, total_amount = await calculate_total_amount(
            conn,
            'AR',
            Decimal(20),
            10,
        )
        assert amount_with_discount == Decimal(180).quantize(one_percent)
        assert total_amount == Decimal(190.26).quantize(one_percent)
        amount_with_discount, total_amount = await calculate_total_amount(
            conn,
            'WY',
            Decimal(20),
            5,
        )
        assert amount_with_discount == Decimal(95).quantize(one_percent)
        assert total_amount == Decimal(102.41).quantize(one_percent)
        amount_with_discount, total_amount = await calculate_total_amount(
            conn,
            'WY',
            Decimal(20),
            10,
        )
        assert amount_with_discount == Decimal(180.00).quantize(one_percent)
        assert total_amount == Decimal(194.04).quantize(one_percent)


async def test_with_not_exists_state(tables_and_data, client):
    """При запросе штата, для которого нет записи налога должны получить исключение."""
    async with client.app['db'].acquire() as conn:
        with pytest.raises(db.RecordNotFound):
            amount_with_discount, total_amount = await calculate_total_amount(
                conn,
                'WI',
                Decimal(20),
                5,
            )


async def test_without_discount_and_exists_state(tables_and_data, client):
    """Если не набрали минимальную сумму для скидки, то размер скидки должен быть равен нулю."""
    async with client.app['db'].acquire() as conn:
        amount_with_discount, total_amount = await calculate_total_amount(
            conn,
            'AR',
            Decimal(20),
            4,
        )
        assert amount_with_discount == Decimal(80).quantize(one_percent)
        assert total_amount == Decimal(84.56).quantize(one_percent)
        amount_with_discount, total_amount = await calculate_total_amount(
            conn,
            'WY',
            Decimal(20),
            4,
        )
        assert amount_with_discount == Decimal(80).quantize(one_percent)
        assert total_amount == Decimal(86.24).quantize(one_percent)


async def test_fetch_discounts_method(tables_and_data, client):
    """Если не набрали минимальную сумму для скидки, то размер скидки должен быть равен нулю."""
    async with client.app['db'].acquire() as conn:
        discounts = await fetch_discount(conn)
        assert len(discounts) == 2


async def test_fetch_taxes_method(tables_and_data, client):
    """Если не набрали минимальную сумму для скидки, то размер скидки должен быть равен нулю."""
    async with client.app['db'].acquire() as conn:
        taxes = await fetch_tax(conn)
        assert len(taxes) == 2

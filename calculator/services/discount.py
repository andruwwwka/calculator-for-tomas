"""Бизнес логика работы с таблицей скидок."""
from .. import db


__all__ = ('fetch_discount', )


async def fetch_discount(conn):
    """Получение всех записей из таблицы скидок."""
    discount = await conn.fetch(
        db.discount
        .select(),
    )
    return discount


async def create_discount(conn, discount_data):
    """Создание записи в таблице скидок."""
    result = await conn.execute(
        db.discount
        .insert()
        .values(**discount_data),
    )
    return result


async def delete_discount(conn, discount_id):
    """Удаление записи из таблицы скидок."""
    result = await conn.execute(
        db.discount
        .delete()
        .where(db.discount.c.id == discount_id),
    )
    return result


async def update_discount(conn, discount_id, discount_data):
    """Обновление записи в таблице скидок."""
    result = await conn.execute(
        db.discount
        .update()
        .where(db.discount.c.id == discount_id).values(**discount_data),
    )
    return result

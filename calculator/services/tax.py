"""Бизнес логика работы с таблицой налогов."""
from .. import db


__all__ = ('fetch_tax', )


async def fetch_tax(conn):
    """Получение всех записей о размере налога."""
    discount = await conn.fetch(
        db.tax
        .select(),
    )
    return discount


async def create_tax(conn, tax_data):
    """Создание записи для таблицы налогов."""
    result = await conn.execute(
        db.tax
        .insert()
        .values(**tax_data),
    )
    return result


async def delete_tax(conn, tax_id):
    """Удаление записи из таблицы налогов."""
    result = await conn.execute(
        db.tax
        .delete()
        .where(db.tax.c.id == tax_id),
    )
    return result


async def update_tax(conn, tax_id, tax_data):
    """Обновление записи в таблице налогов."""
    result = await conn.execute(
        db.discount
        .update()
        .where(db.discount.c.id == tax_id)
        .values(**tax_data),
    )
    return result

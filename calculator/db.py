"""Описание таблиц."""
from sqlalchemy import Column, DECIMAL, Integer, MetaData, Table, VARCHAR


__all__ = (
    'discount',
    'tax',
    'RecordNotFound',
    'construct_db_url',
)


meta = MetaData()


discount = Table(
    'discount', meta,

    Column('id', Integer, primary_key=True),
    Column('minimum_amount', Integer, nullable=False),
    Column('percentage', Integer, nullable=False),
)


tax = Table(
    'tax', meta,

    Column('id', Integer, primary_key=True),
    Column('state', VARCHAR(2), nullable=False),
    Column('rate', DECIMAL(precision=5, scale=2), nullable=False),
)


class RecordNotFound(Exception):
    """Класс ошибки для обработки запроса, который не нашел записи."""


def construct_db_url(config):
    """Преобразование конфигов соединения с БД в строковый вид.

    :param config: Конфигурация подключения с БД
    :return: Строка для подключения к БД
    """
    dsn = 'postgresql://{user}:{password}@{host}:{port}/{database}'
    return dsn.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )

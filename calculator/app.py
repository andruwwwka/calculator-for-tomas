"""Методы инициализации приложения."""
import aiohttp_jinja2
import asyncpgsa
import jinja2
from aiohttp import web

from .db import construct_db_url
from .routes import setup_routes


async def create_app(config: dict):
    """Создание объекта приложения и инициализация его атрибутов."""
    app = web.Application()
    app['config'] = config
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('calculator', 'templates'),
    )
    app.on_startup.append(on_start)
    app.on_shutdown.append(on_shutdown)
    setup_routes(app)
    return app


async def on_start(app):
    """Создание соединения с БД."""
    config = app['config']
    database_uri = construct_db_url(config['database'])
    app['db'] = await asyncpgsa.create_pool(dsn=database_uri)


async def on_shutdown(app):
    """Закрытие соединения с БД."""
    await app['db'].close()

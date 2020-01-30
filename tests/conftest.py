"""Фикстуры для тестов."""
import pytest

from calculator.app import create_app
from calculator.settings import load_config, BASE_DIR
from .helpers import setup_db, teardown_db, create_sample_data, create_tables, drop_tables


@pytest.fixture
async def client(aiohttp_client):
    """Http - клиент."""
    config = load_config(BASE_DIR / 'config' / 'test.yaml')
    app = await create_app(config)
    return await aiohttp_client(app)


@pytest.fixture(scope='session')
def database():
    """Фикстура БД."""
    admin_db_config = load_config(BASE_DIR / 'config' / 'default.yaml')['database']
    test_db_config = load_config(BASE_DIR / 'config' / 'test.yaml')['database']

    setup_db(executor_config=admin_db_config, target_config=test_db_config)
    yield
    teardown_db(executor_config=admin_db_config, target_config=test_db_config)


@pytest.fixture
def tables_and_data(database):
    """Фикстура с начальными данными."""
    config = load_config(BASE_DIR / 'config' / 'test.yaml')['database']

    create_tables(target_config=config)
    create_sample_data(target_config=config)
    yield
    drop_tables(target_config=config)

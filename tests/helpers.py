"""Вспомогательные методы для инициализации тестовой БД."""
from sqlalchemy import create_engine, MetaData

from calculator import db


def setup_db(executor_config=None, target_config=None):
    """Созадние БД."""
    engine = get_engine(executor_config)

    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']
    db_pass = target_config['DB_PASS']

    with engine.connect() as conn:
        teardown_db(executor_config=executor_config,
                    target_config=target_config)

        conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
        conn.execute("CREATE DATABASE %s" % db_name)
        conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                     (db_name, db_user))


def teardown_db(executor_config=None, target_config=None):
    """Удаление БД."""
    engine = get_engine(executor_config)

    db_name = target_config['DB_NAME']
    db_user = target_config['DB_USER']

    with engine.connect() as conn:
        # terminate all connections to be able to drop database
        conn.execute("""
          SELECT pg_terminate_backend(pg_stat_activity.pid)
          FROM pg_stat_activity
          WHERE pg_stat_activity.datname = '%s'
            AND pid <> pg_backend_pid();""" % db_name)
        conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
        conn.execute("DROP ROLE IF EXISTS %s" % db_user)


def get_engine(db_config):
    """Соединение с БД."""
    db_url = db.construct_db_url(db_config)
    engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
    return engine


def create_tables(target_config=None):
    """Созадние таблиц."""
    engine = get_engine(target_config)

    meta = MetaData()
    meta.create_all(bind=engine, tables=[db.tax, db.discount])


def drop_tables(target_config=None):
    """Удаление таблиц."""
    engine = get_engine(target_config)

    meta = MetaData()
    meta.drop_all(bind=engine, tables=[db.tax, db.discount])


def create_sample_data(target_config=None):
    """Создание записей в БД для тестов."""
    engine = get_engine(target_config)

    with engine.connect() as conn:
        conn.execute(db.tax.insert(), [
            {'state': 'AR',
             'rate': 5.7},
            {'state': 'WY',
             'rate': 7.8},
        ])
        conn.execute(db.discount.insert(), [
            {'minimum_amount': 100, 'percentage': 5},
            {'minimum_amount': 200, 'percentage': 10},
        ])

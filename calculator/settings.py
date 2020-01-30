"""Загрузка конфигурации."""
from pathlib import Path

import yaml

__all__ = ('load_config', 'BASE_DIR')


BASE_DIR = Path(__file__).parent.parent


def load_config(config_file=None):
    """Чтение конфигурации из yaml файла.

    :param config_file: Путь до файла, который перекрывает стандарнтые конфиги.
    :return: Словарь конфигурации.
    """
    default_file = BASE_DIR / 'config' / 'default.yaml'
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    cf_dict = {}
    if config_file:
        with open(config_file, 'r') as f:
            cf_dict = yaml.safe_load(f)

    config.update(cf_dict)
    return config

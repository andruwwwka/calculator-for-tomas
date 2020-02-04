"""Запуск приложения."""
import argparse
import asyncio

import aiohttp
import uvloop

from calculator import create_app
from calculator.settings import load_config

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

parser = argparse.ArgumentParser(description='Calculator for Tomas')
parser.add_argument('--port', help='Port to accept connections', default=8080)
parser.add_argument(
    '-c',
    '--config',
    type=argparse.FileType('r'),
    help='Path to configuration file',
)
args = parser.parse_args()

app = create_app(config=load_config(args.config))

if __name__ == '__main__':
    aiohttp.web.run_app(app, port=args.port)

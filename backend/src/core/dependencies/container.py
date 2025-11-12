from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.core.di.providers import (
    ConfigProvider,
    DatabaseProvider,
    RedisProvider,
)

container = make_async_container(
    ConfigProvider(),
    DatabaseProvider(),
    RedisProvider(),
    FastapiProvider(),
)

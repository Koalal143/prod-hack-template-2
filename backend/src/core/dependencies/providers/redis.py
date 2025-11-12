from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from src.core.config import Settings


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    def get_redis(self, settings: Settings) -> Redis:
        return Redis(
            host=settings.redis.host, port=settings.redis.port, db=settings.redis.db, password=settings.redis.password
        )

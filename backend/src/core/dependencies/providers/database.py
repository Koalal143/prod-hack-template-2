from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.config import Settings
from src.db.manager import DatabaseManager


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_database_engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(
            settings.postgres.url.get_secret_value(),
            echo=settings.postgres.echo,
            pool_size=10,
            max_overflow=20,
        )

    @provide(scope=Scope.APP)
    def get_database_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=True)

    @provide(scope=Scope.APP)
    def get_database_manager(
        self, engine: AsyncEngine, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> DatabaseManager:
        return DatabaseManager(engine, sessionmaker)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
        async for session in sessionmaker():
            yield session

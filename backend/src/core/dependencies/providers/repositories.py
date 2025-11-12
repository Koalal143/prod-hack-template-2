from dishka import Provider, Scope, provide
from gigachat import GigaChat
from langchain_gigachat.embeddings import GigaChatEmbeddings
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.chat import ChatRepository, MessageRepository
from src.repositories.embeddings import EmbeddingsRepository
from src.repositories.gigachat_chat import GigaChatRepository
from src.repositories.refresh_token import RefreshTokenRepository
from src.repositories.skill import SkillRepository
from src.repositories.user import UserRepository
from src.repositories.vector_search import VectorSearchRepository


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_skill_repository(self, session: AsyncSession) -> SkillRepository:
        return SkillRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_refresh_token_repository(self, session: AsyncSession, redis: Redis) -> RefreshTokenRepository:
        return RefreshTokenRepository(session, redis)

    @provide(scope=Scope.APP)
    def get_embeddings_repository(self, embeddings: GigaChatEmbeddings) -> EmbeddingsRepository:
        return EmbeddingsRepository(embeddings)

    @provide(scope=Scope.APP)
    def get_vector_search_repository(self, client: AsyncQdrantClient) -> VectorSearchRepository:
        return VectorSearchRepository(client)

    @provide(scope=Scope.REQUEST)
    def get_chat_repository(self, session: AsyncSession) -> ChatRepository:
        return ChatRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_message_repository(self, session: AsyncSession) -> MessageRepository:
        return MessageRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_gigachat_repository(self, session: AsyncSession, gigachat: GigaChat, redis: Redis) -> GigaChatRepository:
        return GigaChatRepository(session, gigachat, redis)

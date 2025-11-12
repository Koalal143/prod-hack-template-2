from dishka import Provider, Scope, provide

from src.repositories.chat import ChatRepository, MessageRepository
from src.repositories.embeddings import EmbeddingsRepository
from src.repositories.gigachat_chat import GigaChatRepository
from src.repositories.refresh_token import RefreshTokenRepository
from src.repositories.skill import SkillRepository
from src.repositories.user import UserRepository
from src.repositories.vector_search import VectorSearchRepository
from src.services.chat import ChatService
from src.services.gigachat import GigaChatService
from src.services.skill import SkillService
from src.services.token import RefreshTokenService, TokenService
from src.services.user import UserService


class ServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_service(self, user_repo: UserRepository) -> UserService:
        return UserService(user_repo)

    @provide(scope=Scope.REQUEST)
    def get_skill_service(
        self,
        skill_repo: SkillRepository,
        vector_search_repo: VectorSearchRepository,
        embeddings_repo: EmbeddingsRepository,
    ) -> SkillService:
        return SkillService(skill_repo, vector_search_repo, embeddings_repo)

    @provide(scope=Scope.REQUEST)
    def get_token_service(
        self,
        refresh_repo: RefreshTokenRepository,
        user_repo: UserRepository,
    ) -> TokenService:
        return TokenService(refresh_repo, user_repo)

    @provide(scope=Scope.REQUEST)
    def get_refresh_token_service(self, refresh_repo: RefreshTokenRepository) -> RefreshTokenService:
        return RefreshTokenService(refresh_repo)

    @provide(scope=Scope.REQUEST)
    def get_chat_service(self, chat_repo: ChatRepository, message_repo: MessageRepository) -> ChatService:
        return ChatService(chat_repo, message_repo)

    @provide(scope=Scope.REQUEST)
    def get_gigachat_service(self, gigachat_repo: GigaChatRepository, user_repo: UserRepository) -> GigaChatService:
        return GigaChatService(gigachat_repo, user_repo)
